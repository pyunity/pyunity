## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

from . import TestCase
from pyunity import Window, PyUnityException, Logger, config

class CustomWindow(Window.ABCWindow):
    def __init__(self, name):
        pass

    def setResize(self, resize):
        pass

    def getMouse(self, mousecode, keystate):
        return False

    def getKey(self, keycode, keystate):
        return False

    def getMousePos(self):
        return (0, 0)

    def refresh(self):
        pass

    def quit(self):
        pass

    def updateFunc(self):
        pass

class TestWindow(TestCase):
    def testSet(self):
        with self.assertRaises(PyUnityException) as exc:
            Window.CustomWindowProvider(1)
        assert exc.value == "Provided window provider is not a class"

        with self.assertRaises(PyUnityException) as exc:
            Window.CustomWindowProvider(int)
        assert exc.value == "Provided window provider does not subclass Window.ABCWindow"

        with Logger.TempRedirect(silent=True) as r:
            Window.CustomWindowProvider(CustomWindow)
        assert r.get() == "Using window provider CustomWindow\n"

        assert config.windowProvider is CustomWindow
