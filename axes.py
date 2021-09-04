from pyunity import *

class AxisTracker(Behaviour):
    name = ShowInInspector(str)
    def Update(self, dt):
        print(Input.GetAxis(self.name))

scene = SceneManager.AddScene("Scene")
scene.mainCamera.AddComponent(AxisTracker).name = "Vertical"
SceneManager.LoadScene(scene)