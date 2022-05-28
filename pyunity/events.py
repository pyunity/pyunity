__all__ = ["Event"]

from .errors import PyUnityException
from .core import Component
from functools import update_wrapper

class Event:
    def __init__(self, func, args, kwargs):
        if not hasattr(func, "__self__"):
            raise PyUnityException(
                "Cannot create event from callback that is not attached to a Component")
        if not issubclass(func.__self__, Component):
            raise PyUnityException(
                "Cannot create event from callback that is not attached to a Component")
        if not isinstance(func.__self__.gameObject):
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
