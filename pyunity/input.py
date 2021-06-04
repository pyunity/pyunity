"""
Module to manage getting input from window providers.

This will be imported as ``pyunity.Input``.

"""

import pygame.locals
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
    
    A = Code([glfw.KEY_A, pygame.locals.K_a, None])
    B = Code([glfw.KEY_B, pygame.locals.K_b, None])
    C = Code([glfw.KEY_C, pygame.locals.K_c, None])
    D = Code([glfw.KEY_D, pygame.locals.K_d, None])
    E = Code([glfw.KEY_E, pygame.locals.K_e, None])
    F = Code([glfw.KEY_F, pygame.locals.K_f, None])
    G = Code([glfw.KEY_G, pygame.locals.K_g, None])
    H = Code([glfw.KEY_H, pygame.locals.K_h, None])
    I = Code([glfw.KEY_I, pygame.locals.K_i, None])
    J = Code([glfw.KEY_J, pygame.locals.K_j, None])
    K = Code([glfw.KEY_K, pygame.locals.K_k, None])
    L = Code([glfw.KEY_L, pygame.locals.K_l, None])
    M = Code([glfw.KEY_M, pygame.locals.K_m, None])
    N = Code([glfw.KEY_N, pygame.locals.K_n, None])
    O = Code([glfw.KEY_O, pygame.locals.K_o, None])
    P = Code([glfw.KEY_P, pygame.locals.K_p, None])
    Q = Code([glfw.KEY_Q, pygame.locals.K_q, None])
    R = Code([glfw.KEY_R, pygame.locals.K_r, None])
    S = Code([glfw.KEY_S, pygame.locals.K_s, None])
    T = Code([glfw.KEY_T, pygame.locals.K_t, None])
    U = Code([glfw.KEY_U, pygame.locals.K_u, None])
    V = Code([glfw.KEY_V, pygame.locals.K_v, None])
    W = Code([glfw.KEY_W, pygame.locals.K_w, None])
    X = Code([glfw.KEY_X, pygame.locals.K_x, None])
    Y = Code([glfw.KEY_Y, pygame.locals.K_y, None])
    Z = Code([glfw.KEY_Z, pygame.locals.K_z, None])
    Space = Code([glfw.KEY_SPACE, pygame.locals.K_SPACE, None])
    Alpha0 = Code([glfw.KEY_0, pygame.locals.K_0, None])
    Alpha1 = Code([glfw.KEY_1, pygame.locals.K_1, None])
    Alpha2 = Code([glfw.KEY_2, pygame.locals.K_2, None])
    Alpha3 = Code([glfw.KEY_3, pygame.locals.K_3, None])
    Alpha4 = Code([glfw.KEY_4, pygame.locals.K_4, None])
    Alpha5 = Code([glfw.KEY_5, pygame.locals.K_5, None])
    Alpha6 = Code([glfw.KEY_6, pygame.locals.K_6, None])
    Alpha7 = Code([glfw.KEY_7, pygame.locals.K_7, None])
    Alpha8 = Code([glfw.KEY_8, pygame.locals.K_8, None])
    Alpha9 = Code([glfw.KEY_9, pygame.locals.K_9, None])
    F1 = Code([glfw.KEY_F1, pygame.locals.K_F1, None])
    F2 = Code([glfw.KEY_F2, pygame.locals.K_F2, None])
    F3 = Code([glfw.KEY_F3, pygame.locals.K_F3, None])
    F4 = Code([glfw.KEY_F4, pygame.locals.K_F4, None])
    F5 = Code([glfw.KEY_F5, pygame.locals.K_F5, None])
    F6 = Code([glfw.KEY_F6, pygame.locals.K_F6, None])
    F7 = Code([glfw.KEY_F7, pygame.locals.K_F7, None])
    F8 = Code([glfw.KEY_F8, pygame.locals.K_F8, None])
    F9 = Code([glfw.KEY_F9, pygame.locals.K_F9, None])
    F10 = Code([glfw.KEY_F10, pygame.locals.K_F10, None])
    F11 = Code([glfw.KEY_F11, pygame.locals.K_F11, None])
    F12 = Code([glfw.KEY_F12, pygame.locals.K_F12, None])
    Keypad0 = Code([glfw.KEY_KP_0, pygame.locals.K_KP0, None])
    Keypad1 = Code([glfw.KEY_KP_1, pygame.locals.K_KP1, None])
    Keypad2 = Code([glfw.KEY_KP_2, pygame.locals.K_KP2, None])
    Keypad3 = Code([glfw.KEY_KP_3, pygame.locals.K_KP3, None])
    Keypad4 = Code([glfw.KEY_KP_4, pygame.locals.K_KP4, None])
    Keypad5 = Code([glfw.KEY_KP_5, pygame.locals.K_KP5, None])
    Keypad6 = Code([glfw.KEY_KP_6, pygame.locals.K_KP6, None])
    Keypad7 = Code([glfw.KEY_KP_7, pygame.locals.K_KP7, None])
    Keypad8 = Code([glfw.KEY_KP_8, pygame.locals.K_KP8, None])
    Keypad9 = Code([glfw.KEY_KP_9, pygame.locals.K_KP9, None])
    Up = Code([glfw.KEY_UP, pygame.locals.K_UP, None])
    Down = Code([glfw.KEY_DOWN, pygame.locals.K_DOWN, None])
    Left = Code([glfw.KEY_LEFT, pygame.locals.K_LEFT, None])
    Right = Code([glfw.KEY_RIGHT, pygame.locals.K_RIGHT, None])

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
