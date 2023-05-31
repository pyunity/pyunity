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
    os.environ["PYOPENGL_PLATFORM"] = "egl"
    try:
        import OpenGL.EGL as egl
    except ImportError:
        cleanup()
        del os.environ["PYOPENGL_PLATFORM"]
        raise WindowProviderException("Could not import OpenGL.EGL")
    egl.eglGetDisplay(egl.EGL_DEFAULT_DISPLAY)
    err = egl.eglGetError()
    if err:
        raise WindowProviderException("EGL error: " + err)

def cleanup():
    import sys
    removed = []
    for module in sys.modules:
        if module.startswith("OpenGL"):
            removed.append(module)

    for module in removed:
        sys.modules.pop(module)
