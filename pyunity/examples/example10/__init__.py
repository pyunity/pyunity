## Copyright (c) 2020-2022 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import SceneManager, GameObject, Vector3, Quaternion, MeshRenderer, Loader, Material, RGB, Behaviour, Camera, ShowInInspector, Input, KeyCode, Light, LightType, Mathf

class OrthoMover(Behaviour):
    cam = ShowInInspector(Camera)
    async def Update(self, dt):
        if Input.GetKey(KeyCode.E):
            self.cam.orthoSize -= dt * 3
        if Input.GetKey(KeyCode.Q):
            self.cam.orthoSize += dt * 3
        self.cam.orthoSize = Mathf.Clamp(self.cam.orthoSize, 2, 16)

        x = Vector3(1, 0, -1) * dt * 8
        y = Vector3(1, 0, 1) * dt * 8
        self.cam.transform.position += x * Input.GetAxis("Horizontal")
        self.cam.transform.position += y * Input.GetAxis("Vertical")

def main():
    scene = SceneManager.AddScene("Scene")
    scene.gameObjects[1].GetComponent(Light).type = LightType.Point
    scene.gameObjects[1].transform.position = Vector3(10, 10, 10)

    scene.mainCamera.transform.position = Vector3(-5, 10, -5)
    scene.mainCamera.transform.localRotation = Quaternion.Euler(Vector3(30, 45, 0))
    scene.mainCamera.skyboxEnabled = False
    scene.mainCamera.ortho = True
    scene.mainCamera.orthoSize = 8
    scene.mainCamera.shadows = False

    mover = scene.mainCamera.AddComponent(OrthoMover)
    mover.cam = scene.mainCamera

    red = Material(RGB(255, 0, 0))
    blue = Material(RGB(0, 0, 255))
    green = Material(RGB(0, 255, 0))
    for i in range(11):
        for j in range(11):
            g = GameObject("Cube")
            g.transform.position = Vector3(i * 2, 0, j * 2)
            renderer = g.AddComponent(MeshRenderer)
            renderer.mesh = Loader.Primitives.cube
            renderer.mat = red if (i * 11 + j) % 2 == 0 else blue
            if i == 5 and j == 5:
                renderer.mat = green
            scene.Add(g)

    SceneManager.LoadScene(scene)

if __name__ == "__main__":
    main()
