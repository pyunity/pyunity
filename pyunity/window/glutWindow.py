from OpenGL.GLUT import *

class Window:
    """A window provider that uses FreeGLUT."""

    def __init__(self, config, name):
        self.config = config
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowPosition(
            (glutGet(GLUT_SCREEN_WIDTH) - size[0]) // 2,
            (glutGet(GLUT_SCREEN_HEIGHT) - size[1]) // 2)
        glutInitWindowSize(*config.size)
        glutCreateWindow(name)
    
    def start(self, update_func):
        """
        Start the main loop of the window.

        Parameters
        ----------
        update_func : function
            The function that calls the OpenGL calls.
        
        """
        self.update_func = update_func
        glutDisplayFunc(self.display)

        self.schedule_update()
        glutMainLoop()
    
    def schedule_update(self, t):
        """Starts the window refreshing."""
        glutPostRedisplay()
        glutTimerFunc(1000 // self.config.fps, self.schedule_update, 0)
    
    def display(self):
        """Function to render in the scene."""
        self.update_func()
        glutSwapBuffers()