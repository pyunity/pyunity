__all__ = ["Clock", "ImmutableStruct"]

import time
import sys
from ..errors import PyUnityException

class Clock:
    def __init__(self):
        self._fps = 60
        self._frameDuration = 1 / self._fps

    @property
    def fps(self):
        return self._fps

    @fps.setter
    def fps(self, value):
        self._fps = value
        self._frameDuration = 1 / self._fps

    def Start(self, fps=None):
        if fps is not None:
            self.fps = fps
        self._start = time.time()

    def Maintain(self):
        self._end = time.time()
        elapsedMS = self._end - self._start
        sleep = self._frameDuration - elapsedMS - 0.001
        if sleep <= 0:
            self._start = time.time()
            return sys.float_info.epsilon
        time.sleep(sleep)
        self._start = time.time()
        return sleep

class ImmutableStruct(type):
    def __setattr__(self, name, value):
        if name in self._names:
            raise PyUnityException(f"Property {name!r} is read-only")
        super().__setattr__(name, value)

    def __delattr__(self, name):
        if name in self._names:
            raise PyUnityException(f"Property {name!r} is read-only")
        super().__delattr__(name)

    def _set(self, name, value):
        super().__setattr__(name, value)
