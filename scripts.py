from pyunity import *

class Rotator(Behaviour):
    def Update(self):
        self.transform.rotation.y += self.deltaTime * 60