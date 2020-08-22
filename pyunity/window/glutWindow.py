from OpenGL.GLUT import *
from .. import config

class Window:
    """
    A window provider that uses FreeGLUT.
    
    """

    def __init__(self, size, name):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowPosition(50, 50)
        glutInitWindowSize(*config.size)
        glutCreateWindow(name)
    
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
    
    def __schedule_update(self, t):
        glutPostRedisplay()
        glutTimerFunc(1000 // config.fps, self.__schedule_update, 0)
    
    def display(self):
        """
        Function to render in the scene.

        """
        self.updateFunc()
        glutSwapBuffers()