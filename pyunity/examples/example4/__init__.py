from pyunity import *

class LookAt(Behaviour):
    other = ShowInInspector(GameObject)
    def Update(self, dt):
        self.transform.LookAtGameObject(self.other)
        self.transform.localEulerAngles *= Vector3(1, 1, 0)

class Mover(Behaviour):
    speed = ShowInInspector(float, 6)
    def Update(self, dt):
        self.transform.localPosition += Vector3(self.speed * dt, 0, 0)

def main():
    scene = SceneManager.AddScene("Scene")
    scene.mainCamera.transform.position = Vector3(0, 3, -10)
    lookAt = scene.mainCamera.AddComponent(LookAt)

    cube = GameObject("Cube")
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mat = Material(RGB(0, 255, 0))
    renderer.mesh = Loader.Primitives.cube
    cube.transform.position = Vector3(-20, 0, 0)
    cube.AddComponent(Mover).speed = 6
    scene.Add(cube)

    lookAt.other = cube

    SceneManager.LoadScene(scene)

if __name__ == "__main__":
    main()
