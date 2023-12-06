## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

from . import Logger
import os

if "PYUNITY_DEBUG_MODE" not in os.environ:
    os.environ["PYUNITY_DEBUG_MODE"] = "1"
if "PYUNITY_AUDIO" not in os.environ:
    os.environ["PYUNITY_AUDIO"] = "1"
if "PYUNITY_CHECK_WINDOW" not in os.environ:
    os.environ["PYUNITY_CHECK_WINDOW"] = "0"
if "PYUNITY_INTERACTIVE" not in os.environ:
    os.environ["PYUNITY_INTERACTIVE"] = "1"
if "PYUNITY_CHANGE_MODULE" not in os.environ:
    os.environ["PYUNITY_CHANGE_MODULE"] = "1"

os.environ["MESA_GL_VERSION_OVERRIDE"] = "3.3"
os.environ["MESA_GLSL_VERSION_OVERRIDE"] = "330"

audio = True

size = (800, 500)
fps = 0
faceCulling = True
windowProvider = None
vsync = False
exitOnError = True

Logger.LogLine(Logger.DEBUG, "Loaded config")
