"""
Module to represent files.

"""

from OpenGL import GL as gl
from PIL import Image

class Script:
    def __init__(self, path):
        self.path = path

class Texture2D:
    def __init__(self, path):
        self.path = path
        self.img = Image.open(self.path)
        self.texData = self.img.tostring('raw', 'RGBX', 0, -1)
        texName = [0]
        gl.glGenTextures(1, texName)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texName[0])
        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, 256, 256, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, self.texData)
        gl.glEnable(gl.GL_TEXTURE_2D)
        self.texture = texName[0]

class Prefab:
    def __init__(self, path):
        self.path = path

class Shader:
    def __init__(self, path):
        self.path = path