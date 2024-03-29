## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import (RGB, Behaviour, GameObject, Material, Mesh, MeshRenderer,
                     SceneManager, Vector3, WaitForSeconds)

class Switch(Behaviour):
    async def Start(self):
        await WaitForSeconds(3)
        SceneManager.LoadSceneByIndex(1)

def main():
    scene = SceneManager.AddScene("Scene")
    scene2 = SceneManager.AddScene("Scene 2")
    scene.mainCamera.transform.localPosition = Vector3(0, 0, -10)
    scene2.mainCamera.transform.localPosition = Vector3(0, 0, -10)

    cube = GameObject("Cube")
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material(RGB(255, 0, 0))
    cube.AddComponent(Switch)
    scene.Add(cube)

    cube2 = GameObject("Cube 2")
    renderer = cube2.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material(RGB(0, 0, 255))
    scene2.Add(cube2)

    SceneManager.LoadScene(scene)

if __name__ == "__main__":
    main()
