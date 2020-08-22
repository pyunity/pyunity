"""
PyUnity
=======

A Python port of the Unity Engine, written in
pure Python.

How to use
----------
The first step in using PyUnity is always
importing it. A standard way to import is like
so:

    >>> from pyunity import *

If you want debug information, set the
PYUNITY_DEBUG_MODE environment variable to "1".
This is the output:

    >>> import os
    >>> os.environ["PYUNITY_DEBUG_MODE"] = "1"
    >>> from pyunity import *
    Loaded window providers
    Loaded config
    Trying FreeGLUT as a window provider
    FreeGLUT doesn't work, trying GLFW
    GLFW doesn't work, trying Pygame
    Loaded PyUnity version 0.0.3
    Using window provider Pygame

The next step is to create a scene. The SceneManager
has already been created, so add a scene like so:

    >>> scene = SceneManager.AddScene("Scene 1")

Then, let's move the camera backwards 10 units.

    >>> scene.mainCamera.transform.position = Vector3(0, 0, -10)

Finally, add a cube at the origin:

    >>> cube = GameObject("Cube")
    >>> renderer = cube.AddComponent(MeshRenderer)
    >>> renderer.mesh = Mesh.cube(2)
    >>> renderer.mat = Material((255, 0, 0))
    >>> scene.Add(cube)

To see what you have added to the scene, call `scene.List()`:

    >>> scene.List()
    /Main Camera
    /Light
    /Cube

Finally, to run the scene, call `scene.Run()`. The window that
is created is one of FreeGLUT, GLFW or Pygame, in which the
precedence is as above.

Behaviours
----------
To create your own PyUnity script, create a class that inherits
from Behaviour. Usually in Unity, you would put the class in its
own file, but Python can't do something like that, so put all of
your scripts in one file. Then, to add a script, just use
`AddComponent()`. Do not put anything in the `__init__` function,
instead put it in `Start()`. The `Update()` function receives one
parameter, `dt`, which is the same as Time.deltaTime.

Windows
-------
Only one window can be used at a time. The window is provided by
one of three providers: FreeGLUT, GLFW and Pygame. To create your
own provider, create a class that has the following methods:

- `__init__`: initiate your window and check to see if it works.
- `start`: start the main loop in your window. The first parameter
    is `update_func`_, which is called when you want to do the OpenGL calls.

"""

import os
from . import config
from .core import *
from .vector3 import Vector3
from .scene import SceneManager
from .errors import *

__version__ = "0.0.3"

try:
    if os.environ["PYUNITY_DEBUG_MODE"] == "1":
        print("Trying FreeGLUT as a window provider")
    from OpenGL.GLUT import *
    glutInit()
    config.windowProvider = "glut"
    w = "FreeGLUT"
except Exception as e:
    if os.environ["PYUNITY_DEBUG_MODE"] == "1":
        print("FreeGLUT doesn't work, using GLFW")
    try:
        import glfw
        if not glfw.init():
            raise Exception
        glfw.create_window(50, 50, "Test", None, None)
        glfw.terminate()
        config.windowProvider = "glfw"
        w = "GLFW"
    except Exception as e:
        if os.environ["PYUNITY_DEBUG_MODE"] == "1":
            print("GLFW doesn't work, using Pygame")
        import pygame
        if pygame.init()[0] == 0:
            raise PyUnityException("No window provider found")
        config.windowProvider = "pygame"
        w = "Pygame"

SceneManager = SceneManager()

if os.environ["PYUNITY_DEBUG_MODE"] == "1":
    print(f"Loaded PyUnity version {__version__}")
    print(f"Using window provider {w}")