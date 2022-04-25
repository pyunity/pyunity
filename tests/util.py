__all__ = ["TestCase", "ExceptionContext", "almostEqual"]

import inspect

class TestCase:
    @classmethod
    def __init_subclass__(cls):
        members = inspect.getmembers(cls, inspect.isroutine)
        variables = [a for a in members if not a[0].startswith("__")]
        for name, val in variables:
            if not name.startswith("__"):
                if name not in ["wrap", "setUp", "tearDown", "assertRaises"]:
                    setattr(cls, name, cls.wrap(val))

    @classmethod
    def wrap(cls, func):
        def inner(self):
            self.setUp()
            try:
                func(self)
            finally:
                self.tearDown()
        return inner

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def assertRaises(self, exctype):
        return ExceptionContext(exctype)

class ExceptionContext:
    def __init__(self, exctype):
        self.exctype = exctype
        self.value = ""

    def __enter__(self):
        return self

    def __exit__(self, exctype, excvalue, exctb):
        assert exctype is self.exctype
        self.value = str(excvalue)
        return True

def almostEqual(a, b):
    return round(abs(a - b), 10) == 0
