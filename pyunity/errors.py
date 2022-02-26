"""Module for all exceptions and warnings related to PyUnity."""

__all__ = ["PyUnityException", "ComponentException",
           "GameObjectException", "ProjectParseException"]

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