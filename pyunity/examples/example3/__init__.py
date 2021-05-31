from pyunity import *

def main():
    scene = SceneManager.AddScene("Scene")

    scene.mainCamera.transform.localPosition = Vector3(0, 6, -20)
    scene.mainCamera.transform.eulerAngles = Vector3(15, 0, 0)

    cube = GameObject("Cube")
    cube.transform.localPosition = Vector3(-5, 0, 0)
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material(Color(255, 0, 0))
    collider = cube.AddComponent(AABBoxCollider)
    collider.SetSize(Vector3(-6, -1, -1), Vector3(-4, 1, 1))
    rb = cube.AddComponent(Rigidbody)
    rb.velocity = Vector3(4, 0, 0)
    rb.gravity = False
    rb.mass = infinity

    scene.Add(cube)

    cube = GameObject("Cube 2")
    cube.transform.localPosition = Vector3(5, 0, 0)
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material(Color(0, 0, 255))
    collider = cube.AddComponent(AABBoxCollider)
    collider.SetSize(Vector3(4, -1, -1), Vector3(6, 1, 1))
    rb = cube.AddComponent(Rigidbody)
    rb.velocity = Vector3(-4, 0, 0)
    rb.gravity = False

    scene.Add(cube)

    cube = GameObject("Cube 3")
    cube.transform.localPosition = Vector3(0, 0, -6)
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material(Color(0, 255, 0))
    collider = cube.AddComponent(AABBoxCollider)
    collider.SetSize(Vector3(-1, -1, -7), Vector3(1, 1, -5))
    rb = cube.AddComponent(Rigidbody)
    rb.velocity = Vector3(0, 0, 4)
    rb.gravity = False

    scene.Add(cube)

    SceneManager.LoadScene(scene)


if __name__ == "__main__":
    main()
