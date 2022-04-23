# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock
import textwrap
import sys
import os
import io
import math

if "full" not in os.environ:
    def atan(*args):
        if len(args) == 2:
            return math.atan2(*args)
        else:
            return math._atan(*args)
    math._atan = math.atan
    math.atan = atan

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
    os.environ["PYUNITY_INTERACTIVE"] = "0"
else:
    os.environ["PYUNITY_CHECK_WINDOW"] = "1"

from pyunity import *

class TestGameObject(unittest.TestCase):
    def testGameObjectName(self):
        gameObject = GameObject()
        self.assertEqual(gameObject.name, "GameObject")

    def testGameObjectTag(self):
        gameObject = GameObject()
        self.assertEqual(gameObject.tag.tag, 0)
        self.assertEqual(gameObject.tag.tagName, "Default")

    def testGameObjectTransform(self):
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

    def testGameObjectComponent(self):
        gameObject = GameObject()
        self.assertIsInstance(gameObject.transform, Transform)
        self.assertEqual(len(gameObject.components), 1)
        component = gameObject.AddComponent(Component)
        self.assertIsInstance(component, Component)
        self.assertEqual(len(gameObject.components), 2)
        self.assertIs(gameObject.GetComponent(Transform), gameObject.transform)
        with self.assertRaises(ComponentException) as exc:
            gameObject.AddComponent(Transform)
        self.assertEqual(str(exc.exception),
                         "Cannot add Transform to the GameObject; it already has one")

class TestTransform(unittest.TestCase):
    def testTransformPosition(self):
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

    def testTransformScale(self):
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
    def testInit(self):
        v = Vector3()
        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, 0)
        self.assertEqual(v.z, 0)
        self.assertEqual(v, Vector3.zero())
        v = Vector3.one()
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 1)
        self.assertEqual(v.z, 1)

    def testAdd(self):
        v1 = Vector3(0, 1, 2)
        v2 = Vector3(0, 2, 3)
        self.assertEqual(v1 + v2, Vector3(0, 3, 5))
        self.assertEqual(v2 + v1, Vector3(0, 3, 5))
        v1 += v2
        self.assertEqual(v1, Vector3(0, 3, 5))
        v2 += 2
        self.assertEqual(v2, Vector3(2, 4, 5))

    def testSub(self):
        v1 = Vector3(0, 1, 2)
        v2 = Vector3(0, 2, 3)
        self.assertEqual(v1 - v2, Vector3(0, -1, -1))
        self.assertEqual(v2 - v1, Vector3(0, 1, 1))
        v1 -= v2
        self.assertEqual(v1, Vector3(0, -1, -1))
        v2 -= 2
        self.assertEqual(v2, Vector3(-2, 0, 1))

    def testMul(self):
        v1 = Vector3(0, 1, 2)
        v2 = Vector3(0, 2, 3)
        self.assertEqual(v1 * v2, Vector3(0, 2, 6))
        self.assertEqual(v2 * v1, Vector3(0, 2, 6))
        v1 *= v2
        self.assertEqual(v1, Vector3(0, 2, 6))
        v2 *= 2
        self.assertEqual(v2, Vector3(0, 4, 6))

    def testDivOps(self):
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

    def testShifts(self):
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

    def testBitwise(self):
        v1 = Vector3(2, 3, 4)
        v2 = Vector3(0, 1, 2)
        self.assertEqual(v1 & v2, Vector3(0, 1, 0))
        self.assertEqual(v2 & v1, Vector3(0, 1, 0))
        self.assertEqual(v1 | v2, Vector3(2, 3, 6))
        self.assertEqual(v2 | v1, Vector3(2, 3, 6))
        self.assertEqual(v1 ^ v2, Vector3(2, 2, 6))
        self.assertEqual(v2 ^ v1, Vector3(2, 2, 6))

    def testUnary(self):
        v = Vector3(2, -3, 4)
        self.assertEqual(-v, Vector3(-2, 3, -4))
        self.assertEqual(+v, Vector3(2, -3, 4))
        self.assertEqual(~v, Vector3(-3, 2, -5))

    def testUtilFuncs(self):
        v = Vector3(2, -3, 4)
        self.assertEqual(v, v.copy())
        self.assertEqual(v.getLengthSqrd(), 29)
        self.assertEqual(v.length, math.sqrt(29))
        self.assertAlmostEqual(v.normalized().length, 1)
class TestVector2(unittest.TestCase):
    def testInit(self):
        v = Vector2()
        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, 0)
        self.assertEqual(v, Vector2.zero())
        v = Vector2.one()
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 1)

    def testAdd(self):
        v1 = Vector2(0, 1)
        v2 = Vector2(2, 3)
        self.assertEqual(v1 + v2, Vector2(2, 4))
        self.assertEqual(v2 + v1, Vector2(2, 4))
        v1 += v2
        self.assertEqual(v1, Vector2(2, 4))
        v2 += 2
        self.assertEqual(v2, Vector2(4, 5))

    def testSub(self):
        v1 = Vector2(0, 1)
        v2 = Vector2(2, 3)
        self.assertEqual(v1 - v2, Vector2(-2, -2))
        self.assertEqual(v2 - v1, Vector2(2, 2))
        v1 -= v2
        self.assertEqual(v1, Vector2(-2, -2))
        v2 -= 2
        self.assertEqual(v2, Vector2(0, 1))

    def testMul(self):
        v1 = Vector2(2, 3)
        v2 = Vector2(5, 4)
        self.assertEqual(v1 * v2, Vector2(10, 12))
        self.assertEqual(v2 * v1, Vector2(10, 12))
        v1 *= v2
        self.assertEqual(v1, Vector2(10, 12))
        v2 *= 2
        self.assertEqual(v2, Vector2(10, 8))

    def testDivOps(self):
        v1 = Vector2(2, 3)
        v2 = Vector2(5, 4)
        self.assertEqual(v1 / v2, Vector2(0.4, 0.75))
        self.assertEqual(v2 / v1, Vector2(2.5, 4/3))
        v1 /= v2
        self.assertEqual(v1, Vector2(0.4, 0.75))
        v2 /= 2
        self.assertEqual(v2, Vector2(2.5, 2))

        v1 = Vector2(2, 3)
        v2 = Vector2(4, 12)
        self.assertEqual(v1 // v2, Vector2(0, 0))
        self.assertEqual(v2 // v1, Vector2(2, 4))
        v1 //= v2
        self.assertEqual(v1, Vector2(0, 0))
        v2 //= 2
        self.assertEqual(v2, Vector2(2, 6))

        with self.assertRaises(ZeroDivisionError):
            v2 / 0

        v1 = Vector2(2, 3)
        v2 = Vector2(4, 12)
        self.assertEqual(v1 % v2, Vector2(2, 3))
        self.assertEqual(v2 % v1, Vector2(0, 0))
        v1 %= v2
        self.assertEqual(v1, Vector2(2, 3))
        v2 %= 2
        self.assertEqual(v2, Vector2(0, 0))

    def testShifts(self):
        v1 = Vector2(2, 3)
        v2 = Vector2(0, 1)
        self.assertEqual(v1 >> v2, Vector2(2, 1))
        self.assertEqual(v2 >> v1, Vector2(0, 0))
        v1 >>= v2
        self.assertEqual(v1, Vector2(2, 1))
        v2 >>= 2
        self.assertEqual(v2, Vector2(0, 0))

        v1 = Vector2(2, 3)
        v2 = Vector2(0, 1)
        self.assertEqual(v1 << v2, Vector2(2, 6))
        self.assertEqual(v2 << v1, Vector2(0, 8))
        v1 <<= v2
        self.assertEqual(v1, Vector2(2, 6))
        v2 <<= 2
        self.assertEqual(v2, Vector2(0, 4))

    def testBitwise(self):
        v1 = Vector2(3, 4)
        v2 = Vector2(1, 2)
        self.assertEqual(v1 & v2, Vector2(1, 0))
        self.assertEqual(v2 & v1, Vector2(1, 0))
        self.assertEqual(v1 | v2, Vector2(3, 6))
        self.assertEqual(v2 | v1, Vector2(3, 6))
        self.assertEqual(v1 ^ v2, Vector2(2, 6))
        self.assertEqual(v2 ^ v1, Vector2(2, 6))

    def testUnary(self):
        v = Vector2(-3, 4)
        self.assertEqual(-v, Vector2(3, -4))
        self.assertEqual(+v, Vector2(-3, 4))
        self.assertEqual(~v, Vector2(2, -5))

    def testUtilFuncs(self):
        v = Vector2(2, -3)
        self.assertEqual(v, v.copy())
        self.assertEqual(v.getLengthSqrd(), 13)
        self.assertEqual(v.length, math.sqrt(13))
        self.assertAlmostEqual(v.normalized().length, 1)

class TestQuaternion(unittest.TestCase):
    sqrt2 = math.sqrt(2) / 2
    def testInit(self):
        q = Quaternion.identity()
        self.assertEqual(q.x, 0)
        self.assertEqual(q.y, 0)
        self.assertEqual(q.z, 0)
        self.assertEqual(q.w, 1)
        self.assertEqual(q, Quaternion(1, 0, 0, 0))

    def testEulerAngles(self):
        q = Quaternion.Euler(Vector3(0, 90, 0))
        self.assertAlmostEqual(q, Quaternion(self.sqrt2, 0, self.sqrt2, 0))
        q.eulerAngles = Vector3(180, 0, 0)
        self.assertAlmostEqual(q, Quaternion(0, 1, 0, 0))

    def testFromDir(self):
        q = Quaternion.FromDir(Vector3(0, 0, 1))
        self.assertEqual(q, Quaternion.identity())
        # q = Quaternion.FromDir(Vector3(0, 0, -1))
        # self.assertAlmostEqual(q, Quaternion(0, 0, 1, 0))
        q = Quaternion.FromDir(Vector3(0, 0, 0))
        self.assertEqual(q, Quaternion.identity())

class TestScripts(unittest.TestCase):
    file1 = textwrap.dedent("""
    from pyunity import Behaviour

    class TestBehaviour1(Behaviour):
        def Start(self):
            print(self.gameObject.name)

    """)

    file2 = textwrap.dedent("""
    print("Hello World!")
    """)

    def testCheckScript(self):
        self.assertTrue(Scripts.CheckScript(self.file1.split("\n")))
        self.assertFalse(Scripts.CheckScript(self.file2.split("\n")))

    def testLoadScript(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file = os.path.join(tmpdir, "TestBehaviour1.py")
            with open(file, "w+") as f:
                f.write(self.file1)

            module = Scripts.LoadScript(file)
            self.assertTrue(module.__pyunity__)
            self.assertIs(__import__("PyUnityScripts"), module)
            self.assertIn(str(Path(file).absolute()), module._lookup)
            self.assertIn("TestBehaviour1", Scripts.var)
            self.assertIn("TestBehaviour1", module.__all__)
            self.assertTrue(hasattr(module, "TestBehaviour1"))
            self.assertTrue(hasattr(module, "TestBehaviour1"))

    def testLoadScriptFails(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file = os.path.join(tmpdir, "file1.py")
            with open(file, "w+") as f:
                f.write(self.file1)

            with self.assertRaises(PyUnityException) as exc:
                Scripts.LoadScript(file)
            self.assertEqual(str(exc.exception),
                f"Cannot find class 'file1' in {file!r}")

            file = os.path.join(tmpdir, "file2.py")
            with open(file, "w+") as f:
                f.write(self.file2)

            f = io.StringIO()
            Logger.stream = f
            Scripts.LoadScript(file)
            Logger.stream = sys.stdout
            self.assertEqual(f.getvalue(),
                f"Warning: {file!r} is not a valid PyUnity script\n")

class TestScene(unittest.TestCase):
    def setUp(self):
        if "full" not in os.environ:
            self.skipTest(reason="GLM not loaded; scene creation will fail")

    def tearDown(self):
        SceneManager.RemoveAllScenes()

    def testInit(self):
        scene = SceneManager.AddScene("Scene")
        self.assertEqual(scene.name, "Scene")
        self.assertEqual(len(scene.gameObjects), 2)

        for gameObject in scene.gameObjects:
            self.assertIs(gameObject.scene, scene)
            for component in gameObject.components:
                self.assertIs(component.gameObject, gameObject)
                self.assertIs(component.transform, gameObject.transform)
                self.assertIsInstance(component, Component)

        self.assertEqual(scene.gameObjects[0].name, "Main Camera")
        self.assertEqual(scene.gameObjects[1].name, "Light")
        self.assertIs(scene.mainCamera, scene.gameObjects[0].components[1])
        self.assertEqual(
            len(scene.gameObjects[0].components), 3)
        self.assertEqual(
            len(scene.gameObjects[1].components), 2)
        self.assertIsNotNone(
            scene.gameObjects[0].GetComponent(Camera))
        self.assertIsNotNone(
            scene.gameObjects[0].GetComponent(AudioListener))
        self.assertIsNotNone(
            scene.gameObjects[1].GetComponent(Light))

    def testFind(self):
        scene = SceneManager.AddScene("Scene")
        a = GameObject("A")
        b = GameObject("B", a)
        c = GameObject("C", a)
        d = GameObject("B", c)
        scene.AddMultiple(a, b, c, d)
        self.assertEqual(len(scene.FindGameObjectsByName("B")), 2)

class TestGui(unittest.TestCase):
    def setUp(self):
        if "full" not in os.environ:
            self.skipTest(reason="GLM not loaded; scene creation will fail")

    def tearDown(self):
        SceneManager.RemoveAllScenes()

    def testMakeButton(self):
        scene = SceneManager.AddScene("Scene")
        rectTransform, button, text = Gui.MakeButton(
            "Button", scene, "Button text",
            FontLoader.LoadFont("Consolas", 20), RGB(255, 0, 0))
        self.assertEqual(len(scene.gameObjects), 5)

        buttonObj = scene.gameObjects[2]
        self.assertEqual(len(buttonObj.components), 3)
        self.assertIs(buttonObj, button.gameObject)
        self.assertIs(buttonObj.GetComponent(RectTransform), rectTransform)
        self.assertIs(buttonObj.GetComponent(Button), button)

        textObj = scene.gameObjects[3]
        self.assertEqual(len(buttonObj.components), 3)
        self.assertIs(textObj, text.gameObject)
        self.assertIsNotNone(textObj.GetComponent(RectTransform))
        self.assertIs(textObj.GetComponent(Text), text)

        textureObj = scene.gameObjects[4]
        self.assertEqual(len(buttonObj.components), 3)
        self.assertIsNotNone(textureObj.GetComponent(Image2D))
        self.assertIsNotNone(textureObj.GetComponent(RectTransform))

if __name__ == "__main__":
    unittest.main()
