import unittest
from unittest.mock import Mock
import sys
import math
import os
if "full" not in os.environ:
    sys.modules["sdl2"] = Mock()
    sys.modules["sdl2.sdlmixer"] = Mock()
    sys.modules["sdl2.ext"] = Mock()
    sys.modules["sdl2.video"] = Mock()
    sys.modules["glfw"] = Mock()
    sys.modules["glm"] = math
    sys.modules["PIL"] = Mock()
    sys.modules["OpenGL"] = Mock()
    sys.modules["OpenGL.GL"] = Mock()
    sys.modules["OpenGL.GLUT"] = Mock()
    os.environ["PYUNITY_TESTING"] = "1"

from pyunity import *

class TestGameObject(unittest.TestCase):
    def test_gameobject_name(self):
        gameObject = GameObject()
        self.assertEqual(gameObject.name, "GameObject")

    def test_gameobject_tag(self):
        gameObject = GameObject()
        self.assertEqual(gameObject.tag.tag, 0)
        self.assertEqual(gameObject.tag.tagName, "Default")

    def test_gameobject_transform(self):
        gameObject = GameObject()
        gameObject2 = GameObject("GameObject2", gameObject)
        self.assertIsInstance(gameObject.transform, Transform)
        self.assertIsInstance(gameObject2.transform, Transform)
        self.assertIs(gameObject2.transform.parent, gameObject.transform)
        self.assertIsNone(gameObject.transform.parent)
        self.assertEqual(
            gameObject2.transform.parent.gameObject.name, "GameObject")
        self.assertEqual(len(gameObject.transform.children), 1)
        self.assertEqual(len(gameObject2.transform.children), 0)

    def test_gameobject_component(self):
        gameObject = GameObject()
        self.assertIsInstance(gameObject.transform, Transform)
        self.assertEqual(len(gameObject.components), 1)
        component = gameObject.AddComponent(Component)
        self.assertIsInstance(component, Component)
        self.assertEqual(len(gameObject.components), 2)
        self.assertIs(gameObject.GetComponent(Transform), gameObject.transform)
        with self.assertRaises(ComponentException) as exception_context:
            gameObject.AddComponent(Transform)
        self.assertEqual(str(exception_context.exception),
                         "Cannot add Transform to the GameObject; it already has one")
    
    def test_gameobject_position(self):
        gameObject = GameObject()
        gameObject2 = GameObject("GameObject2", gameObject)
        self.assertIs(gameObject2.transform.parent.gameObject, gameObject)
        gameObject.transform.position = Vector3(0, 1, 0)
        self.assertEqual(gameObject.transform.localPosition, Vector3(0, 1, 0))

        transform = gameObject2.transform
        transform.position = Vector3(0, 0, 0)
        self.assertEqual(transform.localPosition, Vector3(0, -1, 0))
        self.assertEqual(transform.position, Vector3(0, 0, 0))
        gameObject.transform.position = Vector3(0, 0, 1)
        self.assertEqual(transform.localPosition, Vector3(0, -1, 0))
        self.assertEqual(transform.position, Vector3(0, -1, 1))

    def test_gameobject_scale(self):
        gameObject = GameObject()
        gameObject2 = GameObject("GameObject2", gameObject)
        transform = gameObject2.transform

        gameObject.transform.scale = Vector3(1, 0.5, 3)
        self.assertEqual(gameObject.transform.localScale, Vector3(1, 0.5, 3))
        transform.scale = Vector3(2, 1, 0.5)
        self.assertAlmostEqual(transform.localScale, Vector3(2, 2, 1 / 6))
        gameObject.transform.scale = Vector3(3, 2, 0.5)
        self.assertEqual(gameObject.transform.localScale, Vector3(3, 2, 0.5))
        self.assertAlmostEqual(transform.localScale, Vector3(2, 2, 1 / 6))
        self.assertAlmostEqual(transform.scale, Vector3(6, 4, 1 / 12))

class TestVector3(unittest.TestCase):
    def test_init(self):
        v = Vector3()
        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, 0)
        self.assertEqual(v.z, 0)
        self.assertEqual(v, Vector3.zero())
        v = Vector3.one()
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 1)
        self.assertEqual(v.z, 1)

    def test_add(self):
        v1 = Vector3(0, 1, 2)
        v2 = Vector3(0, 2, 3)
        self.assertEqual(v1 + v2, Vector3(0, 3, 5))
        self.assertEqual(v2 + v1, Vector3(0, 3, 5))
        v1 += v2
        self.assertEqual(v1, Vector3(0, 3, 5))
        v2 += 2
        self.assertEqual(v2, Vector3(2, 4, 5))

    def test_sub(self):
        v1 = Vector3(0, 1, 2)
        v2 = Vector3(0, 2, 3)
        self.assertEqual(v1 - v2, Vector3(0, -1, -1))
        self.assertEqual(v2 - v1, Vector3(0, 1, 1))
        v1 -= v2
        self.assertEqual(v1, Vector3(0, -1, -1))
        v2 -= 2
        self.assertEqual(v2, Vector3(-2, 0, 1))

    def test_mul(self):
        v1 = Vector3(0, 1, 2)
        v2 = Vector3(0, 2, 3)
        self.assertEqual(v1 * v2, Vector3(0, 2, 6))
        self.assertEqual(v2 * v1, Vector3(0, 2, 6))
        v1 *= v2
        self.assertEqual(v1, Vector3(0, 2, 6))
        v2 *= 2
        self.assertEqual(v2, Vector3(0, 4, 6))

    def test_div_ops(self):
        v1 = Vector3(1, 2, 3)
        v2 = Vector3(1, 4, 12)
        self.assertEqual(v1 / v2, Vector3(1, 0.5, 0.25))
        self.assertEqual(v2 / v1, Vector3(1, 2, 4))
        v1 /= v2
        self.assertEqual(v1, Vector3(1, 0.5, 0.25))
        v2 /= 2
        self.assertEqual(v2, Vector3(0.5, 2, 6))

        v1 = Vector3(1, 2, 3)
        v2 = Vector3(1, 4, 12)
        self.assertEqual(v1 // v2, Vector3(1, 0, 0))
        self.assertEqual(v2 // v1, Vector3(1, 2, 4))
        v1 //= v2
        self.assertEqual(v1, Vector3(1, 0, 0))
        v2 //= 2
        self.assertEqual(v2, Vector3(0, 2, 6))

        with self.assertRaises(ZeroDivisionError):
            v2 / 0

        v1 = Vector3(1, 2, 3)
        v2 = Vector3(1, 4, 12)
        self.assertEqual(v1 % v2, Vector3(0, 2, 3))
        self.assertEqual(v2 % v1, Vector3(0, 0, 0))
        v1 %= v2
        self.assertEqual(v1, Vector3(0, 2, 3))
        v2 %= 2
        self.assertEqual(v2, Vector3(1, 0, 0))

    def test_shifts(self):
        v1 = Vector3(2, 3, 4)
        v2 = Vector3(0, 1, 2)
        self.assertEqual(v1 >> v2, Vector3(2, 1, 1))
        self.assertEqual(v2 >> v1, Vector3(0, 0, 0))
        v1 >>= v2
        self.assertEqual(v1, Vector3(2, 1, 1))
        v2 >>= 2
        self.assertEqual(v2, Vector3(0, 0, 0))

        v1 = Vector3(2, 3, 4)
        v2 = Vector3(0, 1, 2)
        self.assertEqual(v1 << v2, Vector3(2, 6, 16))
        self.assertEqual(v2 << v1, Vector3(0, 8, 32))
        v1 <<= v2
        self.assertEqual(v1, Vector3(2, 6, 16))
        v2 <<= 2
        self.assertEqual(v2, Vector3(0, 4, 8))

    def test_bitwise(self):
        v1 = Vector3(2, 3, 4)
        v2 = Vector3(0, 1, 2)
        self.assertEqual(v1 & v2, Vector3(0, 1, 0))
        self.assertEqual(v2 & v1, Vector3(0, 1, 0))
        self.assertEqual(v1 | v2, Vector3(2, 3, 6))
        self.assertEqual(v2 | v1, Vector3(2, 3, 6))
        self.assertEqual(v1 ^ v2, Vector3(2, 2, 6))
        self.assertEqual(v2 ^ v1, Vector3(2, 2, 6))

    def test_unary(self):
        v = Vector3(2, -3, 4)
        self.assertEqual(-v, Vector3(-2, 3, -4))
        self.assertEqual(+v, Vector3(2, -3, 4))
        self.assertEqual(~v, Vector3(-3, 2, -5))

    def test_util_funcs(self):
        v = Vector3(2, -3, 4)
        self.assertEqual(v, v.copy())
        self.assertEqual(v.get_length_sqrd(), 29)
        self.assertEqual(v.length, math.sqrt(29))
        self.assertAlmostEqual(v.normalized().length, 1)

class TestQuaternion(unittest.TestCase):
    sqrt2 = math.sqrt(2) / 2
    def test_init(self):
        q = Quaternion.identity()
        self.assertEqual(q.x, 0)
        self.assertEqual(q.y, 0)
        self.assertEqual(q.z, 0)
        self.assertEqual(q.w, 1)
        self.assertEqual(q, Quaternion(1, 0, 0, 0))
    
    def test_euler(self):
        q = Quaternion.Euler(Vector3(0, 90, 0))
        self.assertAlmostEqual(q, Quaternion(self.sqrt2, 0, self.sqrt2, 0))
        q.eulerAngles = Vector3(180, 0, 0)
        self.assertAlmostEqual(q, Quaternion(0, 1, 0, 0))

    def test_fromdir(self):
        q = Quaternion.FromDir(Vector3(0, 0, 1))
        self.assertEqual(q, Quaternion.identity())
        # q = Quaternion.FromDir(Vector3(0, 0, -1))
        # self.assertAlmostEqual(q, Quaternion(0, 0, 1, 0))
        q = Quaternion.FromDir(Vector3(0, 0, 0))
        self.assertEqual(q, Quaternion.identity())

if __name__ == "__main__":
    unittest.main()
