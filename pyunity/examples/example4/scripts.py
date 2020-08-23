from pyunity import *

class Rotator(Behaviour):
    def Update(self, dt):
        self.transform.rotation += Vector3(45, 90, 135) * dt