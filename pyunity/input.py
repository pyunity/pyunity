"""
Module to manage getting input from window providers.

This will be imported as ``pyunity.Input``.

"""

import pygame.constants
import glfw
from . import config
from .scenes import SceneManager
__all__ = ["GetKey", "GetKeyUp", "GetKeyDown"]

class Code:
    """
    Represents a key on a keyboard.
    Do not instantiate this class.

    """
    def __init__(self, vals):
        self.vals = {
            "GLFW": vals[0],
            "Pygame": vals[1],
            "FreeGLUT": vals[2],
        }

class KeyCode:
    """
    KeyCodes to reference each key on the keyboard.
    Do not instantiate this class.

    """

    A = Code([glfw.KEY_A, pygame.constants.K_a, None])
    B = Code([glfw.KEY_B, pygame.constants.K_b, None])
    C = Code([glfw.KEY_C, pygame.constants.K_c, None])
    D = Code([glfw.KEY_D, pygame.constants.K_d, None])
    E = Code([glfw.KEY_E, pygame.constants.K_e, None])
    F = Code([glfw.KEY_F, pygame.constants.K_f, None])
    G = Code([glfw.KEY_G, pygame.constants.K_g, None])
    H = Code([glfw.KEY_H, pygame.constants.K_h, None])
    I = Code([glfw.KEY_I, pygame.constants.K_i, None])
    J = Code([glfw.KEY_J, pygame.constants.K_j, None])
    K = Code([glfw.KEY_K, pygame.constants.K_k, None])
    L = Code([glfw.KEY_L, pygame.constants.K_l, None])
    M = Code([glfw.KEY_M, pygame.constants.K_m, None])
    N = Code([glfw.KEY_N, pygame.constants.K_n, None])
    O = Code([glfw.KEY_O, pygame.constants.K_o, None])
    P = Code([glfw.KEY_P, pygame.constants.K_p, None])
    Q = Code([glfw.KEY_Q, pygame.constants.K_q, None])
    R = Code([glfw.KEY_R, pygame.constants.K_r, None])
    S = Code([glfw.KEY_S, pygame.constants.K_s, None])
    T = Code([glfw.KEY_T, pygame.constants.K_t, None])
    U = Code([glfw.KEY_U, pygame.constants.K_u, None])
    V = Code([glfw.KEY_V, pygame.constants.K_v, None])
    W = Code([glfw.KEY_W, pygame.constants.K_w, None])
    X = Code([glfw.KEY_X, pygame.constants.K_x, None])
    Y = Code([glfw.KEY_Y, pygame.constants.K_y, None])
    Z = Code([glfw.KEY_Z, pygame.constants.K_z, None])
    Space = Code([glfw.KEY_SPACE, pygame.constants.K_SPACE, None])
    Alpha0 = Code([glfw.KEY_0, pygame.constants.K_0, None])
    Alpha1 = Code([glfw.KEY_1, pygame.constants.K_1, None])
    Alpha2 = Code([glfw.KEY_2, pygame.constants.K_2, None])
    Alpha3 = Code([glfw.KEY_3, pygame.constants.K_3, None])
    Alpha4 = Code([glfw.KEY_4, pygame.constants.K_4, None])
    Alpha5 = Code([glfw.KEY_5, pygame.constants.K_5, None])
    Alpha6 = Code([glfw.KEY_6, pygame.constants.K_6, None])
    Alpha7 = Code([glfw.KEY_7, pygame.constants.K_7, None])
    Alpha8 = Code([glfw.KEY_8, pygame.constants.K_8, None])
    Alpha9 = Code([glfw.KEY_9, pygame.constants.K_9, None])
    F1 = Code([glfw.KEY_F1, pygame.constants.K_F1, None])
    F2 = Code([glfw.KEY_F2, pygame.constants.K_F2, None])
    F3 = Code([glfw.KEY_F3, pygame.constants.K_F3, None])
    F4 = Code([glfw.KEY_F4, pygame.constants.K_F4, None])
    F5 = Code([glfw.KEY_F5, pygame.constants.K_F5, None])
    F6 = Code([glfw.KEY_F6, pygame.constants.K_F6, None])
    F7 = Code([glfw.KEY_F7, pygame.constants.K_F7, None])
    F8 = Code([glfw.KEY_F8, pygame.constants.K_F8, None])
    F9 = Code([glfw.KEY_F9, pygame.constants.K_F9, None])
    F10 = Code([glfw.KEY_F10, pygame.constants.K_F10, None])
    F11 = Code([glfw.KEY_F11, pygame.constants.K_F11, None])
    F12 = Code([glfw.KEY_F12, pygame.constants.K_F12, None])
    Keypad0 = Code([glfw.KEY_KP_0, pygame.constants.K_KP0, None])
    Keypad1 = Code([glfw.KEY_KP_1, pygame.constants.K_KP1, None])
    Keypad2 = Code([glfw.KEY_KP_2, pygame.constants.K_KP2, None])
    Keypad3 = Code([glfw.KEY_KP_3, pygame.constants.K_KP3, None])
    Keypad4 = Code([glfw.KEY_KP_4, pygame.constants.K_KP4, None])
    Keypad5 = Code([glfw.KEY_KP_5, pygame.constants.K_KP5, None])
    Keypad6 = Code([glfw.KEY_KP_6, pygame.constants.K_KP6, None])
    Keypad7 = Code([glfw.KEY_KP_7, pygame.constants.K_KP7, None])
    Keypad8 = Code([glfw.KEY_KP_8, pygame.constants.K_KP8, None])
    Keypad9 = Code([glfw.KEY_KP_9, pygame.constants.K_KP9, None])
    Up = Code([glfw.KEY_UP, pygame.constants.K_UP, None])
    Down = Code([glfw.KEY_DOWN, pygame.constants.K_DOWN, None])
    Left = Code([glfw.KEY_LEFT, pygame.constants.K_LEFT, None])
    Right = Code([glfw.KEY_RIGHT, pygame.constants.K_RIGHT, None])

def GetKey(keycode):
    """
    Check if key has been pressed.

    Parameters
    ----------
    keycode : KeyCode
        Key to query

    Returns
    -------
    int
        1 if pressed and 0 if not pressed.

    """
    pressed = SceneManager.window.get_keys()
    check = keycode.vals[config.windowProvider]
    if check is None:
        return 0
    return pressed[check]

def GetKeyDown(keycode):
    """
    Check if key was pressed down this frame.

    Parameters
    ----------
    keycode : KeyCode
        Key to query

    Returns
    -------
    int
        1 if pressed and 0 if not pressed.

    """
    down = SceneManager.window.get_keys_down()
    check = keycode.vals[config.windowProvider]
    if check is None:
        return 0
    return down[check]

def GetKeyUp(keycode):
    """
    Check if key was released this frame.

    Parameters
    ----------
    keycode : KeyCode
        Key to query

    Returns
    -------
    int
        1 if released and 0 if not released.

    """
    up = SceneManager.window.get_keys_up()
    check = keycode.vals[config.windowProvider]
    if check is None:
        return 0
    return up[check]
