## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""
A basic 3D Physics engine that uses
similar concepts to the Unity
Engine itself. Only supports
non-rotated colliders.

To create an immoveable object, use
math.inf or the provided :const:`Infinity`
variable. This will make the object
not be able to move, unless you set
an initial velocity. Then, the
collider will either push everything
it collides with, or bounces it back
at twice the speed.

Example
-------

    >>> cube = GameObject("Cube")
    >>> collider = cube.AddComponent(BoxCollider)
    >>> collider.SetSize(-Vector3.one(), Vector3.one())
    >>> collider.velocity = Vector3.right()

Configuration
-------------
If you want to change some configurations, import
the config file like so:

    >>> from pyunity.physics import config

Inside the config file there are some configurations:

- ``gravity`` is the gravity of the whole system. It only
  affects Rigidbodies that have :attr:`Rigidbody.gravity` set to True.

"""

from . import core
from .core import *

__all__ = []
__all__.extend(core.__all__)
