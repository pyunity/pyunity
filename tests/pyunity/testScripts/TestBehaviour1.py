from pyunity import Behaviour

class TestBehaviour1(Behaviour):
    def Start(self):
        print(self.gameObject.name)
