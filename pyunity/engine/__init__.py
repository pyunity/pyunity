from .core import *
from .vector3 import Vector3
from .scene import SceneManager
from . import meshes

__version__ = "0.0.1"

SceneManager = SceneManager()

print(f"Loaded PyUnity version {__version__}")