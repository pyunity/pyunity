## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""Class to manage console input as a window provider."""

from pyunity import Logger
from pyunity.errors import WindowProviderException
from pyunity.window import ABCWindow
from .egl import setupPlatform

setupPlatform()
import OpenGL.EGL as egl
import OpenGL.GL as gl

eglDpy = egl.eglGetDisplay(egl.EGL_DEFAULT_DISPLAY)
err = egl.eglGetError()
if err != egl.EGL_SUCCESS:
    raise WindowProviderException("EGL error: " + str(err))

def convert(type, l):
    return (type * len(l))(*l)

def getEglCfg():
    configAttribs = convert(gl.GLint, [
        egl.EGL_SURFACE_TYPE, egl.EGL_PBUFFER_BIT,
        egl.EGL_BLUE_SIZE, 8,
        egl.EGL_GREEN_SIZE, 8,
        egl.EGL_RED_SIZE, 8,
        egl.EGL_DEPTH_SIZE, 8,
        egl.EGL_RENDERABLE_TYPE, egl.EGL_OPENGL_BIT,
        egl.EGL_NONE
    ])
    eglCfgs = (gl.GLvoidp * 1)()
    eglCfgSize = (gl.GLint * 1)(2)
    egl.eglChooseConfig(eglDpy, configAttribs, eglCfgs, 1, eglCfgSize)
    return eglCfgs[0]

class Window(ABCWindow):
    """
    A window provider that uses EGL and
    runs headlessly.

    """

    def __init__(self, name):
        self.name = name

        major, minor = (gl.GLint * 1)(), (gl.GLint * 1)()
        egl.eglInitialize(eglDpy, major, minor)

        self.eglCfg = getEglCfg()
        if self.eglCfg is None:
            raise WindowProviderException("Could not get EGL config")

        pbufferAttribs = [
            egl.EGL_WIDTH, 800,
            egl.EGL_HEIGHT, 500,
            egl.EGL_NONE
        ]
        self.eglSurf = egl.eglCreatePbufferSurface(eglDpy, self.eglCfg, pbufferAttribs)
        egl.eglBindAPI(egl.EGL_OPENGL_API)
        contextAttribs = [
            egl.EGL_CONTEXT_MAJOR_VERSION, 3,
            egl.EGL_CONTEXT_MINOR_VERSION, 3,
            egl.EGL_NONE
        ]
        self.eglCtx = egl.eglCreateContext(eglDpy, self.eglCfg, None, contextAttribs)
        egl.eglMakeCurrent(eglDpy, self.eglSurf, self.eglSurf, self.eglCtx)

    def setResize(self, resize):
        self.resize = resize # not needed, surface shouldn't change size

    def refresh(self):
        pass

    def quit(self):
        Logger.LogLine(Logger.DEBUG, "Exiting")
        egl.eglMakeCurrent(eglDpy, None, None, None)
        egl.eglDestroySurface(eglDpy, self.eglSurf)
        egl.eglDestroyContext(eglDpy, self.eglCtx)
        egl.eglTerminate(eglDpy)

    def updateFunc(self):
        pass

    def getKey(self, keycode, keystate):
        return False

    def getMouse(self, mousecode, keystate):
        return False

    def getMousePos(self):
        return (0, 0)
