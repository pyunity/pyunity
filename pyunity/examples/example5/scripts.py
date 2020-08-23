from pyunity import *

class Rotator(Behaviour):
    def Update(self, dt):
        self.transform.rotation += Vector3(0, 0, 90) * dt