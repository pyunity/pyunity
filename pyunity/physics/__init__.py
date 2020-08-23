"""
A basic 3D Physics engine that uses
similar concepts to the Unity
Engine itself. Only supports
non-rotated colliders.

Example
-------

>>> cube = GameObject("Cube")
>>> collider = cube.AddComponent(AABBoxCollider)
>>> collider.SetSize(-Vector3.one(), Vector3.one())
>>> collider.velocity = Vector3.right()

"""

from .core import *