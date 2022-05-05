from pyunity import (
    SceneManager, GameObject, MeshRenderer, Mesh, Material, RGB,
    Canvas, RectTransform, RenderTarget, Loader, Vector2)
from . import TestCase
import tempfile
import os

class ChangeDirectory:
    def __init__(self, directory):
        self.directory = directory
        self.original = ""

    def __enter__(self):
        self.original = os.getcwd()
        os.chdir(self.directory)
        return self

    def __exit__(self, exctype, excvalue, exctb):
        os.chdir(self.original)

class TestLoadProject(TestCase):
    def testResave(self):
        scene = SceneManager.AddScene("Scene")

        cube = GameObject("Cube")
        renderer = cube.AddComponent(MeshRenderer)
        renderer.mesh = Mesh.cube(2)
        renderer.mat = Material(RGB(255, 0, 0))
        scene.Add(cube)

        canvas = GameObject("Canvas")
        scene.mainCamera.canvas = canvas.AddComponent(Canvas)
        scene.Add(canvas)

        target = GameObject("Target", canvas)
        rectTransform = target.AddComponent(RectTransform)
        rectTransform.anchors.max = Vector2(0.5, 0.5)
        target.AddComponent(RenderTarget)
        scene.Add(target)

        with tempfile.TemporaryDirectory() as tmpdir:
            with ChangeDirectory(tmpdir):
                project = Loader.GenerateProject("Test")
                Loader.SaveProject(project)
                assert os.listdir() == ["Test"]
                oldIds = project._ids.copy()

                SceneManager.RemoveAllScenes()
                project = Loader.LoadProject("Test")
                newscene = SceneManager.GetSceneByIndex(0)
                newIds = project._ids

                assert len(scene.gameObjects) == len(newscene.gameObjects)
                for i in range(len(scene.gameObjects)):
                    a = scene.gameObjects[i]
                    b = newscene.gameObjects[i]
                    assert oldIds[a] == newIds[b]
                    assert len(a.components) == len(b.components)
                    for j in range(len(a.components)):
                        c = a.components[j]
                        d = b.components[j]
                        assert oldIds[c] == newIds[d]
