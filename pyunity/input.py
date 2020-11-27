"""
Module to manage getting input from window providers.

This will be imported as ``pyunity.Input``.

"""

import pygame.locals
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
    A = Code([None, pygame.locals.K_a, None])
    B = Code([None, pygame.locals.K_b, None])
    C = Code([None, pygame.locals.K_c, None])
    D = Code([None, pygame.locals.K_d, None])
    E = Code([None, pygame.locals.K_e, None])
    F = Code([None, pygame.locals.K_f, None])
    G = Code([None, pygame.locals.K_g, None])
    H = Code([None, pygame.locals.K_h, None])
    I = Code([None, pygame.locals.K_i, None])
    J = Code([None, pygame.locals.K_j, None])
    K = Code([None, pygame.locals.K_k, None])
    L = Code([None, pygame.locals.K_l, None])
    M = Code([None, pygame.locals.K_m, None])
    N = Code([None, pygame.locals.K_n, None])
    O = Code([None, pygame.locals.K_o, None])
    P = Code([None, pygame.locals.K_p, None])
    Q = Code([None, pygame.locals.K_q, None])
    R = Code([None, pygame.locals.K_r, None])
    S = Code([None, pygame.locals.K_s, None])
    T = Code([None, pygame.locals.K_t, None])
    U = Code([None, pygame.locals.K_u, None])
    V = Code([None, pygame.locals.K_v, None])
    W = Code([None, pygame.locals.K_w, None])
    X = Code([None, pygame.locals.K_x, None])
    Y = Code([None, pygame.locals.K_y, None])
    Z = Code([None, pygame.locals.K_z, None])
    Space = Code([None, pygame.locals.K_SPACE, None])
    Alpha0 = Code([None, pygame.locals.K_0, None])
    Alpha1 = Code([None, pygame.locals.K_1, None])
    Alpha2 = Code([None, pygame.locals.K_2, None])
    Alpha3 = Code([None, pygame.locals.K_3, None])
    Alpha4 = Code([None, pygame.locals.K_4, None])
    Alpha5 = Code([None, pygame.locals.K_5, None])
    Alpha6 = Code([None, pygame.locals.K_6, None])
    Alpha7 = Code([None, pygame.locals.K_7, None])
    Alpha8 = Code([None, pygame.locals.K_8, None])
    Alpha9 = Code([None, pygame.locals.K_9, None])
    F1 = Code([None, pygame.locals.K_F1, None])
    F2 = Code([None, pygame.locals.K_F2, None])
    F3 = Code([None, pygame.locals.K_F3, None])
    F4 = Code([None, pygame.locals.K_F4, None])
    F5 = Code([None, pygame.locals.K_F5, None])
    F6 = Code([None, pygame.locals.K_F6, None])
    F7 = Code([None, pygame.locals.K_F7, None])
    F8 = Code([None, pygame.locals.K_F8, None])
    F9 = Code([None, pygame.locals.K_F9, None])
    F10 = Code([None, pygame.locals.K_F10, None])
    F11 = Code([None, pygame.locals.K_F11, None])
    F12 = Code([None, pygame.locals.K_F12, None])
    Keypad0 = Code([None, pygame.locals.K_KP0, None])
    Keypad1 = Code([None, pygame.locals.K_KP1, None])
    Keypad2 = Code([None, pygame.locals.K_KP2, None])
    Keypad3 = Code([None, pygame.locals.K_KP3, None])
    Keypad4 = Code([None, pygame.locals.K_KP4, None])
    Keypad5 = Code([None, pygame.locals.K_KP5, None])
    Keypad6 = Code([None, pygame.locals.K_KP6, None])
    Keypad7 = Code([None, pygame.locals.K_KP7, None])
    Keypad8 = Code([None, pygame.locals.K_KP8, None])
    Keypad9 = Code([None, pygame.locals.K_KP9, None])
    Up = Code([None, pygame.locals.K_UP, None])
    Down = Code([None, pygame.locals.K_DOWN, None])
    Left = Code([None, pygame.locals.K_LEFT, None])
    Right = Code([None, pygame.locals.K_RIGHT, None])

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
