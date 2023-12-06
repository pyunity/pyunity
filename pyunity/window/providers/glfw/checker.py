# Default imports, do not modify
# Keep all other imports inside check function
from pyunity.errors import *
from pyunity.window.providers import checkModule

# Modify the below variables and function

name = "GLFW"
prio = 2

def check():
    """Checks to see if GLFW works"""
    glfw = checkModule("glfw")
    if not glfw.init():
        raise WindowProviderException("GLFW init failed")
    window = glfw.create_window(5, 5, "test", None, None)
    glfw.destroy_window(window)
