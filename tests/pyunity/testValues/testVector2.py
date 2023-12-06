## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import Vector2
from . import TestCase, almostEqual
import math

class TestVector2(TestCase):
    def testInit(self):
        v = Vector2()
        assert v.x == 0
        assert v.y == 0
        assert v == Vector2.zero()
        v = Vector2.one()
        assert v.x == 1
        assert v.y == 1

    def testEqual(self):
        v = Vector2(1, 2)
        assert v == Vector2(1, 2)
        assert v != Vector2(3, 1)

    def testAdd(self):
        v1 = Vector2(0, 1)
        v2 = Vector2(2, 3)
        assert v1 + v2 == Vector2(2, 4)
        assert v2 + v1 == Vector2(2, 4)
        v1 += v2
        assert v1 == Vector2(2, 4)
        v2 += 2
        assert v2 == Vector2(4, 5)
        assert 1 + Vector2(0, 1) == Vector2(1, 2)

    def testSub(self):
        v1 = Vector2(0, 1)
        v2 = Vector2(2, 3)
        assert v1 - v2 == Vector2(-2, -2)
        assert v2 - v1 == Vector2(2, 2)
        v1 -= v2
        assert v1 == Vector2(-2, -2)
        v2 -= 2
        assert v2 == Vector2(0, 1)
        assert 1 - Vector2(0, 1) == Vector2(1, 0)

    def testMul(self):
        v1 = Vector2(2, 3)
        v2 = Vector2(5, 4)
        assert v1 * v2 == Vector2(10, 12)
        assert v2 * v1 == Vector2(10, 12)
        v1 *= v2
        assert v1 == Vector2(10, 12)
        v2 *= 2
        assert v2 == Vector2(10, 8)
        assert 2 * Vector2(2, 3) == Vector2(4, 6)

    def testDivOps(self):
        v1 = Vector2(2, 3)
        v2 = Vector2(5, 4)
        assert v1 / v2 == Vector2(0.4, 0.75)
        assert v2 / v1 == Vector2(2.5, 4/3)
        v1 /= v2
        assert v1 == Vector2(0.4, 0.75)
        v2 /= 2
        assert v2 == Vector2(2.5, 2)
        assert 2 / Vector2(2, 3) == Vector2(1.0, 2/3)

        v1 = Vector2(2, 3)
        v2 = Vector2(4, 12)
        assert v1 // v2 == Vector2(0, 0)
        assert v2 // v1 == Vector2(2, 4)
        v1 //= v2
        assert v1 == Vector2(0, 0)
        v2 //= 2
        assert v2 == Vector2(2, 6)
        assert 2 // Vector2(2, 3) == Vector2(1, 0)

        with self.assertRaises(ZeroDivisionError):
            v2 / 0

        v1 = Vector2(2, 3)
        v2 = Vector2(4, 12)
        assert v1 % v2 == Vector2(2, 3)
        assert v2 % v1 == Vector2(0, 0)
        v1 %= v2
        assert v1 == Vector2(2, 3)
        v2 %= 2
        assert v2 == Vector2(0, 0)
        assert 2 % Vector2(2, 3) == Vector2(0, 2)

    def testShifts(self):
        v1 = Vector2(2, 3)
        v2 = Vector2(0, 1)
        assert v1 >> v2 == Vector2(2, 1)
        assert v2 >> v1 == Vector2(0, 0)
        v1 >>= v2
        assert v1 == Vector2(2, 1)
        v2 >>= 2
        assert v2 == Vector2(0, 0)
        assert 16 >> Vector2(2, 3) == Vector2(4, 2)

        v1 = Vector2(2, 3)
        v2 = Vector2(0, 1)
        assert v1 << v2 == Vector2(2, 6)
        assert v2 << v1 == Vector2(0, 8)
        v1 <<= v2
        assert v1 == Vector2(2, 6)
        v2 <<= 2
        assert v2 == Vector2(0, 4)
        assert 1 << Vector2(2, 3) == Vector2(4, 8)

    def testBitwise(self):
        v1 = Vector2(3, 4)
        v2 = Vector2(1, 2)
        assert v1 & v2 == Vector2(1, 0)
        assert v2 & v1 == Vector2(1, 0)
        assert 2 & v2 == Vector2(0, 2)
        assert v1 | v2 == Vector2(3, 6)
        assert v2 | v1 == Vector2(3, 6)
        assert 2 | v2 == Vector2(3, 2)
        assert v1 ^ v2 == Vector2(2, 6)
        assert v2 ^ v1 == Vector2(2, 6)
        assert 2 ^ v2 == Vector2(3, 0)

    def testUnary(self):
        v = Vector2(-3, 4)
        assert -v == Vector2(3, -4)
        assert +v == Vector2(-3, 4)
        assert ~v == Vector2(2, -5)

    def testUtilFuncs(self):
        v = Vector2(2, -3)
        assert v == v.copy()
        assert list(v) == [2, -3]
        assert v.abs() == Vector2(2, 3)
        assert abs(v) == math.sqrt(13)
        assert v.getLengthSqrd() == 13
        assert v.length == math.sqrt(13)
        assert almostEqual(v.normalized().length, 1)
