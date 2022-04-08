# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import Behaviour, SceneManager, GameObject, Vector3, MeshRenderer, Mesh, Material, RGB, Quaternion

class Rotator(Behaviour):
    def Update(self, dt):
        self.transform.eulerAngles += Vector3(0, 90, 135) * dt

def main():
    scene = SceneManager.AddScene("Scene")
    scene.gameObjects[1].transform.position = Vector3(0, 10, 0)
    scene.gameObjects[1].transform.LookAtPoint(Vector3.zero())
    scene.mainCamera.transform.localPosition = Vector3(0, 5, -10)
    scene.mainCamera.transform.LookAtPoint(Vector3.zero())

    cube = GameObject("Cube")
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material(RGB(255, 0, 0))
    cube.AddComponent(Rotator)
    scene.Add(cube)

    floor = GameObject("Floor")
    floor.transform.position = Vector3(0, -4, 0)
    floor.transform.scale = Vector3(10, 1, 10)
    renderer = floor.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material(RGB(255, 255, 255))
    scene.Add(floor)

    scene.List()
    SceneManager.LoadScene(scene)

if __name__ == "__main__":
    main()
