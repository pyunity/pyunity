from pyunity import *

class CameraController(Behaviour):

    attrs = ["other"]

    def Start(self):
        self.offset = self.transform.position - self.other.transform.position
    
    def Update(self, dt):
        self.transform.position = self.other.transform.position + self.offset
