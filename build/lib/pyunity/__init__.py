from . import config
from .core import *
from .vector3 import Vector3
from .scene import SceneManager
from . import errors

__version__ = "0.0.1"

try:
    from OpenGL.GLUT import *
    glutInit()
    config.windowProvider = "glut"
    w = "FreeGLUT"
except Exception as e:
    print("GLUT doesn't work, using GLFW")
    try:
        import glfw
        if not glfw.init():
            raise Exception
        glfw.create_window(50, 50, "Test", None, None)
        glfw.terminate()
        config.windowProvider = "glfw"
        w = "GLFW"
    except Exception as e:
        print("GLFW doesn't work, using Pygame")
        import pygame
        if pygame.init()[0] == 0:
            raise PyUnityException("No window provider found")
        config.windowProvider = "pygame"
        w = "Pygame"

SceneManager = SceneManager()

print(f"Loaded PyUnity version {__version__}")
print(f"Using window provider {w}")