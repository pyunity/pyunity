from pyunity import *

class LookAt(Behaviour):
    other = ShowInInspector(GameObject)
    def LateUpdate(self, dt):
        self.transform.LookAtGameObject(self.other)
        self.transform.localEulerAngles *= Vector3(1, 1, 0)

class Mover(Behaviour):
    speed = ShowInInspector(float, 6)
    rb = ShowInInspector(Rigidbody)
    def Update(self, dt):
        if Input.GetMouseDown(MouseCode.Left):
            self.rb.velocity = Vector3(0, 0, self.speed)

def main():
    scene = SceneManager.AddScene("Scene")
    scene.mainCamera.transform.position = Vector3(0, 3, -10)
    lookAt = scene.mainCamera.AddComponent(LookAt)

    cube = GameObject("Cube")
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mat = Material(RGB(0, 255, 0))
    renderer.mesh = Loader.Primitives.cube
    cube.transform.position = Vector3(-20, 0, 0)
    mover = cube.AddComponent(Mover)
    rb = cube.AddComponent(Rigidbody)
    mover.rb = rb
    scene.Add(cube)

    lookAt.other = cube

    SceneManager.LoadScene(scene)

if __name__ == "__main__":
    main()
