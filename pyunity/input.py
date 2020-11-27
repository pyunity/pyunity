"""
Module to manage getting input from window providers.

This will be imported as ``pyunity.Input``.

"""

from pygame import locals as local
from . import config
from .scene import SceneManager
__all__ = ["GetKey", "GetKeyUp", "GetKeyDown"]

class Code:
    def __init__(self, vals):
        self.vals = {
            "GLFW": vals[0],
            "Pygame": vals[1],
            "FreeGLUT": vals[2],
        }

class KeyCode:
    A = Code([None, local.K_a, None])
    B = Code([None, local.K_b, None])
    C = Code([None, local.K_c, None])
    D = Code([None, local.K_d, None])
    E = Code([None, local.K_e, None])
    F = Code([None, local.K_f, None])
    G = Code([None, local.K_g, None])
    H = Code([None, local.K_h, None])
    I = Code([None, local.K_i, None])
    J = Code([None, local.K_j, None])
    K = Code([None, local.K_k, None])
    L = Code([None, local.K_l, None])
    M = Code([None, local.K_m, None])
    N = Code([None, local.K_n, None])
    O = Code([None, local.K_o, None])
    P = Code([None, local.K_p, None])
    Q = Code([None, local.K_q, None])
    R = Code([None, local.K_r, None])
    S = Code([None, local.K_s, None])
    T = Code([None, local.K_t, None])
    U = Code([None, local.K_u, None])
    V = Code([None, local.K_v, None])
    W = Code([None, local.K_w, None])
    X = Code([None, local.K_x, None])
    Y = Code([None, local.K_y, None])
    Z = Code([None, local.K_z, None])
    Space = Code([None, local.K_SPACE, None])
    Alpha0 = Code([None, local.K_0, None])
    Alpha1 = Code([None, local.K_1, None])
    Alpha2 = Code([None, local.K_2, None])
    Alpha3 = Code([None, local.K_3, None])
    Alpha4 = Code([None, local.K_4, None])
    Alpha5 = Code([None, local.K_5, None])
    Alpha6 = Code([None, local.K_6, None])
    Alpha7 = Code([None, local.K_7, None])
    Alpha8 = Code([None, local.K_8, None])
    Alpha9 = Code([None, local.K_9, None])
    F1 = Code([None, local.K_F1, None])
    F2 = Code([None, local.K_F2, None])
    F3 = Code([None, local.K_F3, None])
    F4 = Code([None, local.K_F4, None])
    F5 = Code([None, local.K_F5, None])
    F6 = Code([None, local.K_F6, None])
    F7 = Code([None, local.K_F7, None])
    F8 = Code([None, local.K_F8, None])
    F9 = Code([None, local.K_F9, None])
    F10 = Code([None, local.K_F10, None])
    F11 = Code([None, local.K_F11, None])
    F12 = Code([None, local.K_F12, None])
    Keypad0 = Code([None, local.K_KP0, None])
    Keypad1 = Code([None, local.K_KP1, None])
    Keypad2 = Code([None, local.K_KP2, None])
    Keypad3 = Code([None, local.K_KP3, None])
    Keypad4 = Code([None, local.K_KP4, None])
    Keypad5 = Code([None, local.K_KP5, None])
    Keypad6 = Code([None, local.K_KP6, None])
    Keypad7 = Code([None, local.K_KP7, None])
    Keypad8 = Code([None, local.K_KP8, None])
    Keypad9 = Code([None, local.K_KP9, None])

def GetKey(keycode):
    pressed = SceneManager.window.get_keys()
    check = keycode.vals[config.windowProvider]
    if check is None:
        return 0
    return pressed[check]

def GetKeyDown(keycode):
    down = SceneManager.window.get_keys_down()
    check = keycode.vals[config.windowProvider]
    if check is None:
        return 0
    return down[check]

def GetKeyUp(keycode):
    up = SceneManager.window.get_keys_up()
    check = keycode.vals[config.windowProvider]
    if check is None:
        return 0
    return up[check]
