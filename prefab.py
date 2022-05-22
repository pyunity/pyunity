from pyunity import *

SceneManager.AddScene("Scene")
project = Loader.GenerateProject("Test")
g = GameObject("Cube")
renderer = g.AddComponent(MeshRenderer)
renderer.mesh = Mesh.cube(2)
renderer.mat = Material(RGB(255, 0, 0))
class Rotator(Behaviour):
    def Update(self, dt):
        self.transform.eulerAngles += Vector3(45, 90, 135) * dt

g.AddComponent(Rotator)
prefab = Prefab(g)
print(prefab.assets)
project.ImportAsset(prefab, g)
