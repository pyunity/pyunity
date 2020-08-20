import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
if "PYUNITY_DEBUG_MODE" not in os.environ: os.environ["PYUNITY_DEBUG_MODE"] = "1"

from .window import *

windowProvider = None
size = (800, 500)
fps = 60
faceCulling = True

windowProviders = {"glut": glutWindow, "glfw": glfwWindow, "pygame": pygameWindow}

if os.environ["PYUNITY_DEBUG_MODE"] == "1":
    print("Loaded config")