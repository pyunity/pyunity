from .core import *
from .vector3 import Vector3
from .scene import SceneManager
from . import meshes
from . import config
from . import errors

__version__ = "0.0.1"

try:
    from OpenGL.GLUT import *
    glutInit()
    config.windowProvider = "glut"
except:
    print("GLUT doesn't work, using GLFW")
    import glfw
    try:
        if not glfw.init():
            raise Exception
        glfw.create_window((50, 50), "Test", None, None)
        glfw.terminate()
        config.windowProvider = "glfw"
    except:
        print("GLFW doesn't work, using Pygame")
        import pygame
        if not pygame.init():
            raise PyUnityException("No window provider found")
        config.windowProvider = "pygame"

SceneManager = SceneManager()

print(f"Loaded PyUnity version {__version__}")