# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import Behaviour, Vector3, SceneManager, GameObject, Mesh, Material, RGB, Texture2D, MeshRenderer
from importlib_resources import files, as_file
from contextlib import ExitStack

class Rotator(Behaviour):
    def Update(self, dt):
        self.transform.eulerAngles += Vector3(0, 90, 135) * dt

def main():
    scene = SceneManager.AddScene("Scene")

    scene.mainCamera.transform.localPosition = Vector3(0, 0, -10)

    stack = ExitStack()
    ref = files(__package__) / "logo.png"
    path = stack.enter_context(as_file(ref))

    cube = GameObject("Cube")
    texture = Texture2D(path)
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material(RGB(255, 255, 255), texture)
    cube.AddComponent(Rotator)
    scene.Add(cube)

    SceneManager.LoadScene(scene)
    stack.close()

if __name__ == "__main__":
    main()
