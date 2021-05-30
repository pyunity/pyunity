"""
Classes to aid in rendering in a Scene.

"""
from .core import SingleComponent
from OpenGL import GL as gl
from OpenGL import GLU as glu


class Camera(SingleComponent):
    """
    Component to hold data about the camera in a scene.

    Attributes
    ----------
    fov : int
        Fov in degrees measured horizontally. Defaults to 90.
    near : float
        Distance of the near plane in the camera frustrum. Defaults to 0.05.
    far : float
        Distance of the far plane in the camera frustrum. Defaults to 100.
    clearColor : tuple
        Tuple of 4 floats of the clear color of the camera. Defaults to (.1, .1, .1, 1).
        Color mode is RGBA.

    """

    def __init__(self):
        super(Camera, self).__init__()
        self.fov = 90
        self.near = 0.05
        self.far = 100
        self.clearColor = (0, 0, 0, 1)

    def Resize(self, width, height):
        """
        Resizes the viewport on screen size change.

        Parameters
        ----------
        width : int
            Width of new window
        height : int
            Height of new window

        """
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(
            self.fov / width * height,
            width / height,
            self.near,
            self.far)
        gl.glMatrixMode(gl.GL_MODELVIEW)
