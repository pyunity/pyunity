from pyunity import *

class Rotator(Behaviour):
    def Update(self, dt):
        self.transform.localEulerAngles += Vector3(0, 90 * dt, 0)

def main():
    mat = Material((255, 0, 0))

    scene = SceneManager.AddScene("Scene")
    scene.mainCamera.transform.localPosition = Vector3(0, 3, 0)
    scene.mainCamera.transform.localEulerAngles = Vector3(20, 0, 0)

    root = GameObject("Root")
    root.AddComponent(Rotator)
    scene.Add(root)

    cube = GameObject("Cube", root)
    cube.transform.localPosition = Vector3(0, 0, 10)
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mat = mat
    renderer.mesh = loader.Primitives.cube
    scene.Add(cube)

    scene.Run()