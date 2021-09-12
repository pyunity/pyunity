"""Class to create a window using GLFW."""

import glfw
import sys
from ..errors import *
from ..values import Clock
from ..input import KeyCode, KeyState, MouseCode
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
        if sys.platform == "darwin":
            glfw.window_hint(glfw.GLFW_CONTEXT_VERSION_MAJOR, 3)
            glfw.window_hint(glfw.GLFW_CONTEXT_VERSION_MINOR, 3)
            glfw.window_hint(glfw.GLFW_OPENGL_FORWARD_COMPAT, glfw.GL_TRUE)
            glfw.window_hint(glfw.GLFW_OPENGL_PROFILE,
                             glfw.GLFW_OPENGL_CORE_PROFILE)

        self.window = glfw.create_window(*config.size, name, None, None)
        if not self.window:
            glfw.terminate()
            raise PyUnityException("Cannot open GLFW window")

        glfw.make_context_current(self.window)

        self.resize = resize
        glfw.set_framebuffer_size_callback(
            self.window, self.framebuffer_size_callback)
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_mouse_button_callback(self.window, self.mouse_callback)

        self.keys = [KeyState.NONE for _ in range(glfw.KEY_MENU)]
        self.mouse = [KeyState.NONE, KeyState.NONE, KeyState.NONE]

    def framebuffer_size_callback(self, window, width, height):
        self.resize(width, height)
        self.update_func()
        glfw.swap_buffers(window)

    def key_callback(self, window, key, scancode, action, mods):
        if action == glfw.RELEASE:
            self.keys[key] = KeyState.UP
        elif action == glfw.REPEAT:
            self.keys[key] = KeyState.PRESS
        else:
            self.keys[key] = KeyState.DOWN

    def mouse_callback(self, window, button, action, mods):
        if action == glfw.PRESS:
            if self.mouse[button] == KeyState.NONE:
                self.mouse[button] = KeyState.DOWN
            else:
                self.mouse[button] = KeyState.PRESS
        elif action == glfw.RELEASE:
            self.mouse[button] = KeyState.UP

    def get_mouse(self, mousecode, keystate):
        mouse = mouseMap[mousecode]
        if keystate == KeyState.PRESS:
            if self.mouse[mouse] in [KeyState.PRESS, KeyState.DOWN]:
                return True
        if self.mouse[mouse] == keystate:
            return True
        return False

    def check_keys(self):
        for i in range(len(self.keys)):
            if self.keys[i] == KeyState.UP:
                self.keys[i] = KeyState.NONE
            elif self.keys[i] == KeyState.DOWN:
                self.keys[i] = KeyState.PRESS

    def check_mouse(self):
        for i in range(len(self.mouse)):
            if self.mouse[i] == KeyState.UP:
                self.mouse[i] = KeyState.NONE
            elif self.mouse[i] == KeyState.DOWN:
                self.mouse[i] = KeyState.PRESS

    def get_key(self, keycode, keystate):
        key = keyMap[keycode]
        if keystate == KeyState.PRESS:
            if self.keys[key] in [KeyState.PRESS, KeyState.DOWN]:
                return True
        if self.keys[key] == keystate:
            return True
        return False

    def get_mouse_pos(self):
        return glfw.get_cursor_pos(self.window)

    def check_quit(self):
        alt_pressed = glfw.get_key(self.window, glfw.KEY_LEFT_ALT) or glfw.get_key(
            self.window, glfw.KEY_RIGHT_ALT)
        if alt_pressed and glfw.get_key(self.window, glfw.KEY_F4):
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
            self.check_quit()
            self.check_keys()
            self.check_mouse()

            glfw.poll_events()
            self.update_func()
            glfw.swap_buffers(self.window)
            clock.Maintain()

        self.quit()

keyMap = {
    KeyCode.A: glfw.KEY_A,
    KeyCode.B: glfw.KEY_B,
    KeyCode.C: glfw.KEY_C,
    KeyCode.D: glfw.KEY_D,
    KeyCode.E: glfw.KEY_E,
    KeyCode.F: glfw.KEY_F,
    KeyCode.G: glfw.KEY_G,
    KeyCode.H: glfw.KEY_H,
    KeyCode.I: glfw.KEY_I,
    KeyCode.J: glfw.KEY_J,
    KeyCode.K: glfw.KEY_K,
    KeyCode.L: glfw.KEY_L,
    KeyCode.M: glfw.KEY_M,
    KeyCode.N: glfw.KEY_N,
    KeyCode.O: glfw.KEY_O,
    KeyCode.P: glfw.KEY_P,
    KeyCode.Q: glfw.KEY_Q,
    KeyCode.R: glfw.KEY_R,
    KeyCode.S: glfw.KEY_S,
    KeyCode.T: glfw.KEY_T,
    KeyCode.U: glfw.KEY_U,
    KeyCode.V: glfw.KEY_V,
    KeyCode.W: glfw.KEY_W,
    KeyCode.X: glfw.KEY_X,
    KeyCode.Y: glfw.KEY_Y,
    KeyCode.Z: glfw.KEY_Z,
    KeyCode.Space: glfw.KEY_SPACE,
    KeyCode.Alpha0: glfw.KEY_0,
    KeyCode.Alpha1: glfw.KEY_1,
    KeyCode.Alpha2: glfw.KEY_2,
    KeyCode.Alpha3: glfw.KEY_3,
    KeyCode.Alpha4: glfw.KEY_4,
    KeyCode.Alpha5: glfw.KEY_5,
    KeyCode.Alpha6: glfw.KEY_6,
    KeyCode.Alpha7: glfw.KEY_7,
    KeyCode.Alpha8: glfw.KEY_8,
    KeyCode.Alpha9: glfw.KEY_9,
    KeyCode.F1: glfw.KEY_F1,
    KeyCode.F2: glfw.KEY_F2,
    KeyCode.F3: glfw.KEY_F3,
    KeyCode.F4: glfw.KEY_F4,
    KeyCode.F5: glfw.KEY_F5,
    KeyCode.F6: glfw.KEY_F6,
    KeyCode.F7: glfw.KEY_F7,
    KeyCode.F8: glfw.KEY_F8,
    KeyCode.F9: glfw.KEY_F9,
    KeyCode.F10: glfw.KEY_F10,
    KeyCode.F11: glfw.KEY_F11,
    KeyCode.F12: glfw.KEY_F12,
    KeyCode.Keypad0: glfw.KEY_KP_0,
    KeyCode.Keypad1: glfw.KEY_KP_1,
    KeyCode.Keypad2: glfw.KEY_KP_2,
    KeyCode.Keypad3: glfw.KEY_KP_3,
    KeyCode.Keypad4: glfw.KEY_KP_4,
    KeyCode.Keypad5: glfw.KEY_KP_5,
    KeyCode.Keypad6: glfw.KEY_KP_6,
    KeyCode.Keypad7: glfw.KEY_KP_7,
    KeyCode.Keypad8: glfw.KEY_KP_8,
    KeyCode.Keypad9: glfw.KEY_KP_9,
    KeyCode.Up: glfw.KEY_UP,
    KeyCode.Down: glfw.KEY_DOWN,
    KeyCode.Left: glfw.KEY_LEFT,
    KeyCode.Right: glfw.KEY_RIGHT
}

mouseMap = {
    MouseCode.Left: glfw.MOUSE_BUTTON_LEFT,
    MouseCode.Middle: glfw.MOUSE_BUTTON_MIDDLE,
    MouseCode.Right: glfw.MOUSE_BUTTON_RIGHT,
}
