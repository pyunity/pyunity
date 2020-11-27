import math
from pyunity import *
from pyunity import config
config.windowProvider = "Pygame"

class CarController(Behaviour):
    def Update(self, dt):
        down = Input.GetKeyDown(KeyCode.W)
        if down: print("W is pressed down")
        up = Input.GetKeyUp(KeyCode.W)
        if up: print("W is released")

class Car(Behaviour):
    def Start(self):
        self.x = 0
        self.y = 0
        self.vel = 0
        self.accel = 0
        self.accel_rate = 0.3
        self.avg_accel_initial = 5
        self.avg_accel = self.avg_accel_initial
        self.rot = 0
        self.rot_vel = 0
        self.max_speed = 10

    def move(self, dt):
        sin, cos = math.sin(self.rot), math.cos(self.rot)
        self.rot += self.rot_vel * dt * \
            math.tanh(self.vel / self.max_speed * 2)
        self.x += sin * self.vel * dt
        self.y += cos * self.vel * dt
        
        self.transform.position = Vector3(self.x, 0, self.y)

    def Update(self, dt):
        self.vel = round((self.vel + self.accel * dt) * 0.999, 10)
        self.avg_accel = (self.max_speed - abs(self.vel)) / \
            self.max_speed * self.avg_accel_initial
        if Input.GetKey(KeyCode.Space):
            self.vel *= 0.95
        self.move(dt)
        if Input.GetKey(KeyCode.Up) or Input.GetKey(KeyCode.W):
            self.accel += self.accel_rate * self.avg_accel
        elif Input.GetKey(KeyCode.Down) or Input.GetKey(KeyCode.S):
            self.accel -= self.accel_rate * self.avg_accel
        if Input.GetKey(KeyCode.Left) or Input.GetKey(KeyCode.A):
            self.rot_vel -= math.pi / 20
        if Input.GetKey(KeyCode.Right) or Input.GetKey(KeyCode.D):
            self.rot_vel += math.pi / 20
        self.rot_vel *= 0.9
        self.accel = round(self.accel * (1 - self.accel_rate), 10)
        
        SceneManager.CurrentScene.mainCamera.transform.LookAtGameObject(self)

scene = SceneManager.AddScene("Scene")
scene.mainCamera.transform.localPosition = Vector3(0, 4, -10)

car = GameObject("Car")
car.transform.localScale = Vector3(2, 1, 4)
renderer = car.AddComponent(MeshRenderer)
renderer.mesh = Mesh.cube(1)
renderer.mat = Material((0, 0, 255))
car.AddComponent(Car)

scene.Add(car)
scene.mainCamera.transform.LookAtGameObject(car)

SceneManager.LoadScene(scene)