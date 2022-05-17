# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import ImmutableStruct, PyUnityException
from . import TestCase

class Struct(metaclass=ImmutableStruct):
    _names = ["x", "y"]
    x = 5
    y = 6

class TestImmutableStruct(TestCase):
    def testInternalSet(self):
        assert Struct.x == 5
        assert Struct.y == 6
        Struct._set("x", 1)
        assert Struct.x == 1
        with self.assertRaises(PyUnityException) as exc:
            Struct._set("a", 1)
        assert exc.value == "No field named 'a'"

    def testException(self):
        with self.assertRaises(PyUnityException) as exc:
            Struct.x = 1
        assert exc.value == "Field 'x' is read-only"

        with self.assertRaises(PyUnityException) as exc:
            del Struct.x
        assert exc.value == "Field 'x' is read-only"

    def testSetOther(self):
        Struct.n = 5
        del Struct.n
        with self.assertRaises(AttributeError) as exc:
            del Struct.f
        assert exc.value == "f"
