## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""
Abstract base class for window providers.
Imported into ``pyunity.Window``.

"""

__all__ = ["ABCWindow"]

from typing import Callable, Tuple
from ..values import ABCMeta, abstractmethod
from ..input import KeyCode, KeyState, MouseCode

class ABCWindow(metaclass=ABCMeta):
    def __init__(self, name: str) -> None: ...
    @abstractmethod
    def setResize(self, resize: Callable[[int, int], None]) -> None: ...
    @abstractmethod
    def getMouse(self, mousecode: MouseCode, keystate: KeyState) -> bool: ...
    @abstractmethod
    def getKey(self, keycode: KeyCode, keystate: KeyState) -> bool: ...
    @abstractmethod
    def getMousePos(self) -> Tuple[int, int]: ...
    @abstractmethod
    def refresh(self) -> None: ...
    @abstractmethod
    def updateFunc(self) -> None: ...
    @abstractmethod
    def quit(self) -> None: ...
