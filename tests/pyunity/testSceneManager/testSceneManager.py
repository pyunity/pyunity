## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import (
    SceneManager, PyUnityException)
from . import SceneTestCase
import pytest

class TestSceneManager(SceneTestCase):
    def testAdd(self):
        scene = SceneManager.AddScene("Scene")
        assert scene in SceneManager.scenesByIndex
        assert SceneManager.scenesByIndex[0] is scene
        assert "Scene" in SceneManager.scenesByName
        assert SceneManager.scenesByName["Scene"] is scene

    def testAddException(self):
        SceneManager.AddScene("Scene")
        with self.assertRaises(PyUnityException) as exc:
            SceneManager.AddScene("Scene")
        assert exc.value == "SceneManager already contains scene 'Scene'"

    def testAddBare(self):
        scene = SceneManager.AddBareScene("Scene")
        assert len(scene.gameObjects) == 0
        assert scene.mainCamera is None

    def testAddBareException(self):
        SceneManager.AddBareScene("Scene")
        with self.assertRaises(PyUnityException) as exc:
            SceneManager.AddBareScene("Scene")
        assert exc.value == "SceneManager already contains scene 'Scene'"

    def testGet(self):
        scene = SceneManager.AddScene("Scene")
        assert SceneManager.GetSceneByIndex(0) is scene
        assert SceneManager.GetSceneByName("Scene") is scene

        with self.assertRaises(IndexError) as exc:
            SceneManager.GetSceneByIndex(1)
        assert exc.value == "There is no scene at index 1"

        with self.assertRaises(PyUnityException) as exc:
            SceneManager.GetSceneByName("non-existent")
        assert exc.value == "There is no scene called 'non-existent'"

    def testRemove(self):
        scene1 = SceneManager.AddScene("Scene 1")
        scene2 = SceneManager.AddScene("Scene 2")
        SceneManager.RemoveScene(scene1)
        assert SceneManager.GetSceneByIndex(0) is scene2
        assert scene1 not in SceneManager.scenesByIndex
        assert scene1 not in SceneManager.scenesByName.values()

def mockLoad(scene):
    print(f"Loading scene {scene.name!r}")

class TestSceneManagerLoad(SceneTestCase):
    def setUp(self):
        super().setUp()
        # SceneManager.__loadScene = mockLoad
        pytest.skip("Cannot replace SceneManager.__loadScene")

    def testByName(self):
        SceneManager.AddScene("Scene")
        SceneManager.LoadSceneByName("Scene")

        with self.assertRaises(TypeError) as exc:
            SceneManager.LoadSceneByName(0)
        assert exc.value == "Expected str, got int"

        with self.assertRaises(PyUnityException) as exc:
            SceneManager.LoadSceneByName("non-existent")
        assert exc.value == "There is no scene named 'non-existent'"

    def testByIndex(self):
        SceneManager.AddScene("Scene")
        SceneManager.LoadSceneByIndex(0)

        with self.assertRaises(TypeError) as exc:
            SceneManager.LoadSceneByIndex("Scene")
        assert exc.value == "Expected int, got str"

        with self.assertRaises(PyUnityException) as exc:
            SceneManager.LoadSceneByIndex(1)
        assert exc.value == "There is no scene at index 1"

    def testLoad(self):
        from pyunity.scenes import Scene
        scene = SceneManager.AddScene("Scene")
        SceneManager.LoadScene(scene)

        with self.assertRaises(TypeError) as exc:
            SceneManager.LoadScene(0)
        assert exc.value == "Expected Scene, got int"

        with self.assertRaises(PyUnityException) as exc:
            SceneManager.LoadScene(Scene("Wrong scene"))
        assert exc.value == "The provided scene is not part of the SceneManager"
