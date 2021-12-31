from pyunity import SceneManager, GameObject, Vector3, MeshRenderer, Mesh, RGB, AABBoxCollider, Rigidbody, Material

def main():
    scene = SceneManager.AddScene("Scene")

    scene.mainCamera.transform.localPosition = Vector3(0, 3, -10)
    scene.mainCamera.transform.eulerAngles = Vector3(15, 0, 0)

    cube = GameObject("Cube")
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material(RGB(255, 0, 0))
    collider = cube.AddComponent(AABBoxCollider)
    collider.pos = Vector3(2, 0, 0)
    rb1 = cube.AddComponent(Rigidbody)
    rb1.transform.position = Vector3(2, 0, 0)
    rb1.gravity = False

    scene.Add(cube)

    cube = GameObject("Cube 2")
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material(RGB(0, 0, 255))
    collider = cube.AddComponent(AABBoxCollider)
    collider.pos = Vector3(6, 0, 0)
    rb2 = cube.AddComponent(Rigidbody)
    rb2.transform.position = Vector3(6, 0, 0)
    rb2.gravity = False

    scene.Add(cube)

    SceneManager.LoadScene(scene)


if __name__ == "__main__":
    main()
