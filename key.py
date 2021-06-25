from pyunity.scenes.scene import Scene
from pyunity import *

class KeyLogger(Behaviour):
    def Update(self, dt):
        keys = [
            int(Input.GetKey(KeyCode.W)),
            int(Input.GetKeyUp(KeyCode.W)),
            int(Input.GetKeyDown(KeyCode.W)),
        ]
        if keys != [0, 0, 0]:
            print(keys)

scene = SceneManager.AddScene("Scene")
gmo = GameObject("gmo")
gmo.AddComponent(KeyLogger)
scene.Add(gmo)
SceneManager.LoadScene(scene)
