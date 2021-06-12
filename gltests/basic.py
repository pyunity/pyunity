from pyunity import *
class Rotator(Behaviour):
    def Update(self, dt):
        self.transform.eulerAngles += Vector3(0, 90, 135) * dt

scene = SceneManager.AddScene("Scene")
scene.mainCamera.transform.localPosition = Vector3(0, 0, -10)
cube = GameObject("Cube")
renderer = cube.AddComponent(MeshRenderer)
renderer.mesh = Mesh.cube(2)
renderer.mat = Material(Color(255, 0, 0))
cube.AddComponent(Rotator)
scene.Add(cube)
Loader.SaveScene(scene)
