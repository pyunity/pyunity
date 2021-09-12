from pyunity import Behaviour, GameObject, SceneManager, Material, RGB, Mesh, Vector3, MeshRenderer

class Switch(Behaviour):
    def Start(self):
        self.a = 3

    def Update(self, dt):
        self.a -= dt
        if self.a < 0:
            SceneManager.LoadSceneByIndex(1)

def main():
    scene = SceneManager.AddScene("Scene")
    scene2 = SceneManager.AddScene("Scene 2")
    scene.mainCamera.transform.localPosition = Vector3(0, 0, -10)
    scene2.mainCamera.transform.localPosition = Vector3(0, 0, -10)

    cube = GameObject("Cube")
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material(RGB(255, 0, 0))
    cube.AddComponent(Switch)
    scene.Add(cube)

    cube2 = GameObject("Cube 2")
    renderer = cube2.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material(RGB(0, 0, 255))
    scene2.Add(cube2)

    SceneManager.LoadScene(scene)

if __name__ == "__main__":
    main()
