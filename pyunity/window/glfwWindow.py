"""Class to create a window using GLFW."""

import glfw
from ..errors import *
import OpenGL.GL as gl

class Window:
    """
    A window provider that uses GLFW.

    Raises
    ------
    PyUnityException
        If the window creation fails

    """

    def __init__(self, config, name, resize):
        self.config = config
        glfw.init()

        # glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
        self.window = glfw.create_window(*config.size, name, None, None)
        if not self.window:
            glfw.terminate()
            raise PyUnityException("Cannot open GLFW window")

        glfw.make_context_current(self.window)

        self.resize = resize
        glfw.set_framebuffer_size_callback(
            self.window, self.framebuffer_size_callback)

    def framebuffer_size_callback(self, window, width, height):
        self.resize(width, height)
        self.update_func()
        glfw.swap_buffers(self.window)

    def start(self, update_func):
        """
        Start the main loop of the window.

        Parameters
        ----------
        update_func : function
            The function that calls the OpenGL calls.

        """
        self.update_func = update_func
        last = glfw.get_time()
        while not glfw.window_should_close(self.window):
            self.update_func()
            glfw.swap_buffers(self.window)
            glfw.poll_events()

            while (glfw.get_time() < last + 1 / self.config.fps):
                pass

            last += 1 / self.config.fps
        glfw.terminate()
