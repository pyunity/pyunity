"""Class to create a window using PySDL2."""

from ..values import Clock
from ..input import KeyCode, KeyState, MouseCode
from .. import config
import sdl2
import sdl2.ext
import sdl2.video

class Window:
    """
    A window provider that uses PySDL2.

    """

    def __init__(self, name, resize):
        self.resize = resize

        self.screen = sdl2.SDL_CreateWindow(
            name.encode(), sdl2.SDL_WINDOWPOS_UNDEFINED,
            sdl2.SDL_WINDOWPOS_UNDEFINED, *config.size,
            sdl2.SDL_WINDOW_OPENGL
        )

        sdl2.video.SDL_GL_SetAttribute(sdl2.video.SDL_GL_MULTISAMPLEBUFFERS, 1)
        sdl2.video.SDL_GL_SetAttribute(sdl2.video.SDL_GL_MULTISAMPLESAMPLES, 8)
        sdl2.video.SDL_GL_SetAttribute(
            sdl2.video.SDL_GL_CONTEXT_MAJOR_VERSION, 3)
        sdl2.video.SDL_GL_SetAttribute(
            sdl2.video.SDL_GL_CONTEXT_MINOR_VERSION, 3)
        sdl2.video.SDL_GL_SetAttribute(
            sdl2.video.SDL_GL_CONTEXT_PROFILE_MASK, sdl2.video.SDL_GL_CONTEXT_PROFILE_CORE)

        self.context = sdl2.SDL_GL_CreateContext(self.screen)

        renderer = sdl2.SDL_CreateRenderer(self.screen, -1, 0)
        sdl2.SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255)
        sdl2.SDL_RenderClear(renderer)
        sdl2.SDL_RenderPresent(renderer)

        self.keys = [KeyState.NONE for _ in range(
            sdl2.SDL_SCANCODE_AUDIOFASTFORWARD)]
        self.mouse = [None, KeyState.NONE, KeyState.NONE, KeyState.NONE]

    def quit(self):
        sdl2.SDL_DestroyWindow(self.screen)

    def start(self, update_func):
        self.update_func = update_func

        done = False
        clock = Clock()
        clock.Start(config.fps)
        while not done:
            events = sdl2.ext.get_events()
            for event in events:
                if event.type == sdl2.SDL_QUIT:
                    done = True

            self.process_keys(events)
            self.process_mouse(events)
            self.update_func()
            sdl2.SDL_GL_SwapWindow(self.screen)

            clock.Maintain()

        self.quit()

    def process_keys(self, events):
        for i in range(len(self.keys)):
            if self.keys[i] == KeyState.UP:
                self.keys[i] = KeyState.NONE
            elif self.keys[i] == KeyState.DOWN:
                self.keys[i] = KeyState.PRESS
        for event in events:
            if event.type == sdl2.SDL_KEYDOWN:
                if self.keys[event.key.keysym.scancode] == KeyState.NONE:
                    self.keys[event.key.keysym.scancode] = KeyState.DOWN
                else:
                    self.keys[event.key.keysym.scancode] = KeyState.PRESS
            elif event.type == sdl2.SDL_KEYUP:
                self.keys[event.key.keysym.scancode] = KeyState.UP

    def process_mouse(self, events):
        for i in range(len(self.mouse)):
            if self.mouse[i] == KeyState.UP:
                self.mouse[i] = KeyState.NONE
            elif self.mouse[i] == KeyState.DOWN:
                self.mouse[i] = KeyState.PRESS
        for event in events:
            if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                if self.mouse[event.button.button] == KeyState.NONE:
                    self.mouse[event.button.button] = KeyState.DOWN
                else:
                    self.mouse[event.button.button] = KeyState.PRESS
            elif event.type == sdl2.SDL_MOUSEBUTTONUP:
                self.mouse[event.button.button] = KeyState.UP

    def get_key(self, keycode, keystate):
        key = keyMap[keycode]
        if keystate == KeyState.PRESS:
            if self.keys[key] in [KeyState.PRESS, KeyState.DOWN]:
                return True
        if self.keys[key] == keystate:
            return True
        return False

    def get_mouse(self, mousecode, keystate):
        mouse = mouseMap[mousecode]
        if keystate == KeyState.PRESS:
            if self.mouse[mouse] in [KeyState.PRESS, KeyState.DOWN]:
                return True
        if self.mouse[mouse] == keystate:
            return True
        return False

keyMap = {
    KeyCode.A: sdl2.SDL_SCANCODE_A,
    KeyCode.B: sdl2.SDL_SCANCODE_B,
    KeyCode.C: sdl2.SDL_SCANCODE_C,
    KeyCode.D: sdl2.SDL_SCANCODE_D,
    KeyCode.E: sdl2.SDL_SCANCODE_E,
    KeyCode.F: sdl2.SDL_SCANCODE_F,
    KeyCode.G: sdl2.SDL_SCANCODE_G,
    KeyCode.H: sdl2.SDL_SCANCODE_H,
    KeyCode.I: sdl2.SDL_SCANCODE_I,
    KeyCode.J: sdl2.SDL_SCANCODE_J,
    KeyCode.K: sdl2.SDL_SCANCODE_K,
    KeyCode.L: sdl2.SDL_SCANCODE_L,
    KeyCode.M: sdl2.SDL_SCANCODE_M,
    KeyCode.N: sdl2.SDL_SCANCODE_N,
    KeyCode.O: sdl2.SDL_SCANCODE_O,
    KeyCode.P: sdl2.SDL_SCANCODE_P,
    KeyCode.Q: sdl2.SDL_SCANCODE_Q,
    KeyCode.R: sdl2.SDL_SCANCODE_R,
    KeyCode.S: sdl2.SDL_SCANCODE_S,
    KeyCode.T: sdl2.SDL_SCANCODE_T,
    KeyCode.U: sdl2.SDL_SCANCODE_U,
    KeyCode.V: sdl2.SDL_SCANCODE_V,
    KeyCode.W: sdl2.SDL_SCANCODE_W,
    KeyCode.X: sdl2.SDL_SCANCODE_X,
    KeyCode.Y: sdl2.SDL_SCANCODE_Y,
    KeyCode.Z: sdl2.SDL_SCANCODE_Z,
    KeyCode.Space: sdl2.SDL_SCANCODE_SPACE,
    KeyCode.Alpha0: sdl2.SDL_SCANCODE_0,
    KeyCode.Alpha1: sdl2.SDL_SCANCODE_1,
    KeyCode.Alpha2: sdl2.SDL_SCANCODE_2,
    KeyCode.Alpha3: sdl2.SDL_SCANCODE_3,
    KeyCode.Alpha4: sdl2.SDL_SCANCODE_4,
    KeyCode.Alpha5: sdl2.SDL_SCANCODE_5,
    KeyCode.Alpha6: sdl2.SDL_SCANCODE_6,
    KeyCode.Alpha7: sdl2.SDL_SCANCODE_7,
    KeyCode.Alpha8: sdl2.SDL_SCANCODE_8,
    KeyCode.Alpha9: sdl2.SDL_SCANCODE_9,
    KeyCode.F1: sdl2.SDL_SCANCODE_F1,
    KeyCode.F2: sdl2.SDL_SCANCODE_F2,
    KeyCode.F3: sdl2.SDL_SCANCODE_F3,
    KeyCode.F4: sdl2.SDL_SCANCODE_F4,
    KeyCode.F5: sdl2.SDL_SCANCODE_F5,
    KeyCode.F6: sdl2.SDL_SCANCODE_F6,
    KeyCode.F7: sdl2.SDL_SCANCODE_F7,
    KeyCode.F8: sdl2.SDL_SCANCODE_F8,
    KeyCode.F9: sdl2.SDL_SCANCODE_F9,
    KeyCode.F10: sdl2.SDL_SCANCODE_F10,
    KeyCode.F11: sdl2.SDL_SCANCODE_F11,
    KeyCode.F12: sdl2.SDL_SCANCODE_F12,
    KeyCode.Keypad0: sdl2.SDL_SCANCODE_KP_0,
    KeyCode.Keypad1: sdl2.SDL_SCANCODE_KP_1,
    KeyCode.Keypad2: sdl2.SDL_SCANCODE_KP_2,
    KeyCode.Keypad3: sdl2.SDL_SCANCODE_KP_3,
    KeyCode.Keypad4: sdl2.SDL_SCANCODE_KP_4,
    KeyCode.Keypad5: sdl2.SDL_SCANCODE_KP_5,
    KeyCode.Keypad6: sdl2.SDL_SCANCODE_KP_6,
    KeyCode.Keypad7: sdl2.SDL_SCANCODE_KP_7,
    KeyCode.Keypad8: sdl2.SDL_SCANCODE_KP_8,
    KeyCode.Keypad9: sdl2.SDL_SCANCODE_KP_9,
    KeyCode.Up: sdl2.SDL_SCANCODE_UP,
    KeyCode.Down: sdl2.SDL_SCANCODE_DOWN,
    KeyCode.Left: sdl2.SDL_SCANCODE_LEFT,
    KeyCode.Right: sdl2.SDL_SCANCODE_RIGHT
}

mouseMap = {
    MouseCode.Left: sdl2.SDL_BUTTON_LEFT,
    MouseCode.Middle: sdl2.SDL_BUTTON_MIDDLE,
    MouseCode.Right: sdl2.SDL_BUTTON_RIGHT,
}