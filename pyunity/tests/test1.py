from engine import *
from scripts import *

def main():
    scene = SceneManager.AddScene("Scene")

    scene.mainCamera.transform.position = Vector3(0, 0, -10)

    quad = GameObject("Quad")
    renderer = quad.AddComponent(MeshRenderer)
    renderer.mesh = meshes.quad
    renderer.mat = Material((255, 0, 0))
    quad.AddComponent(Rotator)

    scene.Add(quad)

    quad2 = GameObject("Quad2", quad)
    renderer = quad2.AddComponent(MeshRenderer)
    renderer.mesh = meshes.quad
    renderer.mat = Material((255, 0, 0))
    quad2.transform.position = Vector3(2, 0, 0)

    scene.Add(quad2)

    quad3 = GameObject("Quad3", quad)
    renderer = quad3.AddComponent(MeshRenderer)
    renderer.mesh = meshes.quad
    renderer.mat = Material((255, 0, 0))
    quad3.transform.position = Vector3(-2, 0, 0)

    scene.Add(quad3)

    scene.List()

    scene.Run()

if __name__ == "__main__":
    main()