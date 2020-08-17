from .core import *
from .vector3 import Vector3
from . import scene
from . import meshes

__version__ = "0.0.1"

SceneManager = scene.SceneManager()

print(f"Loaded PyUnity version {__version__}")