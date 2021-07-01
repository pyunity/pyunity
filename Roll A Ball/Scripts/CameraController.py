from pyunity import *

class CameraController(Behaviour):

    other = None

    def Start(self):
        self.offset = self.transform.position - self.other.transform.position
    
    def Update(self, dt):
        self.transform.position = self.other.transform.position + self.offset
