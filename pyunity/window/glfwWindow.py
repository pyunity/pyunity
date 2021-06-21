"""Class to create a window using GLFW."""

import glfw
from ..errors import *
from ..core import Clock
from .. import config

class Window:
    """
    A window provider that uses GLFW.

    Raises
    ------
    PyUnityException
        If the window creation fails

    """

    def __init__(self, name, resize):
        self.resize = resize
        glfw.init()

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

    def check_quit(self):
        alt_pressed = glfw.get_key(self.window, glfw.KEY_LEFT_ALT) or glfw.get_key(
            self.window, glfw.KEY_RIGHT_ALT)
        if glfw.get_key(self.window, glfw.KEY_ESCAPE) or (alt_pressed and glfw.get_key(self.window, glfw.KEY_F4)):
            glfw.set_window_should_close(self.window, 1)

    def quit(self):
        glfw.destroy_window(self.window)

    def start(self, update_func):
        """
        Start the main loop of the window.

        Parameters
        ----------
        update_func : function
            The function that calls the OpenGL calls.

        """
        self.update_func = update_func
        clock = Clock()
        clock.Start(config.fps)
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.check_quit()

            self.update_func()
            glfw.swap_buffers(self.window)
            clock.Maintain()

        self.quit()
