"""
Version 0.5.1 (in development)
==============================
PyUnity is a Python implementation of the
Unity Engine, written in C++. This is just
a fun project and many features have been
taken out to make it as easy as possible
to create a scene and run it.

Installing
----------
To install PyUnity for Linux distributions
based on Ubuntu or Debian, use::

    > pip3 install pyunity

To install PyUnity for other operating systems,
use pip::

    > pip install pyunity

Alternatively, you can clone the repository
`here <https://github.com/rayzchen/pyunity>`_
to build the package from source. Then use
``setup.py`` to build. Note that it will install
Cython to compile.

    > python setup.py install

Its only dependencies are PyOpenGL, Pygame,
GLFW, Pillow and PyGLM.

Importing
---------
To start using pyunity, you must import it.
A standard way to import is like so:

    >>> from pyunity import *

Debug information is turned on by default. If
you want to turn it off, set the
PYUNITY_DEBUG_MODE environment variable to ``"0"``.
This is the output with debugging::

    Loaded config
    Trying GLFW as a window provider
    GLFW doesn't work, trying Pygame
    Using window provider Pygame
    Loaded PyUnity version 0.5.1

If debugging is off, there is no output:

    >>> import os
    >>> os.environ["PYUNITY_DEBUG_MODE"] = "0"
    >>> from pyunity import *
    >>> # No output

Scenes
------
All PyUnity projects start with a scene. To add
a scene, do this:

    >>> scene = SceneManager.AddScene("Scene 1")

Then, let's move the camera backwards 10 units.

    >>> scene.mainCamera.transform.position = Vector3(0, 0, -10)

Finally, add a cube at the origin:

    >>> cube = GameObject("Cube")
    >>> renderer = cube.AddComponent(MeshRenderer)
    >>> renderer.mesh = Mesh.cube(2)
    >>> renderer.mat = Material(Color(255, 0, 0))
    >>> scene.Add(cube)

To see what you have added to the scene, call ``scene.List()``:

    >>> scene.List()
    /Main Camera
    /Light
    /Cube

Finally, to run the scene, call ``scene.Run()``. The window that
is created is one of FreeGLUT, GLFW or Pygame. The window is
selected on module initialization (see Windows subheading).

Behaviours
----------
To create your own PyUnity script, create a class that inherits
from Behaviour. Usually in Unity, you would put the class in its
own file, but Python can't do something like that, so put all of
your scripts in one file. Then, to add a script, just use
``AddComponent()``. Do not put anything in the ``__init__`` function,
instead put it in ``Start()``. The ``Update()`` function receives one
parameter, ``dt``, which is the same as ``Time.deltaTime``.

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

Examples
--------
To run an example, import it like so:

    >>> from pyunity.examples.example1 import main
    Loaded config
    Trying FreeGLUT as a window provider
    FreeGLUT doesn't work, trying GLFW
    GLFW doesn't work, trying Pygame
    Using window provider Pygame
    Loaded PyUnity version 0.5.1
    >>> main()

Or from the command line::

    > python -m pyunity 1

The ``1`` just means to load example 1, and there
are 9 examples. To load all examples one by
one, do not specify a number. If you want to
contribute an example, then please
create a new pull request.

"""

from . import logger as Logger  # lgtm[py/import-own-module]
from .audio import *
from .core import *
from .script import Behaviour
from . import loader as Loader  # lgtm[py/import-own-module]
from . import input as Input  # lgtm[py/import-own-module]
from .input import KeyCode
from .physics import *
from .errors import *
from .files import *
from .scenes import sceneManager as SceneManager
from .quaternion import Quaternion
from .vector3 import Vector3
from .meshes import Mesh

__version__ = "0.5.1"
__copyright__ = "Copyright 2020-2021 Ray Chen"
__email__ = "tankimarshal2@gmail.com"
__license__ = "MIT License"
__summary__ = "A Python implementation of the Unity Engine that supports different types of windows."
__title__ = "pyunity"
__uri__ = "https://pyunity.readthedocs.io/en/latest/"

from . import audio, core, physics, errors, files
__all__ = ["__version__", "Vector3", "Quaternion",
           "SceneManager", "Mesh", "Loader",
           "Input", "KeyCode", "Logger",
           "Behaviour"]
__all__.extend(audio.__all__)
__all__.extend(core.__all__)
__all__.extend(physics.__all__)
__all__.extend(errors.__all__)
__all__.extend(files.__all__)

Logger.LogLine(Logger.DEBUG, "Loaded PyUnity version %s" % __version__)
Logger.LogSpecial(Logger.INFO, Logger.RUNNING_TIME)
