## Copyright (c) 2020-2022 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

import math
from . import TestCase, almostEqual
from pyunity import Mathf

class TestFunctions(TestCase):
    def testClamp(self):
        assert Mathf.Clamp(0.5, 0, 1) == 0.5
        assert Mathf.Clamp(0, 0, 1) == 0
        assert Mathf.Clamp(2, 0, 1) == 1
        assert Mathf.Clamp01(3) == 1
        assert Mathf.Clamp01(-3) == 0
        assert Mathf.Clamp01(0.25) == 0.25

    def testDeltaAngle(self):
        assert Mathf.DeltaAngle(-50, 365) == 55

    def testInverseLerp(self):
        assert Mathf.InverseLerp(0.5, 0, 2) == 0.25
        assert Mathf.InverseLerp(-1, 2, 3) == 0

    def testLerp(self):
        assert Mathf.Lerp(0.5, 0, 2) == 1
        assert Mathf.Lerp(2, 2, 3) == 3
        assert Mathf.LerpUnclamped(2, 2, 3) == 4

    def testSign(self):
        assert Mathf.Sign(-2) == -1
        assert Mathf.Sign(6) == 1
        assert Mathf.Sign(0) == 0

    def testSmoothStep(self):
        assert almostEqual(Mathf.SmoothStep(0.5), 0.5)
        assert Mathf.SmoothStep(0) == 0
        assert Mathf.SmoothStep(1) == 1

    def testSmoothDamp(self):
        damper = Mathf.SmoothDamper(0.1)
        damper.SmoothDamp(0, 10, 3, 0.1) # only for coverage
