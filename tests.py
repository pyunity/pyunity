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

class TestPyUnity(TestCase):
    def test_gameobject_name(self):
        gameObject = GameObject()
        self.assertEqual(gameObject.name, "GameObject")

    def test_gameobject_tag(self):
        gameObject = GameObject()
        self.assertEqual(gameObject.tag.tag, 0)
        self.assertEqual(gameObject.tag.tagName, "Default")

    def test_gameobject_transform(self):
        gameObject = GameObject()
        self.assertTrue(isinstance(gameObject.transform, Transform))

if __name__ == "__main__":
    main()
