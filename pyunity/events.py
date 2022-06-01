__all__ = ["Event"]

from .errors import PyUnityException
from .core import Component, GameObject
from .values import SavableStruct, StructEntry, Clock
from . import config
from functools import wraps, update_wrapper
import threading

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

    def trigger(self):
        self.func(*self.args, **self.kwargs)

    def callSoon(self):
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
        self.pending = []
        self.updates = []
        self.running = False
        self.clock = Clock()

    def schedule(self, func, main=False):
        if main:
            self.updates.append(func)
        else:
            @wraps(func)
            def inner():
                while self.running:
                    func()
                    self.clock.Maintain()

            t = threading.Thread(target=inner, daemon=True)
            self.threads.append(t)

    def start(self):
        if EventLoop.current is not None:
            raise PyUnityException("Only one EventLoop can be running")
        EventLoop.current = self

        self.clock.Start(config.fps)
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
