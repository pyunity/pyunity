# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

__all__ = ["Clock", "ImmutableStruct", "SavableStruct", "StructEntry", "LockedLiteral"]

import time
import sys
from functools import partial
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
        if value == 0:
            self._frameDuration = 0
        else:
            self._frameDuration = 1 / self._fps

    def Start(self, fps=None):
        if fps is not None:
            self.fps = fps
        self._start = time.time()

    def Maintain(self):
        from .. import config
        self._end = time.time()
        elapsedMS = self._end - self._start
        if config.vsync:
            sleep = 0
        else:
            sleep = self._frameDuration - elapsedMS
        if sleep <= 0:
            self._start = time.time()
            return sys.float_info.epsilon
        time.sleep(sleep)
        self._start = time.time()
        return sleep

class LockedLiteral:
    def _lock(self):
        super(LockedLiteral, self).__setattr__("_locked", True)

    def __setattr__(self, name, value):
        if getattr(self, "_locked", False):
            raise AttributeError(
                f"Cannot change attribute of immutable "
                f"{type(self).__name__!r} object")
        super(LockedLiteral, self).__setattr__(name, value)

    def __delattr__(self, name):
        if getattr(self, "_locked", False):
            raise AttributeError(
                f"Cannot change attribute of immutable "
                f"{type(self).__name__!r} object")
        super(LockedLiteral, self).__delattr__(name)

class SavableStruct:
    def __init__(self, **kwargs):
        self.attrs = kwargs

    def fromDict(self, factory, attrs, instanceCheck=None):
        for key, value in attrs.items():
            if key not in self.attrs:
                raise PyUnityException(
                    f"Invalid field name: {key!r}")
            if instanceCheck is not None:
                type_, value = instanceCheck(self.attrs[key].type, value)
                attrs[key] = value
            else:
                type_ = self.attrs[key].type
            if not isinstance(value, type_):
                raise PyUnityException(
                    f"Invalid type for field {key!r}: expected "
                    f"{self.attrs[key].type.__name__}, got {type(value).__name__}")

        for key in self.attrs:
            if key not in attrs:
                if self.attrs[key].default is not StructEntry.ignore:
                    attrs[key] = self.attrs[key].default

        newAttrs = {}
        for key in self.attrs:
            if key in attrs:
                newAttrs[key] = attrs[key]
            elif self.attrs[key].default is not StructEntry.ignore:
                newAttrs[key] = self.attrs[key].default
            elif self.attrs[key].required:
                raise PyUnityException(f"Missing required field: {key!r}")
        return factory(*attrs.values())

    def __call__(self, cls):
        def __init__(*args, **kwargs):
            argmap = {}
            keys = self._attrs.keys()
            for i, val in args:
                attr = keys[i]
                argmap[attr] = val

            for attr, val in kwargs.items():
                if attr in argmap:
                    raise ValueError(
                        f"{self.__class__.__name__}() got multiple values for argument {attr!r}")
                argmap[attr] = val

            for key in keys:
                if key not in argmap:
                    if self._attrs[key].required:
                        raise PyUnityException(f"Missing required argument: {key!r}")
                    if self._attrs[key].default is not StructEntry.ignore:
                        argmap[key] = self._attrs[key].default

            for k, v in argmap.items():
                setattr(self, k, v)

        if hasattr(cls, "_fromDict"):
            self.fromDict = partial(cls._fromDict, self)

        if cls.__init__ is object.__init__:
            cls.__init__ = __init__
        cls._wrapper = self
        return cls

class StructEntry:
    class _ignoredEntry:
        pass

    ignore = _ignoredEntry()

    def __init__(self, type, default=ignore, required=False):
        self.type = type
        self.default = default
        self.required = required

class ImmutableStruct(type):
    _names = []
    def __setattr__(self, name, value):
        if name in self._names:
            raise PyUnityException(f"Field {name!r} is read-only")
        super().__setattr__(name, value)

    def __delattr__(self, name):
        if name in self._names:
            raise PyUnityException(f"Field {name!r} is read-only")
        super().__delattr__(name)

    def _set(self, name, value):
        if name not in self._names:
            raise PyUnityException(f"No field named {name!r}")
        super().__setattr__(name, value)
