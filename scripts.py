from pyunity import *

class Rotator(Behaviour):
    def Update(self):
        self.transform.rotation.y += 1