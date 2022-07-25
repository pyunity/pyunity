## Copyright (c) 2020-2022 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import ABCMeta, abstractmethod, abstractproperty, ABCException, ABCMessage
from . import TestCase

class TestAbstractmethod(TestCase):
    def testInit(self):
        class ABCTest(metaclass=ABCMeta):
            @abstractmethod
            def meth(self):
                pass

        assert ABCTest.meth.__name__ == "meth"

        with self.assertRaises(ABCException) as exc:
            abstractmethod(1)
        assert exc.value == "Function is not callable: 1"

class TestAbstractproperty(TestCase):
    def testInit(self):
        class ABCTest(metaclass=ABCMeta):
            @abstractproperty
            def prop(self):
                pass

        assert ABCTest.prop.__name__ == "prop"
        assert ABCTest().prop is None

class ABCTest(metaclass=ABCMeta):
    @abstractmethod
    def meth(self):
        pass

    @abstractproperty
    def prop(self):
        pass

class TestABCMeta(TestCase):
    def testCreate(self):
        class ABCSub(ABCTest):
            def meth(self):
                return 5

            @property
            def prop(self):
                return 2

        assert ABCSub is not None

    def testError(self):
        with self.assertRaises(ABCException) as exc:
            class ABCSub(ABCTest):
                def meth(self):
                    return 5
            ABCSub().meth()
        assert exc.value.startswith("Method has not been defined: ")

        with self.assertRaises(ABCException) as exc:
            class ABCSub(ABCTest):
                def meth(self, a):
                    return 5
            ABCSub().meth(1)
        assert exc.value.startswith("Function signature is not the same: ")

        with self.assertRaises(ABCMessage) as exc:
            class ABCSub(ABCTest, message="error message"):
                def meth(self):
                    return 5
        assert exc.value == "error message"
