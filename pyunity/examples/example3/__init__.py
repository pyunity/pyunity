from pyunity import *

def main():
    scene = SceneManager.AddScene("Scene")
    
    scene.mainCamera.transform.position = Vector3(0, 0, -20)
    scene.mainCamera.transform.rotation = Vector3(20, 0, 0)
    
    cube = GameObject("Cube")
    cube.transform.position = Vector3(-5, 0, 0)
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material((255, 0, 0))
    collider = cube.AddComponent(AABBoxCollider)
    collider.SetSize(Vector3(-6, -1, -1), Vector3(-4, 1, 1))
    collider.velocity = Vector3(4, 0, 0)
    collider.mass = infinity

    scene.Add(cube)
    
    cube = GameObject("Cube 2")
    cube.transform.position = Vector3(5, 0, 0)
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material((0, 0, 255))
    collider = cube.AddComponent(AABBoxCollider)
    collider.SetSize(Vector3(4, -1, -1), Vector3(6, 1, 1))
    collider.velocity = Vector3(-4, 0, 0)

    scene.Add(cube)
    
    cube = GameObject("Cube 3")
    cube.transform.position = Vector3(0, 0, -6)
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material((0, 255, 0))
    collider = cube.AddComponent(AABBoxCollider)
    collider.SetSize(Vector3(-1, -1, -7), Vector3(1, 1, -5))
    collider.velocity = Vector3(0, 0, 4)

    scene.Add(cube)

    loader.SaveScene(scene, __file__)

    scene.Run()