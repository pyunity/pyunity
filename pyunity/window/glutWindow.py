from OpenGL.GLUT import *
from .. import config

class Window:
    """
    A window provider that uses FreeGLUT.
    
    """

    def __init__(self, size, name):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowPosition(
            (glutGet(GLUT_SCREEN_WIDTH) - size[0]) // 2,
            (glutGet(GLUT_SCREEN_HEIGHT) - size[1]) // 2)
        glutInitWindowSize(*config.size)
        glutCreateWindow(name)
        glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_CONTINUE_EXECUTION)
    
    def start(self, updateFunc):
        """
        Start the main loop of the window.

        Parameters
        ----------
        updateFunc : function
            The function that calls the OpenGL calls.
        
        """
        self.updateFunc = updateFunc
        glutDisplayFunc(self.display)

        glutTimerFunc(1000 // config.fps, self.__schedule_update, 0)
        glutMainLoop()
        print("h1")
    
    def __schedule_update(self, t):
        try:
            glutPostRedisplay()
            glutTimerFunc(1000 // config.fps, self.__schedule_update, 0)
        except:
            glutLeaveMainLoop()
    
    def display(self):
        """
        Function to render in the scene.

        """
        self.updateFunc()
        glutSwapBuffers()