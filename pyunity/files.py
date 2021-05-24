"""
Module to represent files.

"""
from OpenGL import GL
from PIL import Image

class Script:
    def __init__(self, path):
        self.path = path

class Texture2D:
    """
    Class to represent a texture.
    
    """


    @staticmethod
    def loadTexture(path):
        img = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
        img_data = str(img.tobytes())
        width, height = img.size

        texture = GL.glGenTextures(1)
        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR_MIPMAP_LINEAR)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, width, height, 0,
            GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, img_data)
        GL.glGenerateMipmap(GL.GL_TEXTURE_2D)
        return texture

    def __init__(self, path):
        self.path = path
        self.texture = Texture2D.loadTexture(self.path)

class Prefab:
    def __init__(self, path):
        self.path = path

class Shader:
    def __init__(self, path):
        self.path = path