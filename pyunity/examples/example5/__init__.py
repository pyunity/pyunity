from pyunity import *
from .scripts import *
import os

def main():
    mesh = loader.LoadObj(os.path.join(os.path.dirname(os.path.abspath(__file__)), "house.obj"))

    scene = SceneManager.AddScene("Scene")

    scene.mainCamera.transform.position = Vector3(0, 0, -20)
    scene.gameObjects[1].GetComponent(Light).intensity = 100

    house = GameObject("House")
    house.transform.rotation = Vector3(0, 180, 0)
    renderer = house.AddComponent(MeshRenderer)
    renderer.mesh = mesh
    renderer.mat = Material((255, 0, 0))
    house.AddComponent(Rotator)
    
    scene.Add(house)
    
    scene.Run()
