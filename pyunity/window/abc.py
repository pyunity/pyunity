import inspect

class ABCException(Exception):
    pass

class ABCMessage(ABCException):
    pass

class abstractmethod:
    def __init__(self, func):
        if not isinstance(func, type(self.__class__.__call__)):
            raise ABCException("Provided function is not callable")
        self.func = func
        self.args = self.getargs(func)

    def __eq__(self, other):
        if inspect.isfunction(other):
            return self.args == self.getargs(other)
        elif isinstance(other, abstractmethod):
            return self.args == other.args
        return False

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __repr__(self):
        return repr(self.func)

    @staticmethod
    def getargs(func):
        signature = inspect.signature(func)
        return [(param.name, param.kind) for param in
                signature.parameters.values()]

class ABCMeta(type):
    def __init__(cls, fullname, bases, attrs, message=None):
        super().__init__(fullname, bases, attrs)

        supercls = cls.__bases__[0]
        if supercls is not object:
            methods = {attr: v for attr, v in supercls.__dict__.items()
                       if isinstance(v, abstractmethod)}

            for method in methods:
                if method not in attrs:
                    try:
                        raise ABCException("Method has not been defined: " +
                                           repr(methods[method]))
                    except ABCException:
                        if message is not None:
                            raise ABCMessage(message)
                if methods[method] != attrs[method]:
                    try:
                        raise ABCException("Function signature is not the same: " +
                                           repr(methods[method]) + " and " +
                                           repr(attrs[method]))
                    except ABCException:
                        if message is not None:
                            raise ABCMessage(message)

    def __new__(cls, fullname, bases, attrs, message=None):
        return super().__new__(cls, fullname, bases, attrs)

class ABCWindow(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, name, resize):
        pass

    @abstractmethod
    def get_mouse(self, mousecode, keystate):
        pass

    @abstractmethod
    def get_key(self, keycode, keystate):
        pass

    @abstractmethod
    def get_mouse_pos(self):
        pass

    @abstractmethod
    def quit(self):
        pass

    @abstractmethod
    def start(self, update_func):
        pass
