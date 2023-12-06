## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""
Class to create a window using FreeGLUT.

NOTE: This window provider has been deprecated since PyUnity 0.5.0.
There may be future updates, however it is most likely going to stay
deprecated.

"""

from pyunity import config
from pyunity.window import ABCWindow
from OpenGL import GLUT as glut

class Window(ABCWindow, message="This window provider has been deprecated since PyUnity 0.5.0."):
    """A window provider that uses FreeGLUT."""

    def __init__(self, name, resize):
        self.resize = resize

        glut.glutInit()
        glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_DEPTH)
        # glut.glutInitWindowPosition(
        #     (glut.glutGet(glut.GLUT_SCREEN_WIDTH) - config.size[0]) // 2,
        #     (glut.glutGet(glut.GLUT_SCREEN_HEIGHT) - config.size[1]) // 2)
        glut.glutInitWindowPosition(100, 100)
        glut.glutInitWindowSize(*config.size)
        self.winID = glut.glutCreateWindow(name)

    def refresh(self):
        glut.glutSwapBuffers()

    def start(self, updateFunc):
        """
        Start the main loop of the window.

        Parameters
        ----------
        updateFunc : function
            The function that calls the OpenGL calls.

        """
        self.updateFunc = updateFunc
        glut.glutDisplayFunc(self.display)
        glut.glutReshapeFunc(self.resize)

        self.scheduleUpdate(0)
        glut.glutMainLoop()

    def scheduleUpdate(self, t):
        """Starts the window refreshing."""
        glut.glutPostRedisplay()
        glut.glutTimerFunc(1000 // self.config.fps, self.scheduleUpdate, 0)

    def display(self):
        """Function to render in the scene."""
        self.updateFunc()
        glut.glutSwapBuffers()

    def quit(self):
        glut.glutDestroyWindow(glut.glutGetWindow())

    def getKey(self, keycode, keystate):
        return False

    def getMouse(self, mousecode, keystate):
        return False
