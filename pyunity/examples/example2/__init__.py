from pyunity import SceneManager, GameObject, Vector3, MeshRenderer, Mesh, RGB, BoxCollider, Rigidbody, Material, Behaviour, Input, KeyCode, ShowInInspector

class PhysicsController(Behaviour):
    started = False
    rb1 = ShowInInspector(Rigidbody)
    rb2 = ShowInInspector(Rigidbody)
    def Update(self, dt):
        if not self.started and Input.GetKeyDown(KeyCode.Space):
            self.rb1.velocity = Vector3(-2, 0, 0)
            self.rb2.velocity = Vector3(-4, 0, 0)
            self.started = True
        if self.started and Input.GetKeyDown(KeyCode.R):
            self.started = False
            self.rb1.transform.position = Vector3(2, 0, 0)
            self.rb2.transform.position = Vector3(6, 0, 0)
            self.rb1.velocity = Vector3.zero()
            self.rb2.velocity = Vector3.zero()

def main():
    scene = SceneManager.AddScene("Scene")

    scene.mainCamera.transform.localPosition = Vector3(0, 3, -10)
    scene.mainCamera.transform.eulerAngles = Vector3(15, 0, 0)

    cube = GameObject("Cube")
    cube.transform.localPosition = Vector3(2, 0, 0)
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material(RGB(255, 0, 0))
    collider = cube.AddComponent(BoxCollider)
    rb1 = cube.AddComponent(Rigidbody)
    rb1.gravity = False

    scene.Add(cube)

    cube = GameObject("Cube 2")
    cube.transform.localPosition = Vector3(6, 0, 0)
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material(RGB(0, 0, 255))
    collider = cube.AddComponent(BoxCollider)
    rb2 = cube.AddComponent(Rigidbody)
    rb2.gravity = False

    scene.Add(cube)

    cont = scene.mainCamera.AddComponent(PhysicsController)
    cont.rb1 = rb1
    cont.rb2 = rb2

    SceneManager.LoadScene(scene)


if __name__ == "__main__":
    main()
