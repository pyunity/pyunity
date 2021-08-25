from typing import Any, Iterable, List, Tuple
from .vector3 import Vector3

class Quaternion:
    def __init__(self, w: float, x: float, y: float, z: float) -> None: ...
    def __repr__(self) -> str: ...
    def __getitem__(self, i: int) -> float: ...
    def __iter__(self) -> Iterable[float]: ...
    def __list__(self) -> List[float]: ...
    def __len__(self) -> int: ...
    def __eq__(self, other: Any) -> bool: ...
    def __ne__(self, other: Any) -> bool: ...
    def __mul__(self, other: Quaternion) -> Quaternion: ...
    def copy(self) -> Quaternion: ...
    def normalized(self) -> Quaternion: ...
    def RotateVector(self, vector: Vector3) -> Vector3: ...
    def convert(self) -> Quaternion: ...

    @staticmethod
    def FromAxis(angle: float, a: Vector3) -> Quaternion: ...
    @staticmethod
    def Euler(vector: Vector3) -> Quaternion: ...
    @staticmethod
    def identity() -> Quaternion: ...
    @staticmethod
    def Between(v1: Vector3, v2: Vector3) -> Quaternion: ...
    @staticmethod
    def FromDir(v: Vector3) -> Quaternion: ...

    @property
    def conjugate(self) -> Quaternion: ...
    @property
    def angleAxisPair(self) -> Tuple[float]: ...
    @property
    def eulerAngles(self) -> Vector3: ...