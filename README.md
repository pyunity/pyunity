# pyunity
## Version 0.0.3 (in development)

[![Documentation Status](https://readthedocs.org/projects/pyunity/badge/?version=latest)](https://pyunity.readthedocs.io/en/latest/?badge=latest)

A Python implementation of the Unity Engine, that can be used with other Python modules, and supports different types of windowing. Still in development.

### How to use
The first step in using pyunity is always
importing it. A standard way to import is like
so:

    >>> from pyunity import *

Debug information is turned on by default. If
you want to turn it off, set the
pyunity_DEBUG_MODE environment variable to "0".
This is the output with debugging:

    >>> import os
    >>> os.environ["pyunity_DEBUG_MODE"] = "1"
    >>> from pyunity import *
    Trying FreeGLUT as a window provider
    FreeGLUT doesn't work, trying GLFW
    GLFW doesn't work, trying Pygame
    Using window provider Pygame
    Loaded pyunity version 0.0.3

Without debugging on, there is no output.

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

### Behaviours
To create your own pyunity script, create a class that inherits
from Behaviour. Usually in Unity, you would put the class in its
own file, but Python can't do something like that, so put all of
your scripts in one file. Then, to add a script, just use
`AddComponent()`. Do not put anything in the `__init__` function,
instead put it in `Start()`. The `Update()` function receives one
parameter, `dt`, which is the same as Time.deltaTime.

### Windows
Only one window can be used at a time. The window is provided by
one of three providers: FreeGLUT, GLFW and Pygame. To create your
own provider, create a class that has the following methods:

- `__init__`: initiate your window and check to see if it works.
- `start`: start the main loop in your window. The first parameter
    is ``update_func``, which is called when you want to do the OpenGL calls.