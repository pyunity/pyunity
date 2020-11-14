from unittest import TestCase, main
from unittest.mock import Mock
import sys
sys.modules["pygame"] = Mock()
sys.modules["glfw"] = Mock()
sys.modules["OpenGL"] = Mock()
sys.modules["OpenGL.GL"] = Mock()
sys.modules["OpenGL.GLU"] = Mock()
sys.modules["OpenGL.GLUT"] = Mock()

from pyunity import *

class TestGameObject(TestCase):
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
        self.assertEqual(gameObject2.transform.parent.gameObject.name, "GameObject")
        self.assertEqual(len(gameObject.transform.children), 1)
        self.assertEqual(len(gameObject2.transform.children), 0)

    def test_gameobject_component(self):
        gameObject = GameObject()
        self.assertIsInstance(gameObject.transform, Component)
        self.assertEqual(len(gameObject.components), 1)
        component = gameObject.AddComponent(Component)
        self.assertIsInstance(component, Component)
        self.assertEqual(len(gameObject.components), 2)
        self.assertIs(gameObject.GetComponent(Transform), gameObject.transform)
        with self.assertRaises(ComponentException):
            gameObject.AddComponent(Transform)

class TestVector3(TestCase):
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

if __name__ == "__main__":
    main()
