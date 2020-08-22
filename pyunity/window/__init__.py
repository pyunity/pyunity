"""
pyunity.window
==============
A module used to load the window providers.

Windows
-------
Only one window can be used at a time. The window is provided by
one of three providers: FreeGLUT, GLFW and Pygame. To create your
own provider, create a class that has the following methods:

- `__init__`: initiate your window and check to see if it works.
- `start`: start the main loop in your window. The first parameter
    is ``update_func``, which is called when you want to do the OpenGL calls.

"""

import os
from .pygameWindow import Window as pygameWindow
from .glutWindow import Window as glutWindow
from .glfwWindow import Window as glfwWindow

if os.environ["PYUNITY_DEBUG_MODE"] == "1":
    print("Loaded window providers")