from pyunity import *

class Rotator(Behaviour):
    def Update(self, dt):
        self.transform.rotation += Vector3(0, 45, 0) * dt

def main():
    scene = SceneManager.AddScene("Scene")
    scene.gameObjects[1].transform.localPosition = Vector3(0, 3, 0)

    mat = Material((255, 0, 0))

    rotator = GameObject("Parent")
    rotator.AddComponent(Rotator)
    scene.Add(rotator)

    cube = GameObject("Cube", rotator)
    cube.transform.localPosition = Vector3(0, 0, 10)
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = loader.Primitives.cube
    renderer.mat = mat
    scene.Add(cube)

    quad = GameObject("Quad", rotator)
    quad.transform.localPosition = Vector3(7, 0, 7)
    # quad.transform.localRotation = Vector3(0, -45, 0)
    renderer = quad.AddComponent(MeshRenderer)
    renderer.mesh = loader.Primitives.quad
    renderer.mat = mat
    scene.Add(quad)

    sphere = GameObject("Sphere", rotator)
    sphere.transform.localPosition = Vector3(10, 0, 0)
    renderer = sphere.AddComponent(MeshRenderer)
    renderer.mesh = loader.Primitives.sphere
    renderer.mat = mat
    scene.Add(sphere)

    cylinder = GameObject("Cylinder", rotator)
    cylinder.transform.localPosition = Vector3(7, 0, -7)
    renderer = cylinder.AddComponent(MeshRenderer)
    renderer.mesh = loader.Primitives.cylinder
    renderer.mat = mat
    scene.Add(cylinder)

    capsule = GameObject("Capsule", rotator)
    capsule.transform.localPosition = Vector3(0, 0, -10)
    renderer = capsule.AddComponent(MeshRenderer)
    renderer.mesh = loader.Primitives.capsule
    renderer.mat = mat
    scene.Add(capsule)

    cylinder = GameObject("Cylinder", rotator)
    cylinder.transform.localPosition = Vector3(-7, 0, -7)
    renderer = cylinder.AddComponent(MeshRenderer)
    renderer.mesh = loader.Primitives.cylinder
    renderer.mat = mat
    scene.Add(cylinder)

    sphere = GameObject("Sphere", rotator)
    sphere.transform.localPosition = Vector3(-10, 0, 0)
    renderer = sphere.AddComponent(MeshRenderer)
    renderer.mesh = loader.Primitives.sphere
    renderer.mat = mat
    scene.Add(sphere)

    quad = GameObject("Quad", rotator)
    quad.transform.localPosition = Vector3(7, 0, 7)
    # quad.transform.localRotation = Vector3(0, -45, 0)
    renderer = quad.AddComponent(MeshRenderer)
    renderer.mesh = loader.Primitives.quad
    renderer.mat = mat
    scene.Add(quad)

    scene.Run()

if __name__ == "__main__":
    main()