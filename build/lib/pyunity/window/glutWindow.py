from OpenGL.GLUT import *
from .. import config

class Window:
    def __init__(self, size, name):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowPosition(50, 50)
        glutInitWindowSize(*config.size)
        glutCreateWindow(name)
    
    def start(self, updateFunc):
        self.updateFunc = updateFunc
        glutDisplayFunc(self.display)

        glutTimerFunc(1000 // config.fps, self.schedule_update, 0)
        glutMainLoop()
    
    def schedule_update(self, t):
        glutPostRedisplay()
        glutTimerFunc(1000 // config.fps, self.schedule_update, 0)
    
    def display(self):
        self.updateFunc()
        glutSwapBuffers()