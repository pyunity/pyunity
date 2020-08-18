from pyunity.engine import *
from scripts import *

def main():
    scene = SceneManager.AddScene("Scene")

    scene.mainCamera.transform.position = Vector3(0, 3, -10)
    scene.mainCamera.transform.rotation = Vector3(20, 0, 0)

    cube = GameObject("Cube")
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = meshes.cube
    renderer.mat = Material((255, 0, 0))
    cube.AddComponent(Rotator)

    scene.Add(cube)

    scene.List()

    scene.Run()

if __name__ == "__main__":
    main()