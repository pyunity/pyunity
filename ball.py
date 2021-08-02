from pyunity import *

class PlayerController(Behaviour):
    speed = ShowInInspector(int, 8)
    rigidbody = ShowInInspector(Rigidbody)
    
    def Update(self, dt):
        x = Input.GetKey(KeyCode.D) - Input.GetKey(KeyCode.A)
        y = Input.GetKey(KeyCode.W) - Input.GetKey(KeyCode.S)

        movement = Vector3(x, 0, y)
        self.rigidbody.AddForce(movement * self.speed * 2)

class CameraController(Behaviour):
    other = ShowInInspector(GameObject)

    def Start(self):
        self.offset = self.transform.position - self.other.transform.position
    
    def LateUpdate(self, dt):
        self.transform.position = self.other.transform.position + self.offset

scene = SceneManager.AddScene("Main Scene")
scene.mainCamera.transform.localPosition = Vector3(0, 10, -20)

ball = GameObject("Ball")
ball.AddComponent(AABBoxCollider)
rb = ball.AddComponent(Rigidbody)
rb.mass = 50
rb.gravity = False
rb.physicMaterial = PhysicMaterial(0.5, 0)
renderer = ball.AddComponent(MeshRenderer)
renderer.mesh = Loader.Primitives.sphere
ball.AddComponent(PlayerController).rigidbody = rb
scene.Add(ball)

scene.mainCamera.AddComponent(CameraController).other = ball
scene.mainCamera.transform.localEulerAngles = Vector3(26.5, 0, 0)

floor = GameObject("Floor")
floor.transform.position = Vector3(0, -2, 0)
floor.transform.scale = Vector3(50, 1, 50)
floor.AddComponent(AABBoxCollider)
renderer = floor.AddComponent(MeshRenderer)
renderer.mesh = Loader.Primitives.cube
renderer.mat = Material(RGB(50, 50, 50))
scene.Add(floor)

wall1 = GameObject("Wall")
wall1.transform.position = Vector3(0, 0.5, 51)
wall1.transform.scale = Vector3(50, 3, 1)
wall1.AddComponent(AABBoxCollider)
renderer = wall1.AddComponent(MeshRenderer)
renderer.mesh = Loader.Primitives.cube
scene.Add(wall1)

wall2 = GameObject("Wall")
wall2.transform.position = Vector3(0, 0.5, -51)
wall2.transform.scale = Vector3(50, 3, 1)
wall2.AddComponent(AABBoxCollider)
renderer = wall2.AddComponent(MeshRenderer)
renderer.mesh = Loader.Primitives.cube
scene.Add(wall2)

wall3 = GameObject("Wall")
wall3.transform.position = Vector3(49, 0.5, 0)
wall3.transform.scale = Vector3(1, 3, 50)
wall3.AddComponent(AABBoxCollider)
renderer = wall3.AddComponent(MeshRenderer)
renderer.mesh = Loader.Primitives.cube
scene.Add(wall3)

wall4 = GameObject("Wall")
wall4.transform.position = Vector3(-49, 0.5, 0)
wall4.transform.scale = Vector3(1, 3, 50)
wall4.AddComponent(AABBoxCollider)
renderer = wall4.AddComponent(MeshRenderer)
renderer.mesh = Loader.Primitives.cube
scene.Add(wall4)

SceneManager.LoadSceneByIndex(0)

Loader.SaveSceneToProject(scene, name="Roll A Ball")
