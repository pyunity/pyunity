# PyUnity

[![Documentation Status](https://readthedocs.org/projects/pyunity/badge/?version=latest)](https://pyunity.readthedocs.io/en/latest/?badge=latest) [![License](https://img.shields.io/pypi/l/pyunity.svg?v=1)](https://pypi.python.org/pypi/pyunity)[![PyPI version](https://img.shields.io/pypi/v/pyunity.svg?v=1)](https://pypi.python.org/pypi/pyunity) [![Python version](https://img.shields.io/pypi/pyversions/pyunity.svg?logo=python&logoColor=FBE072)](https://pypi.python.org/pypi/pyunity) [![Commits since last release](https://img.shields.io/github/commits-since/rayzchen/pyunity/0.2.1.svg)](https://github.com/rayzchen/pyunity/compare/0.2.1...master)[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/rayzchen/pyunity.svg?logo=lgtm)](https://lgtm.com/projects/g/rayzchen/pyunity/context:python)[![AppVeyor Build Status](https://ci.appveyor.com/api/projects/status/ohl61d2vavl37tmj?svg=true)](https://ci.appveyor.com/project/rayzchen/pyunity)

## Version 0.3.0 (in development)

A Python implementation of the Unity Engine
that supports different types of windows.
Still in development.

### Importing
The first step in using PyUnity is always
importing it. A standard way to import is like
so:

    >>> from pyunity import *

Debug information is turned on by default. If
you want to turn it off, set the
PYUNITY_DEBUG_MODE environment variable to ``"0"``.
This is the output with debugging:

    Loaded config
    Trying FreeGLUT as a window provider
    FreeGLUT doesn't work, trying GLFW
    GLFW doesn't work, trying Pygame
    Using window provider Pygame
    Loaded PyUnity version 0.3.0

If debugging is off, there is no output:

    >>> import os
    >>> os.environ["PYUNITY_DEBUG_MODE"] = "0"
    >>> from pyunity import *
    >>> # No output

### Scenes
All PyUnity projects start with a scene. To add
a scene, do this:

    >>> scene = SceneManager.AddScene("Scene 1")

Then, let's move the camera backwards 10 units.

    >>> scene.mainCamera.transform.position = Vector3(0, 0, -10)

Finally, add a cube at the origin:

    >>> cube = GameObject("Cube")
    >>> renderer = cube.AddComponent(MeshRenderer)
    >>> renderer.mesh = Mesh.cube(2)
    >>> renderer.mat = Material((255, 0, 0))
    >>> scene.Add(cube)

To see what you have added to the scene, call ``scene.List()``:

    >>> scene.List()
    /Main Camera
    /Light
    /Cube

Finally, to run the scene, call ``scene.Run()``. The window that
is created is one of FreeGLUT, GLFW or Pygame. The window is
selected on module initialization (see Windows subheading).

### Behaviours
To create your own PyUnity script, create a class that inherits
from Behaviour. Usually in Unity, you would put the class in its
own file, but Python can't do something like that, so put all of
your scripts in one file. Then, to add a script, just use
``AddComponent()``. Do not put anything in the ``__init__`` function,
instead put it in ``Start()``. The ``Update()`` function receives one
parameter, ``dt``, which is the same as ``Time.deltaTime``.

### Windows
The window is provided by one of three
providers: GLFW, Pygame and FreeGLUT.
When you first import PyUnity, it checks
to see if any of the three providers
work. The testing order is as above, so
Pygame is tested last.

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

### Examples
To run an example, import it like so:

    >>> from pyunity.examples.example1 import main
    Loaded config
    Trying FreeGLUT as a window provider
    FreeGLUT doesn't work, trying GLFW
    GLFW doesn't work, trying Pygame
    Using window provider Pygame
    Loaded PyUnity version 0.3.0
    >>> main()

Or from the command line:

    > python -m pyunity 1

The ``1`` just means to load example 1, and there
are 8 examples. To load all examples one by
one, do not specify a number. If you want to
contribute an example, then please
[create a new pull request](https://github.com/rayzchen/pyunity/pulls).


