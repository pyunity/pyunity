from pyunity import (
    HideInInspector, Transform, PyUnityException)
from . import TestCase

class TestHideInInspector(TestCase):
    def testFromString(self):
        h = HideInInspector("Transform")
        assert h.type is Transform

        with self.assertRaises(PyUnityException) as exc:
            HideInInspector("WrongName")
        assert exc.value == "No type named 'WrongName'"
