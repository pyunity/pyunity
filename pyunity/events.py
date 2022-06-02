# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

__all__ = ["Event"]

from .errors import PyUnityException
from .core import Component, GameObject
from .values import SavableStruct, StructEntry, Clock
from functools import update_wrapper
import threading
import asyncio
import inspect

@SavableStruct(
    component=StructEntry(Component, required=True),
    name=StructEntry(str, required=True),
    args=StructEntry(tuple, required=True))
class Event:
    def __init__(self, func, args=(), kwargs={}):
        if not hasattr(func, "__self__"):
            raise PyUnityException(
                "Cannot create event from callback that is not attached to a Component")
        if not isinstance(func.__self__, Component):
            raise PyUnityException(
                "Cannot create event from callback that is not attached to a Component")
        if not isinstance(func.__self__.gameObject, GameObject):
            raise PyUnityException(
                "Provided callback component does not belong to a GameObject")

        update_wrapper(self, func)

        self.component = func.__self__
        self.name = func.__name__

        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.isAsync = inspect.iscoroutinefunction(func)

    async def asyncTrigger(self):
        await self.func(*self.args, **self.kwargs)

    def trigger(self):
        self.func(*self.args, **self.kwargs)

    def callSoon(self):
        if self.isAsync:
            loop = asyncio.get_running_loop()
            loop.call_soon(self.trigger)
        else:
            if EventLoop.current is None:
                raise PyUnityException("No EventLoop running")
            EventLoop.current.pending.append(self)

    def _fromDict(self, factory, attrs, instanceCheck=None):
        def wrapper(component, method, args=(), kwargs={}):
            func = getattr(component, method)
            return factory(func, args, kwargs)
        return SavableStruct.fromDict(self, wrapper, attrs, instanceCheck)

class EventLoop:
    current = None

    def __init__(self):
        self.threads = []
        self.loops = []
        self.pending = []
        self.updates = []
        self.running = False

    def schedule(self, *funcs, main=False, ups=None):
        if main:
            self.updates.extend(funcs)
        else:
            if ups is None:
                raise PyUnityException("ups argument is required if main is False")

            loop = asyncio.new_event_loop()
            self.loops.append(loop)
            def inner():
                clock = Clock()
                clock.Start(ups)
                while self.running:
                    for func in funcs:
                        func(loop)
                        loop.call_soon(loop.stop)
                        loop.run_forever()
                    clock.Maintain()

            t = threading.Thread(target=inner, daemon=True)
            self.threads.append(t)

    def start(self):
        if EventLoop.current is not None:
            raise PyUnityException("Only one EventLoop can be running")
        EventLoop.current = self

        self.running = True
        for thread in self.threads:
            thread.start()

        while True:
            for func in self.updates:
                func()

            for event in self.pending:
                event.trigger()
            self.pending.clear()

    def quit(self):
        self.running = False
        for thread in self.threads:
            thread.join() # Will wait until this iteration has finished
        self.threads.clear()
        EventLoop.current = None
