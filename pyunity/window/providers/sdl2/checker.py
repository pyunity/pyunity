# Default imports, do not modify
# Keep all other imports inside check function
from pyunity.errors import *
from pyunity.window.providers import checkModule

# Modify the below variables and function

name = "PySDL2"
prio = 1

def check():
    """Checks to see if PySDL2 works"""
    sdl2 = checkModule("sdl2")
    if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
        raise PyUnityException("SDL2 init failed")
