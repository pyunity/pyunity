import os
from . import Logger
if "PYUNITY_DEBUG_MODE" not in os.environ:
    os.environ["PYUNITY_DEBUG_MODE"] = "1"
if "PYUNITY_INTERACTIVE" not in os.environ:
    os.environ["PYUNITY_INTERACTIVE"] = "1"
os.environ["MESA_GL_VERSION_OVERRIDE"] = "3.3"
os.environ["MESA_GLSL_VERSION_OVERRIDE"] = "330"

size = (800, 500)
fps = 0
faceCulling = True
audio = True
windowProvider = None

Logger.LogLine(Logger.DEBUG, "Loaded config")
