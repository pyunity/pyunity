## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import (
    SceneManager, Component, Camera, AudioListener, Light,
    GameObject, Tag, Transform, GameObjectException,
    ComponentException, Canvas, PyUnityException,
    Behaviour, ShowInInspector, RenderTarget, Logger,
    Vector3, MeshRenderer, Mesh)
from . import SceneTestCase

class TestScene(SceneTestCase):
    def testInit(self):
        scene = SceneManager.AddScene("Scene")
        assert scene.name == "Scene"
        assert len(scene.gameObjects) == 2

        for gameObject in scene.gameObjects:
            assert gameObject.scene is scene
            for component in gameObject.components:
                assert component.gameObject is gameObject
                assert component.transform is gameObject.transform
                assert isinstance(component, Component)

        assert scene.gameObjects[0].name == "Main Camera"
        assert scene.gameObjects[1].name == "Light"
        assert scene.mainCamera is scene.gameObjects[0].components[1]
        assert len(scene.gameObjects[0].components) == 3
        assert len(scene.gameObjects[1].components) == 2
        assert scene.gameObjects[0].GetComponent(Camera) is not None
        assert scene.gameObjects[0].GetComponent(AudioListener) is not None
        assert scene.gameObjects[1].GetComponent(Light) is not None

    def testFind(self):
        scene = SceneManager.AddScene("Scene")
        a = GameObject("A")
        b = GameObject("B", a)
        c = GameObject("C", a)
        d = GameObject("B", c)
        scene.AddMultiple(a, b, c, d)

        tagnum = Tag.AddTag("Custom Tag")
        a.tag = Tag(tagnum)
        c.tag = Tag("Custom Tag")

        assert len(scene.FindGameObjectsByName("B")) == 2
        assert scene.FindGameObjectsByName("B") == [b, d]
        assert scene.FindGameObjectsByTagName("Custom Tag") == [a, c]
        assert scene.FindGameObjectsByTagNumber(tagnum) == [a, c]

        assert isinstance(scene.FindComponent(Transform), Transform)
        assert scene.FindComponents(Transform) == [
            scene.mainCamera.transform, scene.gameObjects[1].transform,
            a.transform, b.transform, c.transform, d.transform]

        with self.assertRaises(GameObjectException) as exc:
            scene.FindGameObjectsByTagName("Invalid")
        assert exc.value == "No tag named Invalid; create a new tag with Tag.AddTag"

        with self.assertRaises(GameObjectException) as exc:
            scene.FindGameObjectsByTagNumber(-1)
        assert exc.value == "No tag at index -1; create a new tag with Tag.AddTag"

        with self.assertRaises(ComponentException) as exc:
            scene.FindComponent(Canvas)
        assert exc.value == "Cannot find component Canvas in scene"

    def testRootGameObjects(self):
        scene = SceneManager.AddScene("Scene")
        a = GameObject("A")
        b = GameObject("B", a)
        c = GameObject("C", a)
        d = GameObject("B", c)
        scene.AddMultiple(a, b, c, d)
        assert len(scene.rootGameObjects) == 3
        assert scene.rootGameObjects[2] is a

    def testAddError(self):
        scene = SceneManager.AddScene("Scene")
        gameObject = GameObject("GameObject")
        scene.Add(gameObject)

        with self.assertRaises(PyUnityException) as exc:
            scene.Add(gameObject)
        assert exc.value == "GameObject \"GameObject\" is already in Scene \"Scene\""

    def testBare(self):
        from pyunity.scenes import Scene
        scene = Scene.Bare("Scene")
        assert scene.name == "Scene"
        assert len(scene.gameObjects) == 0
        assert scene.mainCamera is None

    def testDestroy(self):
        class Test(Behaviour):
            other = ShowInInspector(GameObject)

        scene = SceneManager.AddScene("Scene")

        # Exception
        fake = GameObject("Not in scene")
        with self.assertRaises(PyUnityException) as exc:
            scene.Destroy(fake)
        assert exc.value == "The provided GameObject is not part of the Scene"

        # Correct
        a = GameObject("A")
        b = GameObject("B", a)
        c = GameObject("C", a)
        scene.AddMultiple(a, b, c)
        assert c.scene is scene
        assert c in scene.gameObjects

        scene.Destroy(c)
        assert c.scene is None
        assert c not in scene.gameObjects

        # Multiple
        scene.Destroy(a)
        assert b.scene is None
        assert b not in scene.gameObjects
        assert c.scene is None
        assert c not in scene.gameObjects

        # Components
        cam = GameObject("Camera")
        camera = cam.AddComponent(Camera)
        test = GameObject("Test")
        test.AddComponent(Test).other = cam
        target = GameObject("Target")
        target.AddComponent(RenderTarget).source = camera
        scene.AddMultiple(cam, test, target)

        scene.Destroy(cam)
        assert b.scene is None
        assert cam not in scene.gameObjects
        assert test.GetComponent(Test).other is None
        assert target.GetComponent(RenderTarget).source is None

        # Main Camera
        with Logger.TempRedirect(silent=True) as r:
            scene.Destroy(scene.mainCamera.gameObject)
        assert r.get() == "Warning: Removing Main Camera from scene 'Scene'\n"

    def testHas(self):
        scene = SceneManager.AddScene("Scene")
        gameObject = GameObject("GameObject")
        gameObject2 = GameObject("GameObject 2")
        scene.Add(gameObject)
        assert scene.Has(gameObject)
        assert not scene.Has(gameObject2)

    def testList(self):
        scene = SceneManager.AddScene("Scene")
        a = GameObject("A")
        b = GameObject("B", a)
        c = GameObject("C", a)
        d = GameObject("B", c)
        scene.AddMultiple(b, d, c, a)
        with Logger.TempRedirect(silent=True) as r:
            scene.List()
        assert r.get() == "\n".join([
            "/A", "/A/B", "/A/C", "/A/C/B", "/Light", "/Main Camera\n"])

    def testInsideFrustrum(self):
        scene = SceneManager.AddScene("Scene")
        gameObject = GameObject("Cube")
        gameObject.transform.position = Vector3(0, 0, 5)
        renderer = gameObject.AddComponent(MeshRenderer)
        scene.Add(gameObject)
        assert not scene.insideFrustrum(renderer)

        renderer.mesh = Mesh.cube(2)
        # assert scene.insideFrustrum(renderer))

        gameObject.transform.position = Vector3(0, 0, -5)
        # assert not scene.insideFrustrum(renderer)
