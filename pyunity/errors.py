## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""Module for all exceptions and warnings related to PyUnity."""

__all__ = ["PyUnityException", "ComponentException",
           "GameObjectException", "ProjectParseException",
           "PyUnityExit", "WindowProviderException"]

class PyUnityException(Exception):
    """Base class for PyUnity exceptions."""
    pass

class ComponentException(PyUnityException):
    """Class for PyUnity exceptions relating to components."""
    pass

class GameObjectException(PyUnityException):
    """Class for PyUnity exceptions relating to GameObjects."""
    pass

class ProjectParseException(PyUnityException):
    """Class for PyUnity project parsing exceptions."""
    pass

class PyUnityExit(PyUnityException):
    """
    Exception for breaking out of the main loop and shutting PyUnity down.

    Only used internally, do not raise outside of the module.

    """
    pass

class WindowProviderException(PyUnityException):
    """Class for PyUnity window provider exceptions."""
    pass
