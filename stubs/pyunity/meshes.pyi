## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""Module for meshes created at runtime and their various attributes."""

__all__ = ["Mesh", "MeshRenderer", "Color", "RGB", "HSV", "Material"]

from typing import List, Optional, Union, Any, Iterator
from .values import Vector3
from .files import Asset, Texture2D
from .core import SingleComponent

floatSize: int = ...

class Mesh(Asset):
    verts: List[Vector3]
    triangles: List[int]
    normals: List[Vector3]
    texcoords: List[float]
    compiled: bool
    min: Vector3
    max: Vector3
    def __init__(self, verts: List[Vector3],
                triangles: List[List[int]],
                normals: List[Vector3],
                texcoords: Optional[List[List[float]]] = ...) -> None: ...
    def compile(self, force: bool = ...) -> None: ...
    def draw(self) -> None: ...
    def copy(self) -> Mesh: ...

    @staticmethod
    def quad(size: float) -> Mesh: ...
    @staticmethod
    def doubleQuad(size: float) -> Mesh: ...
    @staticmethod
    def cylinder(radius: float, height: float, detail: int = ...) -> Mesh: ...
    @staticmethod
    def sphere(size: float, detail: int = ...) -> Mesh: ...
    @staticmethod
    def capsule(radius: float, height: float, detail: int = ...) -> Mesh: ...
    @staticmethod
    def cube(size: float) -> Mesh: ...

class Material(Asset):
    color: Color
    texture: Texture2D
    def __init__(self, color: Color, texture: Optional[Texture2D] = ...) -> None: ...

class Color:
    def toString(self) -> str: ...
    @staticmethod
    def fromString(string: str) -> Union[RGB, HSV]: ...

class RGB(Color):
    r: int
    g: int
    b: int
    def __init__(self, r: int, g: int, b: int) -> None: ...
    def __eq__(self, other: Union[RGB, Any]) -> bool: ...
    def __hash__(self) -> int: ...
    def __list__(self) -> List[int]: ...
    def __iter__(self) -> Iterator[int]: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __truediv__(self, other: float) -> RGB: ...
    def __mul__(self, other: float) -> RGB: ...
    def toRGB(self) -> RGB: ...
    def toHSV(self) -> HSV: ...
    @staticmethod
    def fromHSV(h: int, s: int, v: int) -> RGB: ...

class HSV(Color):
    h: int
    s: int
    v: int
    def __init__(self, h: int, s: int, v: int) -> None: ...
    def __eq__(self, other: Union[HSV, Any]) -> bool: ...
    def __hash__(self) -> int: ...
    def __list__(self) -> List[int]: ...
    def __iter__(self) -> Iterator[int]: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def toRGB(self) -> RGB: ...
    def toHSV(self) -> HSV: ...
    @staticmethod
    def fromRGB(r: int, g: int, b: int) -> HSV: ...

class MeshRenderer(SingleComponent):
    DefaultMaterial: Material = ...
    mesh: Union[Mesh, None] = ...
    mat: Material = ...
    def Render(self) -> None: ...
