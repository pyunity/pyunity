# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

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
    ``updateFunc``, which is called
    when you want to do the OpenGL calls.

Check the source code of any of the window
providers for an example. If you have a
window provider, then please create a new
pull request.

"""

__all__ = ["GetWindowProvider", "SetWindowProvider",
           "CustomWindowProvider", "ABCWindow"]

from .providers import getProviders
from ..errors import PyUnityException
from .. import Logger
from .. import config
from .. import settings
from ..values import ABCMeta, abstractmethod
import os
import importlib.util

def GetWindowProvider():
    """Gets an appropriate window provider to use"""
    if os.environ["PYUNITY_INTERACTIVE"] != "1":
        Logger.LogLine(Logger.DEBUG, "Using no window provider")
        return None
    if "windowProvider" in settings.db and "PYUNITY_CHECK_WINDOW" not in os.environ:
        env = os.getenv("PYUNITY_WINDOW_PROVIDER")
        if env is not None:
            env = env.split(",")
            use = settings.db["windowProvider"] in env[0]
        else:
            use = True
        if use:
            if "windowCache" in settings.db:
                del settings.db["windowCache"]
            Logger.LogLine(Logger.DEBUG, "Detected settings.json entry")
            providerName = settings.db["windowProvider"]
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
                settings.db.pop("windowProvider")

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

    windowProvider = ""
    module = importlib.import_module(f".providers.{providers[0]}", __name__)
    Logger.LogLine(Logger.DEBUG, "Trying", module.name, "as a window provider")
    for i, name in enumerate(providers):
        try:
            module.check()
            windowProvider = name
        except Exception as e:
            if isinstance(e, ImportError):
                Logger.LogLine(Logger.WARN,
                               name + ": This window manager requires a "
                               "package that you haven't installed.")
                Logger.LogLine(Logger.WARN, name +
                               ": Check the source code and use `pip install` "
                               "to resolve any missing dependencies.")
            if i == len(providers) - 1:
                Logger.LogLine(Logger.DEBUG, module.name, "doesn't work")
                break
            else:
                newModule = importlib.import_module(f".providers.{providers[i+1]}", __name__)
                Logger.LogLine(Logger.DEBUG,
                               module.name, "doesn't work, trying", newModule.name)
                module = newModule

        if windowProvider:
            break

    if not windowProvider:
        raise PyUnityException(f"No window provider found")

    settings.db["windowProvider"] = windowProvider
    settings.db["windowCache"] = True
    module = importlib.import_module(f".providers.{windowProvider}", __name__)
    Logger.LogLine(Logger.DEBUG, "Using window provider", module.name)
    try:
        module = importlib.import_module(f".providers.{windowProvider}.window", __name__)
    except Exception:
        Logger.LogLine(Logger.WARN, "windowCache entry has been set, indicating "
                                    "window checking happened on this import")
        Logger.LogLine(
            Logger.WARN, "settings.json entry may be faulty, removing")
        settings.db.pop("windowProvider")
        raise
    return module.Window

def SetWindowProvider(name):
    providers = getProviders()
    if name not in providers:
        raise PyUnityException(f"No window provider named {name!r} found")
    module = importlib.import_module(f".providers.{name}", __name__)
    exc = None
    try:
        module.check()
    except Exception as e:
        if isinstance(e, ImportError):
            Logger.LogLine(Logger.WARN,
                           name + ": This window manager requires on a package "
                           "you don't have installed.")
            Logger.LogLine(Logger.WARN,
                           name + ": Check the source code and use `pip install` "
                           "to resolve any missing dependencies.")
        exc = e
    if exc is not None:
        raise PyUnityException(f"Cannot use window provider {module.name!r}")
    Logger.LogLine(Logger.DEBUG, "Using window provider", module.name)
    module = importlib.import_module(f".providers.{name}.window", __name__)
    config.windowProvider = module.Window
    return module.Window

def CustomWindowProvider(cls):
    if not isinstance(cls, type):
        raise PyUnityException("Provided window provider is not a class")
    if not issubclass(cls, ABCWindow):
        raise PyUnityException(
            "Provided window provider does not subclass Window.ABCWindow")
    Logger.LogLine(Logger.DEBUG, "Using window provider", cls.__name__)
    config.windowProvider = cls
    return cls

class ABCWindow(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, name, resize):
        pass

    @abstractmethod
    def getMouse(self, mousecode, keystate):
        pass

    @abstractmethod
    def getKey(self, keycode, keystate):
        pass

    @abstractmethod
    def getMousePos(self):
        pass

    @abstractmethod
    def refresh(self):
        pass

    @abstractmethod
    def quit(self):
        pass

    @abstractmethod
    def start(self, updateFunc):
        pass
