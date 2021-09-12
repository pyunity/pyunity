"""Class to create a window using GLFW."""

import glfw
import sys

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
        if sys.platform == "darwin":
            glfw.window_hint(glfw.GLFW_CONTEXT_VERSION_MAJOR, 3)
            glfw.window_hint(glfw.GLFW_CONTEXT_VERSION_MINOR, 3)
            glfw.window_hint(glfw.GLFW_OPENGL_FORWARD_COMPAT, glfw.GL_TRUE)
            glfw.window_hint(glfw.GLFW_OPENGL_PROFILE,
                             glfw.GLFW_OPENGL_CORE_PROFILE)

        self.window = glfw.create_window(800, 500, name, None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("Cannot open GLFW window")

        glfw.make_context_current(self.window)

        self.resize = resize
        glfw.set_framebuffer_size_callback(
            self.window, self.framebuffer_size_callback)
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_mouse_button_callback(self.window, self.mouse_callback)

    def framebuffer_size_callback(self, window, width, height):
        self.resize(width, height)
        self.update_func()
        glfw.swap_buffers(window)

    def key_callback(self, window, key, scancode, action, mods):
        print("Key")

    def mouse_callback(self, window, button, action, mods):
        print("Mouse")

    # def check_quit(self):
    #     alt_pressed = glfw.get_key(self.window, glfw.KEY_LEFT_ALT) or glfw.get_key(
    #         self.window, glfw.KEY_RIGHT_ALT)
    #     if alt_pressed and glfw.get_key(self.window, glfw.KEY_F4):
    #         glfw.set_window_should_close(self.window, 1)

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
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.update_func()
            glfw.swap_buffers(self.window)

        self.quit()

window = Window("Test", lambda: None)
window.start(lambda: None)