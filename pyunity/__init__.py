## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""
Version 0.9.0 (in development)
==============================
PyUnity is a pure Python 3D Game Engine that
was inspired by the structure of the Unity
Game Engine. It aims to be as close as possible
to Unity itself. This does not mean that PyUnity
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
use::

    > pip install pyunity

Alternatively, you can clone the repository
`here <https://github.com/pyunity/pyunity>`_
to build the package from source. Then use
``pip`` to install::

    > pip install .

The latest builds are on the ``develop`` branch
which is the default branch. These builds are
sometimes broken, so use at your own risk. ::

    > git clone https://github.com/pyunity/pyunity
    > pip install .

Its only dependencies are PyOpenGL, PySDL2,
Pillow and PyGLM. Microsoft Visual
C++ Build Tools are required on Windows
for building yourself, but it can be disabled by
setting the ``cython`` environment variable to
``0``, at the cost of being less optimized.
GLFW can be optionally installed if you would
like to use the GLFW window provider.

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
    Loaded PyUnity version 0.9.0

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
please `create a pull request <https://github.com/pyunity/pyunity/compare>`_.

Environment variables
---------------------
Here is a list of environment variables used
by PyUnity:

- **PYUNITY_TESTING** (default: unset)
  When set, the following features are either
  disabled or ignored:

  - Window provder selection
  - Audio
  - Font loading

- **PYUNITY_DEBUG_MODE** (default: 1)
  Disables debug output if set to "0".
  Debug output has the code \\|D\\| in the log file.
- **PYUNITY_AUDIO** (default: 1)
  If set to "0", sdlmixer won't be loaded and
  ``config.audio`` is set to ``False``.
- **PYUNITY_GL_CONTEXT** (default: unset)
  Set when the OpenGL context is enabled. Usually
  not used except by wrapper scripts as Behaviours
  only update while a valid context exists.
- **PYUNITY_CHECK_WINDOW** (default: 0)
  If set to "1", forces window provider selection regardless
  if ``windowProvider`` is set in ``settings.json``. If set
  to "0", window provider selection is triggered only if
  ``windowProvider`` doesn't already exist in ``settings.json``.
- **PYUNITY_INTERACTIVE** (default: 1)
  If set to "0", window providing is disabled and scenes
  are run without any OpenGL rendering.
- **PYUNITY_SPHINX_CHECK** (default: unset)
  Used by sphinx to fix some bugs that occur during documentation
  generation.
- **PYUNITY_CHANGE_MODULE** (default: 1)
  Change the ``__module__`` attribute of all imported objects
  to ``pyunity``. If set to "0", this is disabled.

Examples
--------
Examples are located at subfolders in
`pyunity/examples <https://github.com/pyunity/pyunity/tree/develop/pyunity/examples>`_
so do be sure to check them out as a
starting point.

To run an example, import it like so:

    >>> from pyunity.examples.example1 import main
    Loaded config
    Trying FreeGLUT as a window provider
    FreeGLUT doesn't work, trying GLFW
    GLFW doesn't work, trying PySDL2
    Using window provider PySDL2
    Loaded PyUnity version 0.9.0
    >>> main()

Or from the command line::

    > python -m pyunity 1

The ``1`` just means to load example 1, and there
are 9 examples. To load all examples one by
one, do not specify a number. If you want to
contribute an example, then please
`create a pull request <https://github.com/pyunity/pyunity/compare>`_.

"""

__copyright__ = "Copyright (c) 2020-2023 The PyUnity Team"
__email__ = "tankimarshal2@gmail.com"
__license__ = "MIT License"
__summary__ = "A pure Python 3D Game Engine that was inspired by the structure of the Unity Game Engine"
__title__ = "pyunity"
__uri__ = "https://docs.pyunity.x10.bz/en/latest/"

# Window provider selection should be as early as possible
# Logger must start first, config straight after
from . import logger as Logger  # noqa
from . import config  # noqa
from . import window as Window  # noqa
import os

if "PYUNITY_TESTING" not in os.environ:
    config.windowProvider = Window.GetWindowProvider()

__all__ = ["Logger", "Loader", "Window", "Primitives", "Screen",
           "SceneManager"]

from .audio import __all__ as _audio_all
from .core import __all__ as _core_all
from .errors import __all__ as _errors_all
from .events import __all__ as _events_all
from .files import __all__ as _files_all
from .gui import __all__ as _gui_all
from .input import __all__ as _input_all
from .meshes import __all__ as _meshes_all
from .physics import __all__ as _physics_all
from .render import __all__ as _render_all
from .values import __all__ as _values_all

__all__.extend(_errors_all)
__all__.extend(_values_all)
__all__.extend(_core_all)
__all__.extend(_events_all)
__all__.extend(_meshes_all)
__all__.extend(_files_all)
__all__.extend(_render_all)
__all__.extend(_audio_all)
__all__.extend(_physics_all)
__all__.extend(_input_all)
__all__.extend(_gui_all)

from . import loader as Loader
from ._version import __version__
from .audio import *
from .core import *
from .errors import *
from .events import *
from .files import *
from .gui import *
from .input import *
from .loader import Primitives
from .meshes import *
from .physics import *
from .render import *
from .scenes import sceneManager as SceneManager
from .values import *

if ("PYUNITY_SPHINX_CHECK" not in os.environ and
        os.environ["PYUNITY_CHANGE_MODULE"] == "1"):
    # Mask module attribute
    for _obj in tuple(locals().values()): # pragma: no cover
        if not getattr(_obj, "__module__", "").startswith("pyunity."):
            continue
        try:
            _obj.__module__ = "pyunity"
        except AttributeError: # __module__ is read-only
            pass

Logger.LogLine(Logger.DEBUG, f"Loaded PyUnity version {__version__}")
Logger.LogSpecial(Logger.INFO, Logger.ELAPSED_TIME)
