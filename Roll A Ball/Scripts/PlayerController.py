from pyunity import *

class PlayerController(Behaviour):
    speed = ShowInInspector(int, 8)
    
    def Update(self, dt):
        x = Input.GetKey(KeyCode.D) - Input.GetKey(KeyCode.A)
        y = Input.GetKey(KeyCode.W) - Input.GetKey(KeyCode.S)

        movement = Vector3(x, 0, y)
        self.transform.position += movement * self.speed * dt
