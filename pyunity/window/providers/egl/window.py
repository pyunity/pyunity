# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

"""Class to manage console input as a window provider."""

from pyunity.window import ABCWindow
from pyunity.values import Clock
from pyunity import config
from .egl import *

eglDpy = eglGetDisplay(0)

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
            EGL_SURFACE_TYPE, EGL_PBUFFER_BIT,
            EGL_BLUE_SIZE, 8,
            EGL_GREEN_SIZE, 8,
            EGL_RED_SIZE, 8,
            EGL_DEPTH_SIZE, 8,
            EGL_RENDERABLE_TYPE, EGL_OPENGL_BIT,
            EGL_NONE
        )
        self.eglCfg = eglChooseConfig(eglDpy, configAttribs, 1)[0]
        pbufferAttribs = EGLList(
            EGL_WIDTH, 800,
            EGL_HEIGHT, 500,
            EGL_NONE
        )
        self.eglSurf = eglCreatePbufferSurface(eglDpy, self.eglCfg, pbufferAttribs)
        eglBindAPI(EGL_OPENGL_API)
        contextAttribs = EGLList(
            EGL_CONTEXT_CLIENT_VERSION, 330,
            EGL_NONE
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
