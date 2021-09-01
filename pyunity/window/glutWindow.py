"""Class to create a window using FreeGLUT."""

from OpenGL import GLUT as glut
from ..input import KeyCode, KeyState  # lgtm [py/unused-import]
from .. import config, Logger

class Window:
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
        glut.glutCreateWindow(name)

        Logger.Log(Logger.WARN, "GLUT window doesn't support user input")

    def start(self, update_func):
        """
        Start the main loop of the window.

        Parameters
        ----------
        update_func : function
            The function that calls the OpenGL calls.

        """
        self.update_func = update_func
        glut.glutDisplayFunc(self.display)
        glut.glutReshapeFunc(self.resize)

        self.schedule_update(0)
        glut.glutMainLoop()

    def schedule_update(self, t):
        """Starts the window refreshing."""
        glut.glutPostRedisplay()
        glut.glutTimerFunc(1000 // self.config.fps, self.schedule_update, 0)

    def display(self):
        """Function to render in the scene."""
        self.update_func()
        glut.glutSwapBuffers()

    def quit(self):
        glut.glutDestroyWindow(glut.glutGetWindow())
    
    def get_key(self, keycode, keystate):
        return False
    
    def get_mouse(self, mousecode, keystate):
        return False
