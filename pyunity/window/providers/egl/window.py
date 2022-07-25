## Copyright (c) 2020-2022 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""Class to manage console input as a window provider."""

from pyunity.window import ABCWindow
from pyunity.values import Clock
from pyunity import config, Logger
from .egl import *

eglDpy = eglGetDisplay(EGL.DEFAULT_DISPLAY)
print(eglGetError())

class Window(ABCWindow):
    """
    A window provider that uses EGL and
    runs headlessly.

    """

    def __init__(self, name, resize):
        self.name = name
        self.resize = resize # not actually needed

        eglInitialize(eglDpy)

        configAttribs = EGLList(
            EGL.SURFACE_TYPE, EGL.PBUFFER_BIT,
            EGL.BLUE_SIZE, 8,
            EGL.GREEN_SIZE, 8,
            EGL.RED_SIZE, 8,
            EGL.DEPTH_SIZE, 8,
            EGL.RENDERABLE_TYPE, EGL.OPENGL_BIT,
            EGL.NONE
        )
        self.eglCfg = eglChooseConfig(eglDpy, configAttribs, 1)[0]
        pbufferAttribs = EGLList(
            EGL.WIDTH, 800,
            EGL.HEIGHT, 500,
            EGL.NONE
        )
        self.eglSurf = eglCreatePbufferSurface(eglDpy, self.eglCfg, pbufferAttribs)
        eglBindAPI(EGL.OPENGL_API)
        contextAttribs = EGLList(
            EGL.CONTEXT_CLIENT_VERSION, 330,
            EGL.NONE
        )
        self.eglCtx = eglCreateContext(eglDpy, self.eglCfg, None, contextAttribs)
        eglMakeCurrent(eglDpy, self.eglSurf, self.eglSurf, self.eglCtx)

    def refresh(self):
        pass

    def quit(self):
        Logger.LogLine(Logger.DEBUG, "Exiting")
        eglMakeCurrent(eglDpy, None, None, None)
        eglDestroySurface(eglDpy, self.eglSurf)
        eglDestroyContext(eglDpy, self.eglCtx)
        eglTerminate(eglDpy)

    def start(self, updateFunc):
        self.updateFunc = updateFunc

        done = False
        clock = Clock()
        clock.Start(config.fps)
        while not done:
            try:
                self.updateFunc()
                clock.Maintain()
            except KeyboardInterrupt:
                done = True

        self.quit()

    def getKey(self, keycode, keystate):
        return False

    def getMouse(self, mousecode, keystate):
        return False

    def getMousePos(self):
        return (0, 0)
