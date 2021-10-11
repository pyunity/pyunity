from typing import Dict, List
from enum import IntEnum
from .values import ImmutableStruct, Vector2

class KeyState(IntEnum):
    UP: KeyState = ...
    DOWN: KeyState = ...
    PRESS: KeyState = ...
    NONE: KeyState = ...

class KeyCode(IntEnum):
    A: KeyCode = ...
    B: KeyCode = ...
    C: KeyCode = ...
    D: KeyCode = ...
    E: KeyCode = ...
    F: KeyCode = ...
    G: KeyCode = ...
    H: KeyCode = ...
    I: KeyCode = ...
    J: KeyCode = ...
    K: KeyCode = ...
    L: KeyCode = ...
    M: KeyCode = ...
    N: KeyCode = ...
    O: KeyCode = ...
    P: KeyCode = ...
    Q: KeyCode = ...
    R: KeyCode = ...
    S: KeyCode = ...
    T: KeyCode = ...
    U: KeyCode = ...
    V: KeyCode = ...
    W: KeyCode = ...
    X: KeyCode = ...
    Y: KeyCode = ...
    Z: KeyCode = ...
    Space: KeyCode = ...
    Alpha0: KeyCode = ...
    Alpha1: KeyCode = ...
    Alpha2: KeyCode = ...
    Alpha3: KeyCode = ...
    Alpha4: KeyCode = ...
    Alpha5: KeyCode = ...
    Alpha6: KeyCode = ...
    Alpha7: KeyCode = ...
    Alpha8: KeyCode = ...
    Alpha9: KeyCode = ...
    F1: KeyCode = ...
    F2: KeyCode = ...
    F3: KeyCode = ...
    F4: KeyCode = ...
    F5: KeyCode = ...
    F6: KeyCode = ...
    F7: KeyCode = ...
    F8: KeyCode = ...
    F9: KeyCode = ...
    F10: KeyCode = ...
    F11: KeyCode = ...
    F12: KeyCode = ...
    Keypad0: KeyCode = ...
    Keypad1: KeyCode = ...
    Keypad2: KeyCode = ...
    Keypad3: KeyCode = ...
    Keypad4: KeyCode = ...
    Keypad5: KeyCode = ...
    Keypad6: KeyCode = ...
    Keypad7: KeyCode = ...
    Keypad8: KeyCode = ...
    Keypad9: KeyCode = ...
    Up: KeyCode = ...
    Down: KeyCode = ...
    Left: KeyCode = ...
    Right: KeyCode = ...

class MouseCode(IntEnum):
    Left: MouseCode = ...
    Middle: MouseCode = ...
    Right: MouseCode = ...

class KeyboardAxis:
    positve: List[KeyCode]
    negative: List[KeyCode]
    value: float
    name: str
    speed: float
    def __init__(self, name: str, speed: float, positive: List[KeyCode], negative: List[KeyCode]) -> None: ...
    def get_value(self, dt: float) -> float: ...

class Input(metaclass=ImmutableStruct):
    _names: List[str] = ...
    _axes: Dict[str, float] = ...
    _axis_objects: Dict[str, KeyboardAxis] = ...
    mousePosition: Vector2
    _mouse_last: Vector2
    @classmethod
    def GetKey(cls, keycode: KeyCode) -> bool: ...
    @classmethod
    def GetKeyUp(cls, keycode: KeyCode) -> bool: ...
    @classmethod
    def GetKeyDown(cls, keycode: KeyCode) -> bool: ...
    @classmethod
    def GetKeyState(cls, keycode: KeyCode, keystate: KeyState) -> bool: ...
    @classmethod
    def GetMouse(cls, mousecode: MouseCode) -> bool: ...
    @classmethod
    def GetMouseUp(cls, mousecode: MouseCode) -> bool: ...
    @classmethod
    def GetMouseDown(cls, mousecode: MouseCode) -> bool: ...
    @classmethod
    def GetMouseState(cls, mousecode: MouseCode, mousestate: KeyState) -> bool: ...
    @classmethod
    def GetAxis(cls, axis: str) -> float: ...
    @classmethod
    def GetRawAxis(cls, axis: str) -> float: ...
    @classmethod
    def UpdateAxes(cls, dt: float) -> None: ...