## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import (RGB, BoxCollider, GameObject, Infinity, Material, Mesh,
                     MeshRenderer, Rigidbody, SceneManager, Vector3)

def main():
    scene = SceneManager.AddScene("Scene")

    scene.mainCamera.transform.localPosition = Vector3(0, 6, -20)
    scene.mainCamera.transform.eulerAngles = Vector3(15, 0, 0)

    cube = GameObject("Cube")
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material(RGB(255, 0, 0))
    collider = cube.AddComponent(BoxCollider)
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
    collider = cube.AddComponent(BoxCollider)
    collider.pos = Vector3(5, 0, 0)
    rb = cube.AddComponent(Rigidbody)
    rb.velocity = Vector3(-4, 0, 0)
    rb.gravity = False

    scene.Add(cube)

    cube = GameObject("Cube 3")
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material(RGB(0, 255, 0))
    collider = cube.AddComponent(BoxCollider)
    collider.pos = Vector3(0, 0, -6)
    rb = cube.AddComponent(Rigidbody)
    rb.velocity = Vector3(0, 0, 4)
    rb.gravity = False

    scene.Add(cube)

    SceneManager.LoadScene(scene)

if __name__ == "__main__":
    main()
