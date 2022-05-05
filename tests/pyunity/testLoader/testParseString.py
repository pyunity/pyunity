from pyunity import Loader, Vector2, Vector3, Quaternion, RGB, HSV
from . import TestCase

class TestParseString(TestCase):
    def testParse(self):
        valid, vector = Loader.parseString("Vector2(0, 0)")
        assert valid
        assert isinstance(vector, Vector2)
        assert vector == Vector2(0, 0)

        valid, vector = Loader.parseString("Vector3(0, 0, 0)")
        assert valid
        assert isinstance(vector, Vector3)
        assert vector == Vector3(0, 0, 0)

        valid, quat = Loader.parseString("Quaternion(0, 0, 0, 0)")
        assert valid
        assert isinstance(quat, Quaternion)
        assert quat == Quaternion(0, 0, 0, 0)

        valid, clr = Loader.parseString("RGB(0, 0, 0)")
        assert valid
        assert isinstance(clr, RGB)
        assert clr == RGB(0, 0, 0)

        valid, clr = Loader.parseString("HSV(0, 0, 0)")
        assert valid
        assert isinstance(clr, HSV)
        assert clr == HSV(0, 0, 0)

        valid, boolean = Loader.parseString("True")
        assert valid
        assert isinstance(boolean, bool)
        assert boolean

        valid, boolean = Loader.parseString("False")
        assert valid
        assert isinstance(boolean, bool)
        assert not boolean

        valid, integer = Loader.parseString("0")
        assert valid
        assert isinstance(integer, int)
        assert integer == 0

        valid, floating_point = Loader.parseString("0.0")
        assert valid
        assert isinstance(floating_point, float)
        assert floating_point == 0.0

        valid, string = Loader.parseString("\"Hello World!\"")
        assert valid
        assert isinstance(string, str)
        assert string == "Hello World!"

        valid, tupleobj = Loader.parseString("(0.0, True)")
        assert valid
        assert isinstance(tupleobj, tuple)
        assert tupleobj == (0.0, True)

        valid, listobj = Loader.parseString("[0.0, True]")
        assert valid
        assert isinstance(listobj, list)
        assert listobj == [0.0, True]
