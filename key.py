from pyunity.scenes.scene import Scene
from pyunity import *

class KeyLogger(Behaviour):
    def Start(self):
        self.done = False
    
    def Update(self, dt):
        if Input.GetKey(KeyCode.W) or Input.GetKeyUp(KeyCode.W):
            self.done = True
            print(
                int(Input.GetKey(KeyCode.W)),
                int(Input.GetKeyUp(KeyCode.W)),
                int(Input.GetKeyDown(KeyCode.W)),
            )
        else:
            self.done = False

scene = SceneManager.AddScene("Scene")
gmo = GameObject("gmo")
gmo.AddComponent(KeyLogger)
scene.Add(gmo)
SceneManager.LoadScene(scene)
