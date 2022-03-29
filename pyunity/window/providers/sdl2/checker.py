# Default imports, do not modify
from pyunity.errors import *
from pyunity.window.providers import checkModule
# Modify the below variable and function

name = "PySDL2"

def check():
    """Checks to see if PySDL2 works"""
    sdl2 = checkModule("sdl2")
    if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
        raise PyUnityException
