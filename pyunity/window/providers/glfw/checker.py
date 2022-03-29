# Default imports, do not modify
from pyunity.errors import *
from pyunity.window.providers import checkModule
# Modify the below variable and function

name = "GLFW"

def check():
    """Checks to see if GLFW works"""
    glfw = checkModule("glfw")
    if not glfw.init():
        raise PyUnityException
    window = glfw.create_window(5, 5, "test", None, None)
    glfw.destroy_window(window)
