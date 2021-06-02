from pyunity import *
import os

class Rotator(Behaviour):
    def Update(self, dt):
        self.transform.eulerAngles += Vector3(0, 90, 0) * dt

def main():
    Logger.Log("House mesh is currently broken")

    # mesh = Loader.LoadMesh(os.path.join(
    #     os.path.dirname(os.path.abspath(__file__)), "house.mesh"))

    scene = SceneManager.AddScene("Scene")

    scene.mainCamera.transform.localPosition = Vector3(0, 0, -20)

    house = GameObject("House")
    house.transform.eulerAngles = Vector3(0, 180, 0)
    renderer = house.AddComponent(MeshRenderer)
    # renderer.mesh = mesh
    renderer.mat = Material(Color(255, 0, 0))
    house.AddComponent(Rotator)

    scene.Add(house)

    SceneManager.LoadScene(scene)


if __name__ == "__main__":
    main()
