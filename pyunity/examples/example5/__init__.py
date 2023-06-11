## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import Behaviour, Vector3, Logger, Material, RGB, SceneManager, GameObject, MeshRenderer, Loader
import math

rt50 = math.sqrt(50)

def average(l):
    return sum(l) / len(l)

class Rotator(Behaviour):
    async def Start(self):
        self.fps = []

    async def Update(self, dt):
        self.transform.localEulerAngles += Vector3(0, 45 * dt, 0)
        if len(self.fps) == 100:
            self.fps.pop(0)
        self.fps.append(1 / dt)
        Logger.Log(round(average(self.fps), 3))

def main():
    mat = Material(RGB(255, 0, 0))

    scene = SceneManager.AddScene("Scene")
    scene.mainCamera.transform.localPosition = Vector3(0, 3, 0)
    scene.mainCamera.transform.localEulerAngles = Vector3(20, 0, 0)
    scene.gameObjects[1].transform.localPosition = Vector3(0, 3, 0)

    root = GameObject("Root")
    root.AddComponent(Rotator)
    scene.Add(root)

    cube = GameObject("Cube", root)
    cube.transform.localPosition = Vector3(0, 0, 10)
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mat = mat
    renderer.mesh = Loader.Primitives.cube
    scene.Add(cube)

    quad = GameObject("Quad", root)
    quad.transform.localPosition = Vector3(rt50, 0, rt50)
    quad.transform.localEulerAngles = Vector3(0, 45, 0)
    renderer = quad.AddComponent(MeshRenderer)
    renderer.mat = mat
    renderer.mesh = Loader.Primitives.quad
    scene.Add(quad)

    sphere = GameObject("Sphere", root)
    sphere.transform.localPosition = Vector3(10, 0, 0)
    renderer = sphere.AddComponent(MeshRenderer)
    renderer.mat = mat
    renderer.mesh = Loader.Primitives.sphere
    scene.Add(sphere)

    capsule = GameObject("Capsule", root)
    capsule.transform.localPosition = Vector3(rt50, 0, -rt50)
    renderer = capsule.AddComponent(MeshRenderer)
    renderer.mat = mat
    renderer.mesh = Loader.Primitives.capsule
    scene.Add(capsule)

    cylinder = GameObject("Cylinder", root)
    cylinder.transform.localPosition = Vector3(0, 0, -10)
    renderer = cylinder.AddComponent(MeshRenderer)
    renderer.mat = mat
    renderer.mesh = Loader.Primitives.cylinder
    scene.Add(cylinder)

    sphere = GameObject("Sphere", root)
    sphere.transform.localPosition = Vector3(-rt50, 0, -rt50)
    renderer = sphere.AddComponent(MeshRenderer)
    renderer.mat = mat
    renderer.mesh = Loader.Primitives.sphere
    scene.Add(sphere)

    dquad = GameObject("Double Quad", root)
    dquad.transform.localPosition = Vector3(-10, 0, 0)
    dquad.transform.localEulerAngles = Vector3(0, -90, 0)
    renderer = dquad.AddComponent(MeshRenderer)
    renderer.mat = mat
    renderer.mesh = Loader.Primitives.doubleQuad
    scene.Add(dquad)

    capsule = GameObject("Capsule", root)
    capsule.transform.localPosition = Vector3(-rt50, 0, rt50)
    capsule.transform.localEulerAngles = Vector3(0, -45, 0)
    renderer = capsule.AddComponent(MeshRenderer)
    renderer.mat = mat
    renderer.mesh = Loader.Primitives.capsule
    scene.Add(capsule)

    SceneManager.LoadScene(scene)
