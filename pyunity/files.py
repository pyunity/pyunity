"""
Module to represent files.

"""

__all__ = ["Texture2D", "Prefab"]

from OpenGL import GL as gl
from PIL import Image

class Script:
    def __init__(self, path):
        self.path = path

class Texture2D:
    """
    Class to represent a texture.

    """

    def __init__(self, path):
        self.path = path
        self.loaded = False

    def load(self):
        """
        Loads the texture and sets up an OpenGL
        texture name.

        """
        img = Image.open(self.path)
        img_data = img.tobytes()
        width, height = img.size
        self.texture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture)
        gl.glTexParameterf(
            gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameterf(
            gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, width, height, 0,
                        gl.GL_RGB, gl.GL_UNSIGNED_BYTE, img_data)
        gl.glEnable(gl.GL_TEXTURE_2D)
        self.loaded = True

    def use(self):
        """
        Binds the texture for usage. The texture is
        reloaded if it hasn't already been.

        """
        if not self.loaded:
            self.load()
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture)

class Prefab:
    def __init__(self, gameObject, components):
        self.gameObject = gameObject
        self.components = components
