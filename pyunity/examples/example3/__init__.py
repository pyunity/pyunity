from pyunity import SceneManager, GameObject, Material, RGB, MeshRenderer, Vector3, Mesh, Rigidbody, AABBoxCollider, Infinity

def main():
    scene = SceneManager.AddScene("Scene")

    scene.mainCamera.transform.localPosition = Vector3(0, 6, -20)
    scene.mainCamera.transform.eulerAngles = Vector3(15, 0, 0)

    cube = GameObject("Cube")
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material(RGB(255, 0, 0))
    collider = cube.AddComponent(AABBoxCollider)
    collider.pos = Vector3(-5, 0, 0)
    rb = cube.AddComponent(Rigidbody)
    rb.velocity = Vector3(4, 0, 0)
    rb.gravity = False
    rb.mass = Infinity

    scene.Add(cube)

    cube = GameObject("Cube 2")
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material(RGB(0, 0, 255))
    collider = cube.AddComponent(AABBoxCollider)
    collider.pos = Vector3(5, 0, 0)
    rb = cube.AddComponent(Rigidbody)
    rb.velocity = Vector3(-4, 0, 0)
    rb.gravity = False

    scene.Add(cube)

    cube = GameObject("Cube 3")
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material(RGB(0, 255, 0))
    collider = cube.AddComponent(AABBoxCollider)
    collider.pos = Vector3(0, 0, -6)
    rb = cube.AddComponent(Rigidbody)
    rb.velocity = Vector3(0, 0, 4)
    rb.gravity = False

    scene.Add(cube)

    SceneManager.LoadScene(scene)

if __name__ == "__main__":
    main()
