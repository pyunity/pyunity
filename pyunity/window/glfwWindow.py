"""Class to create a window using GLFW."""

import glfw
from ..errors import *
from ..core import Clock

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
        glfw.set_key_callback(self.window, self.key_callback)

        self.keys = {
            "up": [0 for i in range(glfw.KEY_LAST)],
            "down": [0 for i in range(glfw.KEY_LAST)],
            "pressed": [0 for i in range(glfw.KEY_LAST)],
        }
        self.released = (False, None)

    def framebuffer_size_callback(self, window, width, height):
        self.resize(width, height)
        self.update_func()
        glfw.swap_buffers(self.window)

    def key_callback(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            self.keys["up"][key] = 0
            self.keys["down"][key] = 1
            self.keys["pressed"][key] = 1
        elif action == glfw.REPEAT:
            self.keys["up"][key] = 0
            self.keys["down"][key] = 0
            self.keys["pressed"][key] = 1
        else:
            self.keys["up"][key] = 1
            self.keys["down"][key] = 0
            self.keys["pressed"][key] = 0
            self.released = (True, key)

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
        clock.Start(60)
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.check_quit()
            if self.released[0]:
                self.keys["up"][self.released[1]] = 0
                self.released = (False, None)

            self.update_func()
            glfw.swap_buffers(self.window)
            clock.Maintain()

        self.quit()

    def get_keys(self):
        return self.keys["pressed"]

    def get_keys_down(self):
        return self.keys["down"]

    def get_keys_up(self):
        return self.keys["up"]
