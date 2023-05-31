## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

import math
from pyunity import Quaternion, Vector3
from . import TestCase, almostEqual

sqrt2 = math.sqrt(2) / 2

class TestQuaternion(TestCase):
    def testInit(self):
        q = Quaternion.identity()
        assert q.x == 0
        assert q.y == 0
        assert q.z == 0
        assert q.w == 1
        assert q == Quaternion(1, 0, 0, 0)

    def testEulerAngles(self):
        q = Quaternion.Euler(Vector3(0, 90, 0))
        assert almostEqual(q, Quaternion(sqrt2, 0, sqrt2, 0))
        q = Quaternion.Euler(Vector3(180, 0, 0))
        assert almostEqual(q, Quaternion(0, 1, 0, 0))

    def testFromDir(self):
        q = Quaternion.FromDir(Vector3(0, 0, 1))
        assert q == Quaternion.identity()
        q = Quaternion.FromDir(Vector3(0, 0, -1))
        assert almostEqual(q, Quaternion(0, 0, 1, 0))
        q = Quaternion.FromDir(Vector3(0, 0, 0))
        assert q == Quaternion.identity()

    def testRotateVector(self):
        q = Quaternion.Euler(Vector3(0, 90, 0))
        assert almostEqual(
            q.RotateVector(Vector3(0, 0, 1)),
            Vector3(1, 0, 0))
        q = Quaternion.Euler(Vector3(90, 0, 0))
        assert almostEqual(
            q.RotateVector(Vector3(0, 0, 1)),
            Vector3(0, -1, 0))
        q = Quaternion.Euler(Vector3(0, 0, 45))
        assert almostEqual(
            q.RotateVector(Vector3(0, 1, 0)),
            Vector3(-sqrt2, sqrt2, 0))
