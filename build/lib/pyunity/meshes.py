from .vector3 import Vector3

class Mesh:
    def __init__(self, verts, triangles, normals):
        self.verts = verts
        self.triangles = triangles
        self.normals = normals

Mesh.quad = Mesh(
    [
        Vector3(1, 1, 0),
        Vector3(-1, 1, 0),
        Vector3(-1, -1, 0),
        Vector3(1, -1, 0),
    ],
    [
        [0, 1, 2],
        [0, 2, 3],
    ],
    [
        Vector3(0, 0, -1),
        Vector3(0, 0, -1)
    ]
)

Mesh.cube = Mesh(
    [
        Vector3(x, y, z) for x in [-1, 1] for y in [-1, 1] for z in [-1, 1]
    ],
    [
        [0, 2, 1],
        [1, 2, 3],
        [4, 5, 6],
        [5, 7, 6],
        [0, 4, 2],
        [2, 4, 6],
        [1, 3, 5],
        [3, 7, 5],
        [2, 6, 3],
        [3, 6, 7],
        [0, 1, 4],
        [4, 1, 5],
    ],
    [
        Vector3(-1, 0, 0),
        Vector3(-1, 0, 0),
        Vector3(1, 0, 0),
        Vector3(1, 0, 0),
        Vector3(0, 0, 1),
        Vector3(0, 0, 1),
        Vector3(0, 0, -1),
        Vector3(0, 0, -1),
        Vector3(0, 1, 0),
        Vector3(0, 1, 0),
        Vector3(0, -1, 0),
        Vector3(0, -1, 0),
    ]
)