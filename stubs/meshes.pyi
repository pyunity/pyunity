from typing import List, Optional
from .vector3 import Vector3

class Mesh:
    verts: List[Vector3]
    triangles: List[int]
    normals: List[Vector3]
    texcoords: List[float]
    compiled: bool
    def __init__(self, verts: List[Vector3],
                triangles: List[List[int]],
                normals: List[Vector3],
                texcoords: Optional[List[List[float]]]=...) -> None: ...
    def recompile(self) -> None: ...
    def copy(self) -> Mesh: ...
    
    @staticmethod
    def quad(size: float) -> Mesh: ...
    @staticmethod
    def ddouble_quad(size: float) -> Mesh: ...
    @staticmethod
    def cube(size: float) -> Mesh: ...
