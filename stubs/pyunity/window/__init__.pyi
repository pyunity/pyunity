## Copyright (c) 2020-2022 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""
A module used to load the window providers.

The window is provided by one of three
providers: GLFW, PySDL2 and GLUT.
When you first import PyUnity, it checks
to see if any of the three providers
work. The testing order is as above, so
GLUT is tested last.

To create your own provider, create a
class that has the following methods:

- ``__init__``: initiate your window and
    check to see if it works.
- ``start``: start the main loop in your
    window. The first parameter is
    ``update_func``, which is called
    when you want to do the OpenGL calls.

Check the source code of any of the window
providers for an example. If you have a
window provider, then please create a new
pull request.

"""

from types import ModuleType
from typing import Callable, Dict, Tuple, Type, TypeVar
from ..values import ABCMeta, abstractmethod
from ..input import KeyCode, KeyState, MouseCode

def checkModule(name: str) -> ModuleType: ...
def glfwCheck() -> None: ...
def sdl2Check() -> None: ...
def glutCheck() -> None: ...

providers: Dict[str, Tuple[str, Callable[[], None]]] = ...

def GetWindowProvider() -> ModuleType: ...
def SetWindowProvider(name: str) -> ModuleType: ...
T = TypeVar("T")
def CustomWindowProvider(cls: Type[T]) -> Type[T]: ...

class ABCWindow(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, name: str, resize: Callable[[int, int], None]) -> None: ...
    @abstractmethod
    def get_mouse(self, mousecode: MouseCode, keystate) -> None: ...
    @abstractmethod
    def get_key(self, keycode: KeyCode, keystate: KeyState) -> None: ...
    @abstractmethod
    def get_mouse_pos(self) -> None: ...
    @abstractmethod
    def quit(self) -> None: ...
    @abstractmethod
    def start(self, update_func: Callable[[float], None]) -> None: ...
