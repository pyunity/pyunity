__all__ = ["KeyState", "KeyCode", "MouseCode", "Input"]

from enum import IntEnum, auto
from .values import clamp, ImmutableStruct
from .errors import PyUnityException
from .scenes import SceneManager
from .values import Vector3

class KeyState(IntEnum):
    UP = auto()
    DOWN = auto()
    PRESS = auto()
    NONE = auto()

class KeyCode(IntEnum):
    A = auto()
    B = auto()
    C = auto()
    D = auto()
    E = auto()
    F = auto()
    G = auto()
    H = auto()
    I = auto()
    J = auto()
    K = auto()
    L = auto()
    M = auto()
    N = auto()
    O = auto()
    P = auto()
    Q = auto()
    R = auto()
    S = auto()
    T = auto()
    U = auto()
    V = auto()
    W = auto()
    X = auto()
    Y = auto()
    Z = auto()
    Space = auto()
    Alpha0 = auto()
    Alpha1 = auto()
    Alpha2 = auto()
    Alpha3 = auto()
    Alpha4 = auto()
    Alpha5 = auto()
    Alpha6 = auto()
    Alpha7 = auto()
    Alpha8 = auto()
    Alpha9 = auto()
    F1 = auto()
    F2 = auto()
    F3 = auto()
    F4 = auto()
    F5 = auto()
    F6 = auto()
    F7 = auto()
    F8 = auto()
    F9 = auto()
    F10 = auto()
    F11 = auto()
    F12 = auto()
    Keypad0 = auto()
    Keypad1 = auto()
    Keypad2 = auto()
    Keypad3 = auto()
    Keypad4 = auto()
    Keypad5 = auto()
    Keypad6 = auto()
    Keypad7 = auto()
    Keypad8 = auto()
    Keypad9 = auto()
    Up = auto()
    Down = auto()
    Left = auto()
    Right = auto()

class MouseCode(IntEnum):
    Left = auto()
    Middle = auto()
    Right = auto()

class KeyboardAxis:
    def __init__(self, name, speed, positive, negative):
        self.positive = positive
        self.negative = negative
        self.value = 0
        self.name = name
        self.speed = speed

    def get_value(self, dt):
        change = sum([Input.GetKey(key) for key in self.positive]) - \
            sum([Input.GetKey(key) for key in self.negative])
        if change == 0:
            if self.value != 0:
                change = -abs(self.value) / self.value
                if abs(dt) > abs(self.value):
                    self.value = 0
                    return 0
            else:
                return 0
        self.value += clamp(change, -1, 1) * dt * self.speed
        self.value = clamp(self.value, -1, 1)
        return self.value

class Input(metaclass=ImmutableStruct):
    _names = ["mousePosition"]
    @classmethod
    def GetKey(cls, keycode):
        """
        Check if key is pressed at moment of function call

        Parameters
        ----------
        keycode : KeyCode
            Key to query

        Returns
        -------
        boolean
            If the key is pressed

        """
        return SceneManager.windowObject.get_key(keycode, KeyState.PRESS)

    @classmethod
    def GetKeyUp(cls, keycode):
        """
        Check if key was released this frame.

        Parameters
        ----------
        keycode : KeyCode
            Key to query

        Returns
        -------
        boolean
            If the key was released

        """
        return SceneManager.windowObject.get_key(keycode, KeyState.UP)

    @classmethod
    def GetKeyDown(cls, keycode):
        """
        Check if key was pressed down this frame.

        Parameters
        ----------
        keycode : KeyCode
            Key to query

        Returns
        -------
        boolean
            If the key was pressed down

        """
        return SceneManager.windowObject.get_key(keycode, KeyState.DOWN)

    @classmethod
    def GetMouse(cls, mousecode):
        """
        Check if mouse button is pressed at moment of function call

        Parameters
        ----------
        mousecode : MouseCode
            Mouse button to query

        Returns
        -------
        boolean
            If the mouse button is pressed

        """
        return SceneManager.windowObject.get_mouse(mousecode, KeyState.PRESS)

    @classmethod
    def GetMouseUp(cls, mousecode):
        """
        Check if mouse button was released this frame.

        Parameters
        ----------
        mousecode : MouseCode
            Mouse button to query

        Returns
        -------
        boolean
            If the mouse button was released

        """
        return SceneManager.windowObject.get_mouse(mousecode, KeyState.UP)

    @classmethod
    def GetMouseDown(cls, mousecode):
        """
        Check if mouse button was pressed down this frame.

        Parameters
        ----------
        mousecode : MouseCode
            Mouse button to query

        Returns
        -------
        boolean
            If the mouse button was pressed down

        """
        return SceneManager.windowObject.get_mouse(mousecode, KeyState.DOWN)

    _axes = {"MouseX": 0, "MouseY": 0, "Horizontal": 0, "Vertical": 0}
    _axis_objects = [
        KeyboardAxis("Horizontal", 3,
                     [KeyCode.D, KeyCode.Right],
                     [KeyCode.A, KeyCode.Left]
                     ),
        KeyboardAxis("Vertical", 3,
                     [KeyCode.W, KeyCode.Up],
                     [KeyCode.S, KeyCode.Down]
                     ),
    ]

    @classmethod
    def GetAxis(cls, axis):
        if axis not in cls._axes:
            raise PyUnityException(repr(axis) + " is not a valid axis")
        return cls._axes[axis]

    mousePosition = None
    _mouse_last = None

    @classmethod
    def UpdateAxes(cls, dt):
        cls._set("mousePosition", Vector3(
            *SceneManager.windowObject.get_mouse_pos(), 0))

        new = cls.mousePosition
        if cls._mouse_last is None:
            diff = new
        else:
            diff = new - cls._mouse_last
        cls._mouse_last = new
        cls._axes["MouseX"] = diff.x
        cls._axes["MouseY"] = diff.y

        for axis in cls._axis_objects:
            cls._axes[axis.name] = axis.get_value(dt)
