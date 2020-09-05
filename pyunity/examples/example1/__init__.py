from pyunity import *

class Rotator(Behaviour):
    a = 0
    def Update(self, dt):
        if self.a == 1:
            self.transform.rotation *= Quaternion.Euler(Vector3(45, 90, 135) * dt)
            print(self.transform.eulerAngles.rounded)
            self.a = 0
        self.a += 1

def main():
    scene = SceneManager.AddScene("Scene")

    scene.mainCamera.transform.position = Vector3(0, 3, -10)
    scene.mainCamera.transform.eulerAngles = Vector3(20, 0, 0)

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