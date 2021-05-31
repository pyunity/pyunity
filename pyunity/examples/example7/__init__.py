from pyunity import *

class Switch(Behaviour):
    a = 3
    def Update(self, dt):
        self.a -= dt
        if self.a < 0:
            SceneManager.LoadSceneByName("Scene 2")

def main():
    scene = SceneManager.AddScene("Scene")
    scene2 = SceneManager.AddScene("Scene 2")
    scene.mainCamera.transform.localPosition = Vector3(0, 0, -10)
    scene2.mainCamera.transform.localPosition = Vector3(0, 0, -10)

    cube = GameObject("Cube")
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material(Color(255, 0, 0))
    cube.AddComponent(Switch).scene2 = scene2
    scene.Add(cube)

    cube2 = GameObject("Cube 2")
    renderer = cube2.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material(Color(0, 0, 255))
    scene2.Add(cube2)

    SceneManager.LoadScene(scene)


if __name__ == "__main__":
    main()
