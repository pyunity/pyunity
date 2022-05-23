from pyunity import *

scene = SceneManager.AddScene("Scene")
project = Loader.GenerateProject("Test")
g = GameObject("Cube")
renderer = g.AddComponent(MeshRenderer)
renderer.mesh = Mesh.cube(2)
renderer.mat = Material(RGB(255, 0, 0))
class Rotator(Behaviour):
    def Update(self, dt):
        self.transform.eulerAngles += Vector3(0, 90, 135) * dt

g.AddComponent(Rotator)
prefab = Prefab(g)
project.ImportAsset(prefab, g)
project.Write()

class Instantiator(Behaviour):
    prefab = ShowInInspector(Prefab)

    def Start(self):
        self.prefab.Instantiate()

scene.mainCamera.AddComponent(Instantiator).prefab = prefab
scene.mainCamera.transform.position = Vector3(0, 0, -10)
Loader.SaveScene(scene, project, "Scenes")
