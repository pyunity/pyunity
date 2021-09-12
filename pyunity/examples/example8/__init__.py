from pyunity import Behaviour, Vector3, SceneManager, GameObject, Mesh, Material, RGB, Texture2D, MeshRenderer
import os

class Rotator(Behaviour):
    def Update(self, dt):
        self.transform.eulerAngles += Vector3(0, 90, 135) * dt

def main():
    scene = SceneManager.AddScene("Scene")

    scene.mainCamera.transform.localPosition = Vector3(0, 0, -10)

    cube = GameObject("Cube")
    texture = Texture2D(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "logo.png"))
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material(RGB(255, 255, 255), texture)
    cube.AddComponent(Rotator)

    scene.Add(cube)

    scene.List()
    SceneManager.LoadScene(scene)

if __name__ == "__main__":
    main()
