## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import RectAnchors, RectData, RectOffset, Vector2
from . import TestCase

class TestRectData(TestCase):
    def testInit(self):
        d = RectData()
        assert d.min == Vector2.zero()
        assert d.max == Vector2.zero()

        d = RectData(Vector2.one())
        assert d.min == Vector2.one()
        assert d.max == Vector2.one()

        assert d == RectData(d)

        d = RectData(Vector2.one(), Vector2(2, 2))
        assert d.min == Vector2.one()
        assert d.max == Vector2(2, 2)

        assert d.size() == Vector2(1, 1)

    def testOps(self):
        a = RectData()
        b = RectData(Vector2.one())
        assert a + b == RectData(Vector2.one())
        assert b - a == RectData(Vector2.one())
        assert a + Vector2.one() == b
        assert b - Vector2.one() == a

class TestRectAnchors(TestCase):
    def testInit(self):
        a = RectAnchors(Vector2.zero(), Vector2(0.5, 0.5))
        assert a.max == Vector2(0.5, 0.5)
        a.SetPoint(Vector2(1, 1))
        assert a.min == Vector2(1, 1)
        assert a.max == Vector2(1, 1)

    def testRelativeTo(self):
        a = RectAnchors(Vector2(0.25, 0.25), Vector2(0.75, 0.75))
        b = RectAnchors(Vector2(0, 0), Vector2(0.5, 0.5))
        assert a.RelativeTo(b) == RectAnchors(Vector2(0.125, 0.125), Vector2(0.375, 0.375))

class TestRectOffset(TestCase):
    def testCreate(self):
        a = RectOffset.Rectangle(Vector2(800, 500), Vector2(200, 200))
        assert a.min == Vector2(-200, -50)
        assert a.max == Vector2(600, 450)

    def testSet(self):
        a = RectOffset()
        a.Move(Vector2(400, 250))
        assert a.min == Vector2(400, 250)
        assert a.max == Vector2(400, 250)

        a.max = Vector2(500, 350)
        a.SetCenter(Vector2.zero())
        assert a.min == Vector2(-50, -50)
        assert a.max == Vector2(50, 50)
