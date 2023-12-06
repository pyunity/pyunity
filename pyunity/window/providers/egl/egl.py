## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import Logger
from OpenGL.platform import ctypesloader
from OpenGL.platform.baseplatform import lazy_property
import os
import ctypes

def setupPlatform():
    if os.name == "nt":
        setupWin32Platform()

def setupWin32Platform():
    @lazy_property
    def EGL(self):
        for name in ("EGL", "libEGL"):
            Logger.LogLine(Logger.INFO, "Attempting to load", name + ".dll")
            try:
                lib = ctypesloader.loadLibrary(
                    ctypes.cdll,
                    name,
                    mode=ctypes.RTLD_GLOBAL
                )
                if lib:
                    Logger.LogLine(Logger.INFO, name + ".dll loaded to", lib)
                    return lib
            except OSError:
                Logger.LogLine(Logger.INFO, name + ".dll not found")
        raise OSError("No GL/OpenGL library available")

    @lazy_property
    def GLES2(self):
        for name in ("GLESv2", "libGLESv2"):
            Logger.LogLine(Logger.INFO, "Attempting to load", name + ".dll")
            try:
                lib = ctypesloader.loadLibrary(
                    ctypes.cdll,
                    name,
                    mode=ctypes.RTLD_GLOBAL
                )
                if lib:
                    Logger.LogLine(Logger.INFO, name + ".dll loaded to", lib)
                    return lib
            except OSError:
                Logger.LogLine(Logger.INFO, name + ".dll not found")
        raise OSError("No GL/OpenGL library available")

    from OpenGL.platform.win32 import Win32Platform
    Win32Platform.EGL = EGL
    Win32Platform.GLES2 = GLES2
