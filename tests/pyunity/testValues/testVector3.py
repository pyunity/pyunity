## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import Vector3
from . import TestCase, almostEqual
import math

class TestVector3(TestCase):
    def testInit(self):
        v = Vector3()
        assert v.x == 0
        assert v.y == 0
        assert v.z == 0
        assert v == Vector3.zero()
        v = Vector3.one()
        assert v.x == 1
        assert v.y == 1
        assert v.z == 1

    def testEqual(self):
        v = Vector3(1, 2, 3)
        assert v == Vector3(1, 2, 3)
        assert v != Vector3(3, 2, 1)

    def testAdd(self):
        v1 = Vector3(0, 1, 2)
        v2 = Vector3(0, 2, 3)
        assert v1 + v2 == Vector3(0, 3, 5)
        assert v2 + v1 == Vector3(0, 3, 5)
        v1 += v2
        assert v1 == Vector3(0, 3, 5)
        v2 += 2
        assert v2 == Vector3(2, 4, 5)
        assert 1 + Vector3(0, 1, 2) == Vector3(1, 2, 3)

    def testSub(self):
        v1 = Vector3(0, 1, 2)
        v2 = Vector3(0, 2, 3)
        assert v1 - v2 == Vector3(0, -1, -1)
        assert v2 - v1 == Vector3(0, 1, 1)
        v1 -= v2
        assert v1 == Vector3(0, -1, -1)
        v2 -= 2
        assert v2 == Vector3(-2, 0, 1)
        assert 1 - Vector3(0, 1, 2) == Vector3(1, 0, -1)

    def testMul(self):
        v1 = Vector3(0, 1, 2)
        v2 = Vector3(0, 2, 3)
        assert v1 * v2 == Vector3(0, 2, 6)
        assert v2 * v1 == Vector3(0, 2, 6)
        v1 *= v2
        assert v1 == Vector3(0, 2, 6)
        v2 *= 2
        assert v2 == Vector3(0, 4, 6)
        assert 2 * Vector3(0, 1, 2) == Vector3(0, 2, 4)

    def testDivOps(self):
        v1 = Vector3(1, 2, 3)
        v2 = Vector3(1, 4, 12)
        assert v1 / v2 == Vector3(1, 0.5, 0.25)
        assert v2 / v1 == Vector3(1, 2, 4)
        v1 /= v2
        assert v1 == Vector3(1, 0.5, 0.25)
        v2 /= 2
        assert v2 == Vector3(0.5, 2, 6)
        assert 2 / Vector3(1, 2, 3) == Vector3(2.0, 1.0, 2/3)

        v1 = Vector3(1, 2, 3)
        v2 = Vector3(1, 4, 12)
        assert v1 // v2 == Vector3(1, 0, 0)
        assert v2 // v1 == Vector3(1, 2, 4)
        v1 //= v2
        assert v1 == Vector3(1, 0, 0)
        v2 //= 2
        assert v2 == Vector3(0, 2, 6)
        assert 2 // Vector3(1, 2, 3) == Vector3(2, 1, 0)

        with self.assertRaises(ZeroDivisionError):
            v2 / 0

        v1 = Vector3(1, 2, 3)
        v2 = Vector3(1, 4, 12)
        assert v1 % v2 == Vector3(0, 2, 3)
        assert v2 % v1 == Vector3(0, 0, 0)
        v1 %= v2
        assert v1 == Vector3(0, 2, 3)
        v2 %= 2
        assert v2 == Vector3(1, 0, 0)
        assert 2 % Vector3(1, 2, 3) == Vector3(0, 0, 2)

    def testShifts(self):
        v1 = Vector3(2, 3, 4)
        v2 = Vector3(0, 1, 2)
        assert v1 >> v2 == Vector3(2, 1, 1)
        assert v2 >> v1 == Vector3(0, 0, 0)
        v1 >>= v2
        assert v1 == Vector3(2, 1, 1)
        v2 >>= 2
        assert v2 == Vector3(0, 0, 0)
        assert 16 >> Vector3(2, 3, 4) == Vector3(4, 2, 1)

        v1 = Vector3(2, 3, 4)
        v2 = Vector3(0, 1, 2)
        assert v1 << v2 == Vector3(2, 6, 16)
        assert v2 << v1 == Vector3(0, 8, 32)
        v1 <<= v2
        assert v1 == Vector3(2, 6, 16)
        v2 <<= 2
        assert v2 == Vector3(0, 4, 8)
        assert 1 << Vector3(2, 3, 4) == Vector3(4, 8, 16)

    def testBitwise(self):
        v1 = Vector3(2, 3, 4)
        v2 = Vector3(0, 1, 2)
        assert v1 & v2 == Vector3(0, 1, 0)
        assert v2 & v1 == Vector3(0, 1, 0)
        assert 2 & v2 == Vector3(0, 0, 2)
        assert v1 | v2 == Vector3(2, 3, 6)
        assert v2 | v1 == Vector3(2, 3, 6)
        assert 2 | v2 == Vector3(2, 3, 2)
        assert v1 ^ v2 == Vector3(2, 2, 6)
        assert v2 ^ v1 == Vector3(2, 2, 6)
        assert 2 ^ v2 == Vector3(2, 3, 0)

    def testUnary(self):
        v = Vector3(2, -3, 4)
        assert -v == Vector3(-2, 3, -4)
        assert +v == Vector3(2, -3, 4)
        assert ~v == Vector3(-3, 2, -5)

    def testUtilFuncs(self):
        v = Vector3(2, -3, 4)
        assert v == v.copy()
        assert list(v) == [2, -3, 4]
        assert v.abs() == Vector3(2, 3, 4)
        assert abs(v) == math.sqrt(29)
        assert v.getLengthSqrd() == 29
        assert v.length == math.sqrt(29)
        assert almostEqual(v.normalized().length, 1)
