## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

__all__ = ["KeyState", "KeyCode", "MouseCode", "Input", "KeyboardAxis"]

from .errors import PyUnityException
from .scenes import SceneManager
from .values import ImmutableStruct, Mathf, Vector3
from enum import IntEnum, auto
import os

from enum import IntEnum, auto

class KeyState(IntEnum):
    UP = auto()
    DOWN = auto()
    PRESS = auto()
    NONE = auto()

class KeyCode(IntEnum):
    pass

_keys = {}
for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    _keys[letter] = auto()

_keys['Space'] = auto()

for i in range(10):
    _keys[f'Alpha{i}'] = auto()

for i in range(1, 13):
    _keys[f'F{i}'] = auto()

for i in range(10):
    _keys[f'Keypad{i}'] = auto()

for direction in ['Up', 'Down', 'Left', 'Right']:
    _keys[direction] = auto()

# KeyCode enum'unu oluştur
KeyCode = IntEnum('KeyCode', _keys)

class MouseCode(IntEnum):
    Left = auto()
    Middle = auto()
    Right = auto()

class KeyboardAxis:
    def __init__(self, name, speed, positive, negative):
        self.positive = positive
        self.negative = negative
        self.value = 0
        self.raw = 0
        self.name = name
        self.speed = speed

    def getValue(self, dt):
        change = sum([Input.GetKey(key) for key in self.positive]) - \
            sum([Input.GetKey(key) for key in self.negative])
        self.raw = change
        if change == 0:
            if self.value != 0:
                change = -abs(self.value) / self.value
                if abs(dt) > abs(self.value):
                    self.value = 0
                    return 0
            else:
                return 0
        self.value += Mathf.Clamp(change, -1, 1) * dt * self.speed
        self.value = Mathf.Clamp(self.value, -1, 1)
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
        if os.environ["PYUNITY_INTERACTIVE"] != "1":
            return False
        return SceneManager.runner.window.getKey(keycode, KeyState.PRESS)

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
        if os.environ["PYUNITY_INTERACTIVE"] != "1":
            return False
        return SceneManager.runner.window.getKey(keycode, KeyState.UP)

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
        if os.environ["PYUNITY_INTERACTIVE"] != "1":
            return False
        return SceneManager.runner.window.getKey(keycode, KeyState.DOWN)

    @classmethod
    def GetKeyState(cls, keycode, keystate):
        """
        Check key state at moment of function call

        Parameters
        ----------
        keycode : KeyCode
            Key to query
        keystate : KeyState
            Keystate, either KeyState.PRESS, KeyState.UP or KeyState.DOWN

        Returns
        -------
        boolean
            If the key state matches

        """
        if os.environ["PYUNITY_INTERACTIVE"] != "1":
            return False
        return SceneManager.runner.window.getKey(keycode, keystate)

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
        if os.environ["PYUNITY_INTERACTIVE"] != "1":
            return False
        return SceneManager.runner.window.getMouse(mousecode, KeyState.PRESS)

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
        if os.environ["PYUNITY_INTERACTIVE"] != "1":
            return False
        return SceneManager.runner.window.getMouse(mousecode, KeyState.UP)

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
        if os.environ["PYUNITY_INTERACTIVE"] != "1":
            return False
        return SceneManager.runner.window.getMouse(mousecode, KeyState.DOWN)

    @classmethod
    def GetMouseState(cls, mousecode, mousestate):
        """
        Check for mouse button state at moment of function call

        Parameters
        ----------
        mousecode : MouseCode
            Key to query
        mousestate : KeyState
            Keystate, either KeyState.PRESS, KeyState.UP or KeyState.DOWN

        Returns
        -------
        boolean
            If the mouse button state matches

        """
        if os.environ["PYUNITY_INTERACTIVE"] != "1":
            return False
        return SceneManager.runner.window.getMouse(mousecode, mousestate)

    _axes = {"MouseX": 0, "MouseY": 0, "Horizontal": 0, "Vertical": 0}
    _axisObjects = {
        "Horizontal": KeyboardAxis(
            "Horizontal", 3,
            [KeyCode.D, KeyCode.Right],
            [KeyCode.A, KeyCode.Left]
        ),
        "Vertical": KeyboardAxis(
            "Vertical", 3,
            [KeyCode.W, KeyCode.Up],
            [KeyCode.S, KeyCode.Down]
        ),
    }

    @classmethod
    def GetAxis(cls, axis):
        """
        Get the value for the specified axis. This is
        always between -1 and 1.

        Parameters
        ----------
        axis : str
            Specified axis

        Returns
        -------
        float
            Axis value

        Raises
        ------
        PyUnityException
            If the axis is not a valid axis
        """
        if axis not in cls._axes:
            raise PyUnityException(f"Invalid axis: {axis!r}")
        if os.environ["PYUNITY_INTERACTIVE"] != "1":
            return 0
        return cls._axes[axis]

    @classmethod
    def GetRawAxis(cls, axis):
        """
        Get the raw value for the specified axis. This is
        always either -1, 0 or 1.

        Parameters
        ----------
        axis : str
            Specified axis

        Returns
        -------
        float
            Raw axis value

        Raises
        ------
        PyUnityException
            If the axis is not a valid axis
        """
        if axis not in cls._axisObjects:
            raise PyUnityException(f"Invalid axis: {axis!r}")
        if os.environ["PYUNITY_INTERACTIVE"] != "1":
            return 0
        return cls._axisObjects[axis].raw

    mousePosition = None
    _mouseLast = None

    @classmethod
    def UpdateAxes(cls, dt):
        cls._set("mousePosition", Vector3(
            *SceneManager.runner.window.getMousePos(), 0))

        new = cls.mousePosition
        if cls._mouseLast is None:
            diff = new
        else:
            diff = new - cls._mouseLast
        cls._mouseLast = new
        cls._axes["MouseX"] = diff.x
        cls._axes["MouseY"] = diff.y

        for axis in cls._axisObjects.values():
            cls._axes[axis.name] = axis.getValue(dt)
