from .core import Mesh
from .vector3 import Vector3

quad = Mesh(
    [
        Vector3(1, 1, 0),
        Vector3(-1, 1, 0),
        Vector3(-1, -1, 0),
        Vector3(1, -1, 0),
    ],
    [
        [0, 1, 2],
        [3, 0, 2],
    ]
)