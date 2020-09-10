from pyunity import *

class Rotator(Behaviour):
    def Update(self, dt):
        self.transform.eulerAngles += Vector3(0, 90, 135) * dt

def main():
    scene = SceneManager.AddScene("Scene")

    scene.mainCamera.transform.localPosition = Vector3(0, 0, -10)

    cube = GameObject("Cube")
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(1)
    renderer.mat = Material((255, 0, 0))
    cube.AddComponent(Rotator)

    scene.Add(cube)

    scene.List()

    scene.Run()

if __name__ == "__main__":
    main()