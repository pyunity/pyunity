"""
Module for all exceptions related to PyUnity.

"""

class PyUnityException(Exception):
    """Base class for PyUnity exceptions."""
    pass

class ComponentException(PyUnityException):
    """Class for PyUnity exceptions relating to components."""
    pass

class GameObjectException(PyUnityException):
    """Class for PyUnity exceptions relating to GameObjects."""
    pass