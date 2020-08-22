"""
Module for all exceptions related to PyUnity.

"""

class PyUnity(Exception):
    """Base class for PyUnity exceptions."""
    pass

class ComponentException(PyUnity):
    """Class for PyUnity exceptions relating to components."""
    pass

class GameObjectException(PyUnity):
    """Class for PyUnity exceptions relating to GameObjects."""
    pass