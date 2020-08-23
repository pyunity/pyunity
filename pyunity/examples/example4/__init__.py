from pyunity import *
from .scripts import *

def main():
    mesh = loader.LoadObj("pyunity/examples/example4/cube.obj")

    scene = SceneManager.AddScene("Scene")

    scene.mainCamera.transform.position = Vector3(0, 3, -10)
    scene.mainCamera.transform.rotation = Vector3(20, 0, 0)

    cube = GameObject("Cube")
    cube.AddComponent(Rotator)
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = mesh
    renderer.mat = Material((255, 0, 0))
    
    scene.Add(cube)
    
    scene.Run()