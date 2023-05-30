## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import Color, RGB, HSV
from . import TestCase

class TestColors(TestCase):
    def testFromString(self):
        a = Color.fromString("RGB(127, 0, 255)")
        assert a.r == 127
        assert a.g == 0
        assert a.b == 255
        assert a.toString() == "RGB(127, 0, 255)"

        b = Color.fromString("HSV(180, 50, 75)")
        assert b.h == 180
        assert b.s == 50
        assert b.v == 75
        assert b.toString() == "HSV(180, 50, 75)"

    def testConvert(self):
        a = RGB(127, 0, 255)
        assert a.toRGB() is a

        b = HSV(180, 50, 75)
        assert b.toHSV() is b

class TestRGB(TestCase):
    def testDivMul(self):
        a = RGB(127, 0, 255)
        assert a / 255 == (127/255, 0, 1.0)
        assert a * 2 == (254, 0, 510)
