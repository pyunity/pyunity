## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

__all__ = ["ABCException", "ABCMeta", "abstractmethod", "abstractproperty"]

from .other import IncludeMixin
import inspect

class ABCException(Exception):
    pass

class abstractmethod(IncludeMixin):
    def __init__(self, func):
        if not callable(func):
            raise ABCException(f"Function is not callable: {func}")
        self.func = func
        self.args = self.getargs(func)

    def __eq__(self, other):
        if isinstance(other, abstractmethod):
            return self.args == other.args
        else:
            return self.args == self.getargs(other)

    def __get__(self, instance, owner=None):
        return self.func

    @staticmethod
    def getargs(func):
        signature = inspect.signature(func)
        return [(param.name, param.kind) for param in
                signature.parameters.values()]

class abstractproperty(abstractmethod):
    def __get__(self, instance, owner=None):
        if instance is None:
            return self.func
        return self.func(instance)

    def __set__(self, instance, value):
        raise NotImplementedError

    def __eq__(self, other):
        if isinstance(other, property):
            return self.func.__name__ == other.fget.__name__
        return False

class ABCMeta(type):
    _trigger = True

    def __init__(cls, name, bases, attrs, **kwds):
        super(ABCMeta, cls).__init__(name, bases, attrs, **kwds)

        for supercls in cls.__bases__:
            if supercls is object:
                continue
            methods = {attr: v for attr, v in supercls.__dict__.items()
                       if isinstance(v, abstractmethod)}

            for method in methods:
                if cls._trigger and method not in attrs:
                    raise ABCException("Method has not been defined: " +
                                       repr(methods[method].func))

                if cls._trigger and methods[method] != attrs[method]:
                    raise ABCException("Function signature is not the same: " +
                                       repr(methods[method].func) + " and " +
                                       repr(attrs[method]))
