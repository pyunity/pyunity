"""
Example window provider.

See https://docs.pyunity.x10.bz/en/latest/api/pyunity.window.abc.html

"""

from pyunity.window import ABCWindow

class Window(ABCWindow, message="Cannot load example window provider"):
    def __init__(self, name):
        pass

    def refresh(self):
        pass

    def quit(self):
        pass

    def setResize(self, resize):
        pass

    def updateFunc(self):
        pass
