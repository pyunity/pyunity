"""Template window provider, use this for creating new window providers"""

from ..errors import *
from ..core import Clock
from ..input import KeyCode
from .. import config

class Window:
    """
    A template window provider.

    """

    def __init__(self, name, resize):
        self.resize = resize

    def quit(self):
        pass

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
        while True:
            try:
                self.update_func()
                clock.Maintain()
            except KeyboardInterrupt:
                break

        self.quit()

keyMap = {
    KeyCode.A: "A",
    KeyCode.B: "B",
    KeyCode.C: "C",
    KeyCode.D: "D",
    KeyCode.E: "E",
    KeyCode.F: "F",
    KeyCode.G: "G",
    KeyCode.H: "H",
    KeyCode.I: "I",
    KeyCode.J: "J",
    KeyCode.K: "K",
    KeyCode.L: "L",
    KeyCode.M: "M",
    KeyCode.N: "N",
    KeyCode.O: "O",
    KeyCode.P: "P",
    KeyCode.Q: "Q",
    KeyCode.R: "R",
    KeyCode.S: "S",
    KeyCode.T: "T",
    KeyCode.U: "U",
    KeyCode.V: "V",
    KeyCode.W: "W",
    KeyCode.X: "X",
    KeyCode.Y: "Y",
    KeyCode.Z: "Z",
    KeyCode.Space: "SPACE",
    KeyCode.Alpha0: "0",
    KeyCode.Alpha1: "1",
    KeyCode.Alpha2: "2",
    KeyCode.Alpha3: "3",
    KeyCode.Alpha4: "4",
    KeyCode.Alpha5: "5",
    KeyCode.Alpha6: "6",
    KeyCode.Alpha7: "7",
    KeyCode.Alpha8: "8",
    KeyCode.Alpha9: "9",
    KeyCode.F1: "F1",
    KeyCode.F2: "F2",
    KeyCode.F3: "F3",
    KeyCode.F4: "F4",
    KeyCode.F5: "F5",
    KeyCode.F6: "F6",
    KeyCode.F7: "F7",
    KeyCode.F8: "F8",
    KeyCode.F9: "F9",
    KeyCode.F10: "F10",
    KeyCode.F11: "F11",
    KeyCode.F12: "F12",
    KeyCode.Keypad0: "KP_0",
    KeyCode.Keypad1: "KP_1",
    KeyCode.Keypad2: "KP_2",
    KeyCode.Keypad3: "KP_3",
    KeyCode.Keypad4: "KP_4",
    KeyCode.Keypad5: "KP_5",
    KeyCode.Keypad6: "KP_6",
    KeyCode.Keypad7: "KP_7",
    KeyCode.Keypad8: "KP_8",
    KeyCode.Keypad9: "KP_9",
    KeyCode.Up: "UP",
    KeyCode.Down: "DOWN",
    KeyCode.Left: "LEFT",
    KeyCode.Right: "RIGHT"
}
