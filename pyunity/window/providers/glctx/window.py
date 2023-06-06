"""
Example window provider.

See https://docs.pyunity.x10.bz/en/latest/api/pyunity.window.abc.html

"""

from pyunity.window import ABCWindow
import glcontext

class Window(ABCWindow):
    def __init__(self, name):
        self.name = name

        backend = glcontext.default_backend()
        self.ctx = backend(glversion=330, mode="standalone")

    def refresh(self):
        pass

    def quit(self):
        pass

    def setResize(self, resize):
        pass

    def updateFunc(self):
        pass

    def getMouse(self, mousecode, keystate):
        return False

    def getKey(self, keycode, keystate):
        return False

    def getMousePos(self):
        return (0, 0)
