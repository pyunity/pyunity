from pyunity import Behaviour, SceneManager, GameObject, Vector3, MeshRenderer, Mesh, Material, RGB, ShowInInspector

class Rotator(Behaviour):
    a = ShowInInspector(int, 0)
    def Update(self, dt):
        self.transform.eulerAngles += Vector3(0, 90, 135) * dt

def main():
    scene = SceneManager.AddScene("Scene")

    scene.mainCamera.transform.localPosition = Vector3(0, 0, -10)

    cube = GameObject("Cube")
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material(RGB(255, 0, 0))
    cube.AddComponent(Rotator)

    scene.Add(cube)

    scene.List()
    SceneManager.LoadScene(scene)

if __name__ == "__main__":
    main()
