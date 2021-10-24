from pyunity import *
import math

class Rotator(Behaviour):
    rotVel = Vector3(-math.pi, math.pi, math.pi)
    def Update(self, dt):
        rot = self.rotVel * dt
        self.transform.rotation *= Quaternion.FromAxis(math.degrees(rot.length), rot.normalized())

scene = SceneManager.AddScene("Scene")
scene.mainCamera.transform.position = Vector3(0, 3, -10)
scene.mainCamera.transform.eulerAngles = Vector3(15, 0, 0)

cube = GameObject("Cube")
renderer = cube.AddComponent(MeshRenderer)
renderer.mesh = Mesh.cube(2)
renderer.mat = Material(Color(255, 0, 0))
cube.AddComponent(Rotator)

scene.Add(cube)

scene.List()
SceneManager.LoadScene(scene)