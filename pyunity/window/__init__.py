"""
pyunity.window
==============
A module used to load the window providers.

Windows
-------
The window is provided by one of three
providers: GLFW, Pygame and FreeGLUT.
When you first import PyUnity, it checks
to see if any of the three providers
work. The testing order is as above, so
FreeGLUT is tested last.

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

from .pygameWindow import Window as pygameWindow
from .glfwWindow import Window as glfwWindow
from .glutWindow import Window as glutWindow
from ..errors import *
from .. import Logger
import os
import OpenGL.GLUT
import glfw
import pygame
glfw.ERROR_REPORTING = True


window_providers = {"FreeGLUT": glutWindow,
                    "GLFW": glfwWindow, "Pygame": pygameWindow}

def glfwCheck():
    """Checks to see if GLFW works"""
    if not glfw.init():
        raise Exception
    glfw.create_window(5, 5, "a", None, None)
    glfw.terminate()

def pygameCheck():
    """Checks to see if Pygame works"""
    if pygame.init()[0] == 0:
        raise Exception

def glutCheck():
    """Checks to see if FreeGLUT works"""
    OpenGL.GLUT.glutInit()

def GetWindowProvider():
    """Gets an appropriate window provider to use"""
    winfo = [
        ("GLFW", glfwCheck),
        ("Pygame", pygameCheck),
        ("FreeGLUT", glutCheck),
    ]

    windowProvider = ""
    i = 0

    for name, checker in winfo:
        next = winfo[i + 1][0] if i < len(winfo) - 1 else None
        Logger.LogLine(Logger.DEBUG, "Trying", name, "as a window provider")
        try:
            checker()
            windowProvider = name
        except Exception as e:
            if next is not None:
                Logger.LogLine(Logger.DEBUG, name,
                               "doesn't work, trying", next)

        if next is None:
            raise PyUnityException("No window provider found")
        if windowProvider:
            break
        i += 1

    if os.environ["PYUNITY_DEBUG_MODE"] == "1":
        Logger.LogLine(Logger.DEBUG, "Using window provider", windowProvider)

    return windowProvider
