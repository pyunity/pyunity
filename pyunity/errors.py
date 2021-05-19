"""Module for all exceptions and warnings related to PyUnity."""

__all__ = ["PyUnityException", "ComponentException",
           "GameObjectException"]

class PyUnityException(Exception):
    """Base class for PyUnity exceptions."""
    pass

class ComponentException(PyUnityException):
    """Class for PyUnity exceptions relating to components."""
    pass

class GameObjectException(PyUnityException):
    """Class for PyUnity exceptions relating to GameObjects."""
    pass
