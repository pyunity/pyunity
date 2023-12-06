# Default imports, do not modify
# Keep all other imports inside check function
from pyunity.errors import *
from pyunity.window.providers import checkModule

# Modify the below variables and function

name = "GLContext"
prio = 0

def check():
    glcontext = checkModule("glcontext")
    backend = glcontext.default_backend()
    backend(glversion=330, mode="standalone")
