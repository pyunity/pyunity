## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import GameObject, Vector3
from . import TestCase, almostEqual

class TestTransform(TestCase):
    def testTransformPosition(self):
        gameObject = GameObject()
        gameObject2 = GameObject("GameObject2", gameObject)
        assert gameObject2.transform.parent.gameObject is gameObject
        gameObject.transform.position = Vector3(0, 1, 0)
        assert gameObject.transform.localPosition == Vector3(0, 1, 0)

        transform = gameObject2.transform
        transform.position = Vector3(0, 0, 0)
        assert transform.localPosition == Vector3(0, -1, 0)
        assert transform.position == Vector3(0, 0, 0)
        gameObject.transform.position = Vector3(0, 0, 1)
        assert transform.localPosition == Vector3(0, -1, 0)
        assert transform.position == Vector3(0, -1, 1)

    def testTransformScale(self):
        gameObject = GameObject()
        gameObject2 = GameObject("GameObject2", gameObject)
        transform = gameObject2.transform

        gameObject.transform.scale = Vector3(1, 0.5, 3)
        assert gameObject.transform.localScale == Vector3(1, 0.5, 3)
        transform.scale = Vector3(2, 1, 0.5)
        assert almostEqual(transform.localScale, Vector3(2, 2, 1 / 6))
        gameObject.transform.scale = Vector3(3, 2, 0.5)
        assert gameObject.transform.localScale == Vector3(3, 2, 0.5)
        assert almostEqual(transform.localScale, Vector3(2, 2, 1 / 6))
        assert almostEqual(transform.scale, Vector3(6, 4, 1 / 12))
