# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

"""Module for meshes created at runtime."""

from typing import List, Optional
from .values import Vector3

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
    def compile(self) -> None: ...
    def copy(self) -> Mesh: ...
    def draw(self) -> None: ...
    
    @staticmethod
    def quad(size: float) -> Mesh: ...
    @staticmethod
    def double_quad(size: float) -> Mesh: ...
    @staticmethod
    def cube(size: float) -> Mesh: ...
