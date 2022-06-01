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

    def __call__(self):
        self.func(*self.args, **self.kwargs)

    def _fromDict(self, factory, attrs, instanceCheck=None):
        def wrapper(component, method, args=(), kwargs={}):
            func = getattr(component, method)
            return factory(func, args, kwargs)
        return SavableStruct.fromDict(self, wrapper, attrs, instanceCheck)

class EventLoop:
    def __init__(self):
        self.funcs = []
        self.threads = []
        self.running = False
        self.clock = Clock()

    def schedule(self, func, repeat=False):
        @wraps(func)
        def inner():
            while self.running:
                func()
                self.clock.Maintain()

        self.funcs.append(func)
        t = threading.Thread(target=inner, daemon=True)
        self.threads.append(t)

    def start(self, *updates):
        self.clock.Start(config.fps)
        self.running = True
        for thread in self.threads:
            thread.start()

        while True:
            for updateFunc in updates:
                updateFunc()
