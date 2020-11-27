from pyunity import *
from pyunity import config
config.windowProvider = "Pygame"

class CarController(Behaviour):
    def Update(self, dt):
        down = Input.GetKeyDown(KeyCode.W)
        if down: print("W is pressed down")
        up = Input.GetKeyUp(KeyCode.W)
        if up: print("W is released")

scene = SceneManager.AddScene("Scene")
scene.mainCamera.transform.localPosition = Vector3(0, 4, -10)

car = GameObject("Car")
car.transform.localScale = Vector3(2, 1, 4)
renderer = car.AddComponent(MeshRenderer)
renderer.mesh = Mesh.cube(1)
renderer.mat = Material((0, 0, 255))
car.AddComponent(CarController)

scene.mainCamera.transform.LookAtGameObject(car)
scene.Add(car)

SceneManager.LoadScene(scene)