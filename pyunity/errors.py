"""Module for all exceptions related to PyUnity."""

__all__ = ["PyUnityException", "ComponentException", "GameObjectException", "PyUnityWarning"]

class PyUnityException(Exception):
    """Base class for PyUnity exceptions."""
    pass

class ComponentException(PyUnityException):
    """Class for PyUnity exceptions relating to components."""
    pass

class GameObjectException(PyUnityException):
    """Class for PyUnity exceptions relating to GameObjects."""
    pass

class PyUnityWarning(Warning):
    """Base class for PyUnity warnings."""
    pass