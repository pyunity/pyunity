# Default imports, do not modify
# Keep all other imports inside check function
from pyunity.errors import *
from pyunity.window.providers import checkModule
# Modify the below variables and function

name = "EGL"
prio = 0

def check():
    """Checks to see if EGL works"""
    import os
    from .egl import setupPlatform
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib")
    if os.path.isdir(directory):
        context = os.add_dll_directory(directory)
    else:
        context = None
    try:
        setupPlatform()
        egl = checkModule("OpenGL.EGL")
    except ImportError:
        cleanup()
        raise WindowProviderException("Could not import OpenGL.EGL")
    finally:
        if context is not None:
            context.close()
    egl.eglGetDisplay(egl.EGL_DEFAULT_DISPLAY)
    err = egl.eglGetError()
    if err != egl.EGL_SUCCESS:
        raise WindowProviderException("EGL error: " + str(err))

def cleanup():
    import sys
    removed = []
    for module in sys.modules:
        if module.startswith("OpenGL"):
            removed.append(module)

    for module in removed:
        sys.modules.pop(module)
