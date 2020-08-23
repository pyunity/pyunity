import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
if "PYUNITY_DEBUG_MODE" not in os.environ: os.environ["PYUNITY_DEBUG_MODE"] = "1"
if "PYUNITY_NO_INTERACTIVE" not in os.environ: os.environ["PYUNITY_NO_INTERACTIVE"] = "0"

size = (800, 500)
fps = 60
faceCulling = True

if os.environ["PYUNITY_DEBUG_MODE"] == "1":
    print("Loaded config")

if os.environ["PYUNITY_NO_INTERACTIVE"] == "0":

    from . import window

    try:
        if os.environ["PYUNITY_DEBUG_MODE"] == "1":
            print("Trying FreeGLUT as a window provider")
        import OpenGL.GLUT
        OpenGL.GLUT.glutInit()
        del OpenGL
        windowProvider = "glut"
        w = "FreeGLUT"
    except Exception as e:
        if os.environ["PYUNITY_DEBUG_MODE"] == "1":
            print("FreeGLUT doesn't work, using GLFW")
        try:
            import glfw
            if not glfw.init():
                raise Exception
            glfw.create_window(50, 50, "Test", None, None)
            glfw.terminate()
            del glfw
            windowProvider = "glfw"
            w = "GLFW"
        except Exception as e:
            if os.environ["PYUNITY_DEBUG_MODE"] == "1":
                print("GLFW doesn't work, using Pygame")
            import pygame
            if pygame.init()[0] == 0:
                raise PyUnityException("No window provider found")
            del pygame
            windowProvider = "pygame"
            w = "Pygame"

    windowProvider = window.LoadWindowProvider(windowProvider)

    del window

    if os.environ["PYUNITY_DEBUG_MODE"] == "1":
        print(f"Using window provider {w}")

else:
    print("PYUNITY_NO_INTERACTIVE is set to 1, no window provider loaded")

del os