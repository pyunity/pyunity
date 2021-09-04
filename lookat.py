from pyunity import *

class LookAt(Behaviour):
    other = ShowInInspector(GameObject)
    def Update(self, dt):
        self.transform.LookAtGameObject(self.other)

class Mover(Behaviour):
    speed = ShowInInspector(float, 6)
    def Update(self, dt):
        self.transform.localPosition += Vector3(self.speed * dt, 0, 0)

scene = SceneManager.AddScene("Scene")
scene.mainCamera.transform.position = Vector3(0, 3, -10)
lookAt = scene.mainCamera.AddComponent(LookAt)

cube = GameObject("Cube")
renderer = cube.AddComponent(MeshRenderer)
renderer.mat = Material(RGB(255, 0, 0))
renderer.mesh = Mesh.cube(2)
cube.transform.position = Vector3(-20, 0, 0)
cube.AddComponent(Mover).speed = 6
scene.Add(cube)

lookAt.other = cube

SceneManager.LoadScene(scene)