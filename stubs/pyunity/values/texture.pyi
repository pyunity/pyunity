__all__ = ["Material", "Color", "RGB", "HSV"]

from typing import Iterator, List, Tuple, Union, Optional
from ..files import Texture2D

class Material:
    color: Color = ...
    texture: Optional[Texture2D]

    def __init__(self, color: Color, texture: Texture2D) -> None: ...

class Color:
    def to_string(self) -> str: ...

    @staticmethod
    def from_string(string: str) -> Union[RGB, HSV]: ...

class RGB(Color):
    r: float
    g: float
    b: float

    def __init__(self, r: float, g: float, b: float) -> None: ...
    def __truediv__(self, other: float) -> Tuple[float]: ...
    def __mul__(self, other: float) -> Tuple[float]: ...
    def __list__(self) -> List[float]: ...
    def __iter__(self) -> Iterator[float]: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def to_rgb(self) -> RGB: ...
    def to_hsv(self) -> HSV: ...

    @staticmethod
    def from_hsv(h: float, s: float, v: float) -> RGB: ...

class HSV(Color):
    h: float
    s: float
    v: float

    def __init__(self, h: float, s: float, v: float) -> None: ...
    def __list__(self) -> List[float]: ...
    def __iter__(self) -> Iterator[float]: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def to_rgb(self) -> RGB: ...
    def to_hsv(self) -> HSV: ...

    @staticmethod
    def from_rgb(r: float, g: float, b: float) -> HSV: ...
