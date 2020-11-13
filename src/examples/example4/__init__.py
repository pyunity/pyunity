from pyunity import *
import os

class Rotator(Behaviour):
    def Update(self, dt):
        self.transform.eulerAngles += Vector3(0, 90, 135) * dt

def main():
    mesh = loader.LoadMesh(os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "cube.mesh"))

    scene = SceneManager.AddScene("Scene")

    scene.mainCamera.transform.localPosition = Vector3(0, 0, -10)

    cube = GameObject("Cube")
    cube.AddComponent(Rotator)
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = mesh
    renderer.mat = Material((255, 0, 0))
    scene.Add(cube)

    scene.List()
    SceneManager.LoadScene(scene)


if __name__ == "__main__":
    main()
