"""
A module used to load the window providers.

The window is provided by one of three
providers: GLFW, PySDL2 and GLUT.
When you first import PyUnity, it checks
to see if any of the three providers
work. The testing order is as above, so
GLUT is tested last.

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

__all__ = ["GetWindowProvider", "SetWindowProvider", "CustomWindowProvider"]

from ..errors import *
from .. import Logger
from .. import config
from .. import settings
import os
import sys
import importlib.util

def checkModule(module):
    if os.getenv("PYUNITY_TESTING") is not None:
        return sys.modules[module]
    spec = importlib.util.find_spec(module)
    if spec is None:
        raise PyUnityException
    return importlib.util.module_from_spec(spec)

def glfwCheck():
    """Checks to see if GLFW works"""
    glfw = checkModule("glfw")
    if not glfw.init():
        raise PyUnityException
    glfw.create_window(5, 5, "a", None, None)
    glfw.terminate()

def sdl2Check():
    """Checks to see if PySDL2 works"""
    sdl2 = checkModule("sdl2")
    if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
        raise PyUnityException

def glutCheck():
    """Checks to see if GLUT works"""
    checkModule("OpenGL.GLUT")
    import OpenGL.GLUT
    OpenGL.GLUT.glutInit()


providers = {
    "GLFW": ("glfwWindow", glfwCheck),
    "PySDL2": ("sdl2Window", sdl2Check),
    "GLUT": ("glutWindow", glutCheck),
}

def GetWindowProvider():
    """Gets an appropriate window provider to use"""
    if "window_provider" in settings.db:
        if "window_cache" in settings.db:
            del settings.db["window_cache"]
        Logger.LogLine(Logger.DEBUG, "Detected settings.json entry")
        windowProvider = settings.db["window_provider"]
        Logger.LogLine(Logger.DEBUG, "Using window provider", windowProvider)
        return importlib.import_module("." + providers[windowProvider][0], __name__)

    windowProvider = ""
    i = 0
    winfo = list(map(lambda x: (x[0], x[1][1]), providers.items()))
    env = os.getenv("PYUNITY_WINDOW_PROVIDER")
    if env is not None:
        env = env.split(",")
        for specified in reversed(env):
            if specified not in providers:
                Logger.LogLine(Logger.DEBUG, "PYUNITY_WINDOW_PROVIDER environment variable contains",
                    specified, "but there is no window provider called that")
                continue
            for item in winfo:
                if item[0] == specified:
                    selected = item
            winfo.remove(selected)
            winfo.insert(0, selected)

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

    settings.db["window_provider"] = windowProvider
    settings.db["window_cache"] = True
    Logger.LogLine(Logger.DEBUG, "Using window provider", windowProvider)
    return importlib.import_module("." + providers[windowProvider][0], __name__)

def SetWindowProvider(name):
    if name not in providers:
        raise PyUnityException(
            "No window provider named " + repr(name) + " found")
    module, checker = providers[name]
    e = None
    try:
        checker()
    except Exception as e:
        pass
    if e is not None:
        raise PyUnityException("Cannot use window provider " + repr(name))
    Logger.LogLine(Logger.DEBUG, "Using window provider", name)
    window = importlib.import_module("." + module, __name__)
    config.windowProvider = window
    return window

def CustomWindowProvider(cls):
    Logger.LogLine(Logger.DEBUG, "Using window provider", cls.__name__)
    config.windowProvider = cls
    return cls
