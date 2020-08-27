import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
if "PYUNITY_DEBUG_MODE" not in os.environ: os.environ["PYUNITY_DEBUG_MODE"] = "1"

size = (800, 500)
fps = 60
faceCulling = True

if os.environ["PYUNITY_DEBUG_MODE"] == "1":
    print("Loaded config")

from . import window

windowProvider = window.LoadWindowProvider()

del window, os