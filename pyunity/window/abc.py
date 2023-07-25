## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""
Abstract base class for window providers.
Imported into ``pyunity.Window``.

"""

__all__ = ["ABCMessage", "ABCWindow"]

from ..values import ABCException, ABCMeta, abstractmethod

class ABCMessage(ABCException):
    pass

class ABCWindow(metaclass=ABCMeta):
    """
    Abstract base class that window providers
    should subclass and define methods of.

    Parameters
    ----------
    name : str
        Name to display on window title.

    """

    def __init__(self, name):
        pass

    @classmethod
    def __init_subclass__(cls, **kwargs):
        if "message" in kwargs:
            raise ABCMessage(kwargs["message"])
        super(ABCWindow, cls).__init_subclass__(**kwargs)

    @abstractmethod
    def setResize(self, resize):
        """
        Sets the resize function, which has a signature
        of ``def Resize(width, height):``. This should
        be bound to the appropriate callback handler
        of the window.

        Parameters
        ----------
        resize : function
            Resize function

        """
        pass

    @abstractmethod
    def getMouse(self, mousecode, keystate):
        """
        Get mouse state for specific mouse button
        and state.

        Parameters
        ----------
        mousecode : MouseCode
            Query button
        keystate : KeyState
            Query state

        Returns
        -------
        bool
            If the query button matches the query state.
            Note that both :attr:`KeyState.PRESS` and
            :attr:`KeyState.DOWN` will match a query
            of :attr:`KeyState.PRESS` because when a button
            is first hit it is still pressed down.

        Notes
        -----
        A good starting point is this example function:

        .. code-block:: python

            def getMouse(self, mousecode, keystate):
                mouse = mouseMap[mousecode]
                if keystate == KeyState.PRESS:
                    if self.mouse[mouse] in [KeyState.PRESS, KeyState.DOWN]:
                        return True
                if self.mouse[mouse] == keystate:
                    return True
                return False

        where ``mouseMap`` is a mapping of :class:`MouseCode` to
        the window provider's own representation of mouse buttons,
        `self.mouse` is a mapping of the window provider's own
        representation of mouse buttons to :class:`KeyState`. This
        makes it easy to both query and set the keystates of the mouse.

        """
        pass

    @abstractmethod
    def getKey(self, keycode, keystate):
        """
        Get key state for specific key
        and state.

        Parameters
        ----------
        keycode : KeyCode
            Query key
        keystate : KeyState
            Query state

        Returns
        -------
        bool
            If the query key matches the query state.
            Note that both :attr:`KeyState.PRESS` and
            :attr:`KeyState.DOWN` will match a query
            of :attr:`KeyState.PRESS` because when a key
            is first hit it is still pressed down.

        Notes
        -----
        A good starting point is this example function:

        .. code-block:: python

            def getKey(self, keycode, keystate):
                key = keyMap[keycode]
                if keystate == KeyState.PRESS:
                    if self.keys[key] in [KeyState.PRESS, KeyState.DOWN]:
                        return True
                if self.keys[key] == keystate:
                    return True
                return False

        where ``keyMap`` is a mapping of :class:`KeyCode` to
        the window provider's own representation of keys,
        `self.keys` is a mapping of the window provider's own
        representation of keys to :class:`KeyState`. This
        makes it easy to both query and set the keystates of the keyboard.

        """
        pass

    @abstractmethod
    def getMousePos(self):
        """
        Get a tuple of (x, y) representing the position
        of the mouse inside the window.

        Returns
        -------
        tuple
            Mouse coordinates

        """
        pass

    @abstractmethod
    def refresh(self):
        """
        Refreshes and redraws the screen.

        """
        pass

    @abstractmethod
    def updateFunc(self):
        """
        Update the input of keys and mouse.
        Also checks to quit. Don't close the
        window in this method. Close it in
        :meth:`quit` instead.

        Raises
        ------
        PyUnityExit
            When the window should

        """
        pass

    @abstractmethod
    def quit(self):
        """
        Closes the window.

        """
        pass
