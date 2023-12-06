## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

__all__ = ["Clock", "IgnoredMixin", "ImmutableStruct", "IncludeInstanceMixin",
           "IncludeMixin", "LockedLiteral", "ModuleExportControlMixin",
           "SavableStruct", "StructEntry"]

from .. import config
from ..errors import PyUnityException
from functools import partial
import sys
import time

class ModuleExportControlMixin:
    # Used by various helper scripts.
    pass

class IgnoredMixin(ModuleExportControlMixin):
    # Used by various helper scripts.
    pass

class IncludeMixin(ModuleExportControlMixin):
    # Used by various helper scripts.
    pass

class IncludeInstanceMixin(ModuleExportControlMixin):
    # Used by various helper scripts.
    pass

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
        self._start = time.perf_counter()

    def Maintain(self):
        self._end = time.perf_counter()
        elapsedMS = self._end - self._start
        if config.vsync or self.fps == 0:
            sleep = 0.001
        else:
            sleep = self._frameDuration - elapsedMS
        if sleep <= 0:
            self._start = time.perf_counter()
            return sys.float_info.epsilon
        time.sleep(sleep)
        self._start = time.perf_counter()
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
        factory = self.factoryWrapper(factory)
        return factory(*attrs.values())

    def factoryWrapper(self, factory):
        return factory

    def __call__(self, cls):
        def __init__(obj, *args, **kwargs):
            argmap = {}
            keys = self.attrs.keys()
            for i, val in args:
                attr = keys[i]
                argmap[attr] = val

            for attr, val in kwargs.items():
                if attr in argmap:
                    raise ValueError(
                        f"{cls.__name__}() got multiple values for argument {attr!r}")
                argmap[attr] = val

            for key in keys:
                if key not in argmap:
                    if self.attrs[key].required:
                        raise PyUnityException(f"Missing required argument: {key!r}")
                    if self.attrs[key].default is not StructEntry.ignore:
                        argmap[key] = self.attrs[key].default

            for k, v in argmap.items():
                setattr(obj, k, v)

        if hasattr(cls, "_factoryWrapper"):
            self.factoryWrapper = cls._factoryWrapper

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
        super(ImmutableStruct, self).__setattr__(name, value)

    def __delattr__(self, name):
        if name in self._names:
            raise PyUnityException(f"Field {name!r} is read-only")
        super(ImmutableStruct, self).__delattr__(name)

    def _set(self, name, value):
        if name not in self._names:
            raise PyUnityException(f"No field named {name!r}")
        super(ImmutableStruct, self).__setattr__(name, value)
