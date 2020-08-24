"""
Version 0.0.3 (in development)
==============================

A Python implementation of the Unity Engine
that can be used with other Python modules,
and supports different types of windows.
Still in development.

Importing
---------
The first step in using PyUnity is always
importing it. A standard way to import is like
so:

    >>> from pyunity import *

Debug information is turned on by default. If
you want to turn it off, set the
PYUNITY_DEBUG_MODE environment variable to "0".
This is the output with debugging:

    >>> import os
    >>> os.environ["PYUNITY_DEBUG_MODE"] = "1"
    >>> from pyunity import *
    Loaded config
    Trying FreeGLUT as a window provider
    FreeGLUT doesn't work, trying GLFW
    GLFW doesn't work, trying Pygame
    Using window provider Pygame
    Loaded PyUnity version 0.0.3

Without debugging on, there is no output.

Scenes
------
All PyUnity projects start with a scene. There
is no way to change between scenes yet.

To add a scene, do this:

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
is created is one of FreeGLUT, GLFW or Pygame. The window is
selected on startup (see Windows subheading).

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

Examples
--------
To run an example, import it like so:

    >>> from pyunity.examples.example1 import main
    Loaded config
    Trying FreeGLUT as a window provider
    FreeGLUT doesn't work, trying GLFW
    GLFW doesn't work, trying Pygame
    Using window provider Pygame
    Loaded PyUnity version 0.0.3
    >>> main()

Or from the command line:

    $ python -m pyunity 1

The ``1`` just means to load example 1, and there
are 5 examples. If you want to contribute an
example, then please create a new pull request.

"""

import os
from . import config
from .core import *
from .vector3 import *
from .scene import SceneManager
from .physics import *
from . import loader

__version__ = "0.0.3"

SceneManager = SceneManager()

del core, errors, meshes, scene, vector3, window, physics

if os.environ["PYUNITY_DEBUG_MODE"] == "1":
    print(f"Loaded PyUnity version {__version__}")

del os