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
Pygame is tested last.

To create your own provider, create a
class that has the following methods:

- `__init__`: initiate your window and
    check to see if it works.
- `start`: start the main loop in your
    window. The first parameter is
    ``update_func``, which is called
    when you want to do the OpenGL calls.

Check the source code of any of the window
providers for an example. If you have a
window provider, then please create a new
pull request.

"""

import os
import OpenGL.GLUT, glfw, pygame
from ..errors import *

def glfwCheck():
    """Checks to see if GLFW works"""
    global glfw
    if not glfw.init():
        raise Exception
    glfw.create_window(5, 5, "a", None, None)
    glfw.terminate()
    del glfw

def pygameCheck():
    """Checks to see if Pygame works"""
    global pygame
    if pygame.init()[0] == 0:
        raise Exception
    del pygame

def glutCheck():
    """Checks to see if FreeGLUT works"""
    global OpenGL
    OpenGL.GLUT.glutInit()
    del OpenGL

def LoadWindowProvider():
    """Loads an appropriate window provider to use"""
    winfo = [
        ("GLFW", glfwCheck),
        ("Pygame", pygameCheck),
        ("FreeGLUT", glutCheck),
    ]

    windowProvider = ""
    failed = False
    i = 0

    for name, checker in winfo:
        next = winfo[i + 1][0] if i < len(winfo) - 1 else None
        if os.environ["PYUNITY_DEBUG_MODE"] == "1":
            print("Trying", name, "as a window provider")
        try:
            checker()
            windowProvider = name
        except Exception as e:
            failed = not bool(next)
            if not failed and os.environ["PYUNITY_DEBUG_MODE"] == "1":
                print(name, "doesn't work, trying", next)
        
        if next is None: raise PyUnityException("No window provider found")
        if windowProvider: break
        i += 1

    if os.environ["PYUNITY_DEBUG_MODE"] == "1":
        print(f"Using window provider {windowProvider}")

    if windowProvider == "FreeGLUT":
        from .glutWindow import Window as glutWindow
        return glutWindow
    if windowProvider == "GLFW":
        from .glfwWindow import Window as glfwWindow
        return glfwWindow
    if windowProvider == "Pygame":
        from .pygameWindow import Window as pygameWindow
        return pygameWindow
