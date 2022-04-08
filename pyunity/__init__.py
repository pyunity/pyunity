# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

"""
Version 0.8.3 (in development)
==============================
PyUnity is a pure Python 3D Game Engine that
was inspired by the structure of the Unity
Game Engine. This does not mean that PyUnity
are bindings for the UnityEngine. However,
this project has been made to facilitate
any programmer, beginner or advanced, novice
or veteran.

Disclaimer
----------
As we have said above, this is not a set of
bindings for the UnityEngine, but a pure
Python library to aid in making 3D games in
Python.

Installing
----------
To install PyUnity for Linux distributions
based on Ubuntu or Debian, use::

    > pip3 install pyunity

To install PyUnity for other operating systems,
use pip::

    > pip install pyunity

Alternatively, you can clone the repository
`here <https://github.com/pyunity/pyunity>`_
to build the package from source. Then use
``setup.py`` to build. Note that it will install
Cython to compile.

    > python setup.py install

The latest builds are on the ``develop`` branch
which is the default branch. These builds are
sometimes broken, so use at your own risk.

    > git clone https://github.com/pyunity/pyunity
    > python setup.py install

Its only dependencies are PyOpenGL, PySDL2,
Pillow and PyGLM. Microsoft Visual
C++ Build Tools are required on Windows
for building yourself. GLFW can be optionally
installed if you would like to use the GLFW
window provider.

Importing
---------
To start using PyUnity, you must import it.
A standard way to import is like so:

    >>> from pyunity import *

Debug information is turned on by default. If
you want to turn it off, set the
PYUNITY_DEBUG_MODE environment variable to ``"0"``.
This is the output with debugging::

    Loaded config
    Trying GLFW as a window provider
    GLFW doesn't work, trying PySDL2
    Using window provider PySDL2
    Loaded PyUnity version 0.8.3

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
    >>> renderer.mat = Material(RGB(255, 0, 0))
    >>> scene.Add(cube)

To see what you have added to the scene, call ``scene.List()``:

    >>> scene.List()
    /Main Camera
    /Light
    /Cube

Finally, to run the scene, call ``scene.Run()``. The window that
is created is one of FreeGLUT, GLFW or PySDL2. The window is
selected on module initialization (see Windows subheading).

Behaviours
----------
To create your own PyUnity script, create a class that inherits
from Behaviour. Usually in Unity, you would put the class in its
own file, but Python can't do something like that, so put all of
your scripts in one file. Then, to add a script, just use
``AddComponent()``. Do not put anything in the ``__init__`` function,
instead put it in ``Start()``. The ``Update()`` function receives one
parameter, ``dt``, which is the same as ``Time.deltaTime`` in Unity.

Windows
-------
The window is provided by one of three
providers: GLFW, PySDL2 and FreeGLUT.
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
providers for an example. If you would like
to contribute a new window provider, then
please `create a pull request <https://github.com/pyunity/pyunity/compare>`.

Examples
--------
To run an example, import it like so:

    >>> from pyunity.examples.example1 import main
    Loaded config
    Trying FreeGLUT as a window provider
    FreeGLUT doesn't work, trying GLFW
    GLFW doesn't work, trying PySDL2
    Using window provider PySDL2
    Loaded PyUnity version 0.8.3
    >>> main()

Or from the command line::

    > python -m pyunity 1

The ``1`` just means to load example 1, and there
are 9 examples. To load all examples one by
one, do not specify a number. If you want to
contribute an example, then please
`create a pull request <https://github.com/pyunity/pyunity/compare>`.

"""

# Logger must start first, config straight after
from . import logger as Logger # lgtm[py/import-own-module]
from . import config # lgtm[py/import-own-module]
__all__ = ["Logger", "Loader", "Window", "Primitives", "Screen",
           "SceneManager", "Mesh"]

from .errors import __all__ as _errors_all
from .values import __all__ as _values_all
from .core import __all__ as _core_all
from .files import __all__ as _files_all
from .render import __all__ as _render_all
from .audio import __all__ as _audio_all
from .physics import __all__ as _physics_all
from .input import __all__ as _input_all
from .gui import __all__ as _gui_all
__all__.extend(_errors_all)
__all__.extend(_values_all)
__all__.extend(_core_all)
__all__.extend(_files_all)
__all__.extend(_render_all)
__all__.extend(_audio_all)
__all__.extend(_physics_all)
__all__.extend(_input_all)
__all__.extend(_gui_all)

import os
from .errors import *
from .values import *
from .meshes import Mesh
from .core import *
from .physics import *
from .audio import *
from .files import *
from .render import *
from .scenes import sceneManager as SceneManager
from . import window as Window # lgtm[py/import-own-module]
from . import loader as Loader # lgtm[py/import-own-module]
from .loader import Primitives
from .input import *
from .gui import *
from ._version import __version__

__copyright__ = "Copyright 2020-2021 Ray Chen"
__email__ = "tankimarshal2@gmail.com"
__license__ = "MIT License"
__summary__ = "A pure Python 3D Game Engine that was inspired by the structure of the Unity Game Engine"
__title__ = "pyunity"
__uri__ = "https://pyunity.readthedocs.io/en/latest/"

if "PYUNITY_TESTING" not in os.environ:
    config.windowProvider = Window.GetWindowProvider()
    Logger.LogSpecial(Logger.INFO, Logger.ELAPSED_TIME)

for _obj in tuple(locals().values()): # pragma: no cover
    if not getattr(_obj, "__module__", "").startswith("pyunity."):
        continue
    try:
        _obj.__module__ = "pyunity"
    except AttributeError: # __module__ is read-only
        pass

Logger.LogLine(Logger.DEBUG, "Loaded PyUnity version %s" % __version__)
Logger.LogSpecial(Logger.INFO, Logger.ELAPSED_TIME)
