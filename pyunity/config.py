import os
from . import Logger
if "PYUNITY_DEBUG_MODE" not in os.environ:
    os.environ["PYUNITY_DEBUG_MODE"] = "1"
if "PYUNITY_INTERACTIVE" not in os.environ:
    os.environ["PYUNITY_INTERACTIVE"] = "1"
os.environ["MESA_GL_VERSION_OVERRIDE"] = "3.3"
os.environ["MESA_GLSL_VERSION_OVERRIDE"] = "330"

size = (800, 500)
fps = 60
faceCulling = True
audio: bool = True

Logger.LogLine(Logger.DEBUG, "Loaded config")

if os.environ["PYUNITY_INTERACTIVE"] == "1":
    from . import window
    windowProvider = window.GetWindowProvider()

    def SetWindowProvider(name):
        global windowProvider
        windowProvider = window.SetWindowProvider(name)
