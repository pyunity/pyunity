class abstractmethod:
    def __init__(self, func):
        self.func = func
    
    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

class ABCMeta(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        
        supercls = cls.__bases__[0]
        if supercls is not object:
            superattrs = supercls.__dict__
            methods = {attr: v for attr, v in superattrs.items()
                if isinstance(v, abstractmethod)}
            
            for method in methods:
                if method not in attrs:
                    raise Exception("Method has not been defined: " + \
                        repr(method))

class ABCWindow(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, name, resize):
        pass
