from OpenGL.GLUT import *

class Window:
    """A window provider that uses FreeGLUT."""

    def __init__(self, size, name):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowPosition(
            (glutGet(GLUT_SCREEN_WIDTH) - size[0]) // 2,
            (glutGet(GLUT_SCREEN_HEIGHT) - size[1]) // 2)
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

        self.schedule_update()
        glutMainLoop()
    
    def schedule_update(self, t):
        """Starts the window refreshing."""
        glutPostRedisplay()
        glutTimerFunc(1000 // 60, self.schedule_update, 0)
    
    def display(self):
        """Function to render in the scene."""
        self.updateFunc()
        glutSwapBuffers()