## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import HideInInspector, PyUnityException, Transform
from . import TestCase

class TestHideInInspector(TestCase):
    def testFromString(self):
        h = HideInInspector("Transform")
        assert h.type is Transform

        with self.assertRaises(PyUnityException) as exc:
            HideInInspector("WrongName")
        assert exc.value == "No type named 'WrongName'"
