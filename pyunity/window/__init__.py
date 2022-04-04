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

__all__ = ["GetWindowProvider", "SetWindowProvider",
           "CustomWindowProvider", "ABCWindow"]

from .providers import getProviders
from ..errors import *
from .. import Logger
from .. import config
from .. import settings
from ..values import ABCMeta, abstractmethod
import os
import importlib.util

def GetWindowProvider():
    """Gets an appropriate window provider to use"""
    if os.environ["PYUNITY_INTERACTIVE"] != "1":
        Logger.LogLine(Logger.DEBUG, "Interactive mode on")
        Logger.LogLine(Logger.DEBUG, "Using no window provider")
        return None
    if "window_provider" in settings.db and "PYUNITY_CHECK_WINDOW" not in os.environ:
        env = os.getenv("PYUNITY_WINDOW_PROVIDER")
        if env is not None:
            env = env.split(",")
            use = settings.db["window_provider"] in env[0]
        else:
            use = True
        if use:
            if "window_cache" in settings.db:
                del settings.db["window_cache"]
            Logger.LogLine(Logger.DEBUG, "Detected settings.json entry")
            providerName = settings.db["window_provider"]
            if providerName in getProviders():
                module = importlib.import_module(f".providers.{providerName}", __name__)
                Logger.LogLine(
                    Logger.DEBUG, "Using window provider", module.name)
                module = importlib.import_module(f".providers.{providerName}.window", __name__)
                return module.Window
            else:
                Logger.LogLine(Logger.WARN,
                               f"settings.json entry {providerName!r} is "
                               f"not a valid window provider, removing")
                settings.db.pop("window_provider")

    windowProvider = ""
    i = 0
    env = os.getenv("PYUNITY_WINDOW_PROVIDER")
    providers = getProviders()
    if env is not None:
        env = env.split(",")
        for specified in reversed(env):
            if specified not in providers:
                Logger.LogLine(Logger.WARN, "PYUNITY_WINDOW_PROVIDER environment variable contains",
                               specified, "but there is no window provider called that")
                continue
            for item in providers:
                if item == specified:
                    selected = item
            providers.remove(selected)
            providers.insert(0, selected)

    if len(providers) == 0:
        raise PyUnityException("No window providers installed")

    module = importlib.import_module(f".providers.{providers[0]}", __name__)
    Logger.LogLine(Logger.DEBUG, "Trying", module.name, "as a window provider")
    for name in providers:
        try:
            module = importlib.import_module(f".providers.{name}", __name__)
            module.check()
            windowProvider = name
        except Exception as e:
            if isinstance(e, ImportError):
                Logger.LogLine(Logger.WARN,
                               name + ": This window manager requires a package "
                               "you don't have installed.")
                Logger.LogLine(Logger.WARN,
                               name + ": Check the source code and use `pip install` "
                               "to resolve any missing dependencies.")
            Logger.LogLine(Logger.DEBUG, name, "doesn't work")
        else:
            if not windowProvider:
                raise PyUnityException("No window provider found")

        if windowProvider:
            break
        i += 1

    settings.db["window_provider"] = windowProvider
    settings.db["window_cache"] = True
    module = importlib.import_module(f".providers.{windowProvider}", __name__)
    Logger.LogLine(Logger.DEBUG, "Using window provider", module.name)
    try:
        module = importlib.import_module(f".providers.{windowProvider}.window", __name__)
    except Exception:
        Logger.LogLine(Logger.WARN, "window_cache entry has been set, indicating "
                                    "window checking happened on this import")
        Logger.LogLine(
            Logger.WARN, "settings.json entry may be faulty, removing")
        settings.db.pop("window_provider")
        raise
    return module.Window

def SetWindowProvider(name):
    providers = getProviders()
    if name not in providers:
        raise PyUnityException(f"No window provider named {name!r} found")
    modname = providers[name]
    module = importlib.import_module(f".providers.{modname}", __name__)
    exc = None
    try:
        module.check()
    except Exception as e:
        if isinstance(e, ImportError):
            Logger.LogLine(Logger.WARN,
                           modname + ": This window manager requires on a package "
                           "you don't have installed.")
            Logger.LogLine(Logger.WARN,
                           modname + ": Check the source code and use `pip install` "
                           "to resolve any missing dependencies.")
        exc = e
    if exc is not None:
        raise PyUnityException(f"Cannot use window provider {module.name!r}")
    Logger.LogLine(Logger.DEBUG, "Using window provider", module.name)
    module = importlib.import_module(f".providers.{modname}.window", __name__)
    config.windowProvider = module.Window
    return module.Window

def CustomWindowProvider(cls):
    if not isinstance(cls, type):
        raise PyUnityException("Provided window provider is not a class")
    if not issubclass(cls, ABCWindow):
        raise PyUnityException(
            "Provided window provider does not subclass ABCWindow")
    Logger.LogLine(Logger.DEBUG, "Using window provider", cls.__name__)
    config.windowProvider = cls
    return cls

class ABCWindow(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, name, resize):
        pass

    @abstractmethod
    def get_mouse(self, mousecode, keystate):
        pass

    @abstractmethod
    def get_key(self, keycode, keystate):
        pass

    @abstractmethod
    def get_mouse_pos(self):
        pass

    @abstractmethod
    def refresh(self):
        pass

    @abstractmethod
    def quit(self):
        pass

    @abstractmethod
    def start(self, update_func):
        pass
