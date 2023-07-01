## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import Behaviour, Vector3, SceneManager, GameObject, Mesh, Material, RGB, Texture2D, MeshRenderer
from pyunity.resources import resolver

class Rotator(Behaviour):
    async def Update(self, dt):
        self.transform.eulerAngles += Vector3(0, 90, 135) * dt

def main():
    scene = SceneManager.AddScene("Scene")

    scene.mainCamera.transform.localPosition = Vector3(0, 0, -10)

    cube = GameObject("Cube")
    texture = Texture2D(resolver.getPath("examples/example8/logo.png"))
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material(RGB(255, 255, 255), texture)
    cube.AddComponent(Rotator)
    scene.Add(cube)

    SceneManager.LoadScene(scene)

if __name__ == "__main__":
    main()
