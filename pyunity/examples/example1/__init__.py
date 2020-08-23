from pyunity import *
from .scripts import *

# TODO: https://www.youtube.com/watch?v=eFxcAI85xeg&list=PLEETnX-uPtBXm1KEr_2zQ6K_0hoGH6JJ0&index=3

def main():
    scene = SceneManager.AddScene("Scene1")

    scene.mainCamera.transform.position = Vector3(0, 3, -10)
    scene.mainCamera.transform.rotation = Vector3(20, 0, 0)

    cube = GameObject("Cube")
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material((255, 0, 0))
    cube.AddComponent(Rotator)

    scene.Add(cube)

    scene.List()

    scene.Run()

if __name__ == "__main__":
    main()