__all__ = ["ABCMessage", "ABCException", "ABCMeta",
           "abstractmethod", "abstractproperty"]

import inspect

class ABCException(Exception):
    pass

class ABCMessage(ABCException):
    pass

class abstractmethod:
    def __init__(self, func):
        self.func = func
        self.args = self.getargs(func)

    def __eq__(self, other):
        if isinstance(other, abstractmethod):
            return self.args == other.args
        else:
            return self.args == self.getargs(other)

    def __get__(self, instance, owner):
        return self.func

    @staticmethod
    def getargs(func):
        signature = inspect.signature(func)
        return [(param.name, param.kind) for param in
                signature.parameters.values()]

class abstractproperty(abstractmethod):
    def __eq__(self, other):
        if isinstance(other, property):
            return self.func.__name__ == other.fget.__name__
        return False

class ABCMeta(type):
    _trigger = True
    def __init__(cls, fullname, bases, attrs, message=None):
        super().__init__(fullname, bases, attrs)

        supercls = cls.__bases__[0]
        if supercls is not object:
            methods = {attr: v for attr, v in supercls.__dict__.items()
                       if isinstance(v, abstractmethod)}

            for method in methods:
                if cls._trigger and method not in attrs:
                    try:
                        raise ABCException("Method has not been defined: " +
                                           repr(methods[method].func))
                    except ABCException:
                        if message is not None:
                            raise ABCMessage(message)
                        raise

                if cls._trigger and methods[method] != attrs[method]:
                    try:
                        raise ABCException("Function signature is not the same: " +
                                           repr(methods[method].func) + " and " +
                                           repr(attrs[method]))
                    except ABCException:
                        if message is not None:
                            raise ABCMessage(message)
                        raise

    def __new__(cls, fullname, bases, attrs, message=None):
        return super().__new__(cls, fullname, bases, attrs)
