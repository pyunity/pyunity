## Copyright (c) 2020-2023 The PyUnity Team
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
    ``updateFunc``, which is called
    when you want to do the OpenGL calls.

Check the source code of any of the window
providers for an example. If you have a
window provider, then please create a new
pull request.

"""

__all__ = ["GetWindowProvider", "SetWindowProvider",
           "CustomWindowProvider", "ABCWindow"]

from typing import Type, TypeVar, TYPE_CHECKING
from .abc import ABCWindow

if TYPE_CHECKING:
    T = TypeVar("T", bound=ABCWindow)

def GetWindowProvider() -> Type[ABCWindow]: ...
def SetWindowProvider(name: str) -> Type[ABCWindow]: ...
def CustomWindowProvider(cls: Type[T]) -> Type[T]: ...
