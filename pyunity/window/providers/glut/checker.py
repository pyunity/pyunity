# Default imports, do not modify
# Keep all other imports inside check function
from pyunity.errors import *
from pyunity.window.providers import checkModule

# Modify the below variables and function

name = "GLUT"
prio = 0

def check():
    """Checks to see if GLUT works"""
    checkModule("OpenGL.GLUT")
    import OpenGL.GLUT
    OpenGL.GLUT.glutInit()
