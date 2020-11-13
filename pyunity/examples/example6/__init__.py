from pyunity import *
import math

rt50 = math.sqrt(50)

class Rotator(Behaviour):
    def Update(self, dt):
        self.transform.localEulerAngles += Vector3(0, 45 * dt, 0)
        print(round(1 / dt, 3))

def main():
    mat = Material((255, 0, 0))

    scene = SceneManager.AddScene("Scene")
    scene.mainCamera.transform.localPosition = Vector3(0, 3, 0)
    scene.mainCamera.transform.localEulerAngles = Vector3(20, 0, 0)

    root = GameObject("Root")
    root.AddComponent(Rotator)
    scene.Add(root)

    cube = GameObject("Cube", root)
    cube.transform.localPosition = Vector3(0, 0, 10)
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mat = mat
    renderer.mesh = loader.Primitives.cube
    scene.Add(cube)

    quad = GameObject("Quad", root)
    quad.transform.localPosition = Vector3(rt50, 0, rt50)
    quad.transform.localEulerAngles = Vector3(0, -45, 0)
    renderer = quad.AddComponent(MeshRenderer)
    renderer.mat = mat
    renderer.mesh = loader.Primitives.quad
    scene.Add(quad)

    sphere = GameObject("Sphere", root)
    sphere.transform.localPosition = Vector3(10, 0, 0)
    renderer = sphere.AddComponent(MeshRenderer)
    renderer.mat = mat
    renderer.mesh = loader.Primitives.sphere
    scene.Add(sphere)

    capsule = GameObject("Capsule", root)
    capsule.transform.localPosition = Vector3(rt50, 0, -rt50)
    renderer = capsule.AddComponent(MeshRenderer)
    renderer.mat = mat
    renderer.mesh = loader.Primitives.capsule
    scene.Add(capsule)

    cylinder = GameObject("Cylinder", root)
    cylinder.transform.localPosition = Vector3(0, 0, -10)
    renderer = cylinder.AddComponent(MeshRenderer)
    renderer.mat = mat
    renderer.mesh = loader.Primitives.cylinder
    scene.Add(cylinder)

    sphere = GameObject("Sphere", root)
    sphere.transform.localPosition = Vector3(-rt50, 0, -rt50)
    renderer = sphere.AddComponent(MeshRenderer)
    renderer.mat = mat
    renderer.mesh = loader.Primitives.sphere
    scene.Add(sphere)

    capsule = GameObject("Capsule", root)
    capsule.transform.localPosition = Vector3(-10, 0, 0)
    renderer = capsule.AddComponent(MeshRenderer)
    renderer.mat = mat
    renderer.mesh = loader.Primitives.capsule
    scene.Add(capsule)

    quad = GameObject("Quad", root)
    quad.transform.localPosition = Vector3(-rt50, 0, rt50)
    quad.transform.localEulerAngles = Vector3(0, 45, 0)
    renderer = quad.AddComponent(MeshRenderer)
    renderer.mat = mat
    renderer.mesh = loader.Primitives.quad
    scene.Add(quad)

    SceneManager.LoadScene(scene)
