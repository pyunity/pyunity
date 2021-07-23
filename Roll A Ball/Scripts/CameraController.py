from pyunity import *

class CameraController(Behaviour):
    other = ShowInInspector(GameObject)

    def Start(self):
        self.offset = self.transform.position - self.other.transform.position
    
    def LateUpdate(self, dt):
        self.transform.position = self.other.transform.position + self.offset
