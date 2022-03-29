# Default imports, do not modify
from pyunity.errors import *
from pyunity.window.providers import checkModule
# Modify the below variable and function

name = "GLUT"

def check():
    """Checks to see if GLUT works"""
    checkModule("OpenGL.GLUT")
    import OpenGL.GLUT
    OpenGL.GLUT.glutInit()
