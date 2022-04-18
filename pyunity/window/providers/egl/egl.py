# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

# __all__ = ["EGLBoolean", "EGLConfig", "EGLContext", "EGLDisplay",
#            "EGLSurface", "EGLint", "eglBindAPI", "eglChooseConfig",
#            "eglCreateContext", "eglCreatePbufferSurface",
#            "eglGetDisplay", "eglInitialize", "eglMakeCurrent",
#            "eglDestroySurface", "eglDestroyContext", "eglTerminate"]

import os
import ctypes
import ctypes.util
import functools
from pyunity import Logger, PyUnityException

search = True
if "PYUNITY_EGL_PATH" in os.environ:
    try:
        _egl = ctypes.CDLL(os.environ["PYUNITY_EGL_PATH"])
        search = False
    except FileNotFoundError:
        Logger.LogLine(Logger.DEBUG,
                       "PYUNITY_EGL_PATH environment variable specified but "
                       "path not found")
if search:
    _libname = ctypes.util.find_library("libegl")
    if _libname is None:
        raise PyUnityException("Cannot find libegl library")
    _egl = ctypes.CDLL(_libname)

def wrap(func):
    @functools.wraps(func)
    def inner(*args):
        return getattr(_egl, func.__name__)(*args)
    return inner

def returnPointer(wrapArgs, includeOutput=False):
    def decorator(func):
        @functools.wraps(func)
        def inner(*args):
            orig = getattr(_egl, func.__name__)
            newArgs = list(args)
            for argnum in wrapArgs:
                item = orig.argtypes[argnum]._type_()
                newArgs.insert(argnum, item)
            res = orig(*newArgs)
            out = []
            if includeOutput:
                out.append(res)
            for argnum in wrapArgs:
                out.append(newArgs[argnum].value)
            if len(out) == 1:
                return out[0]
            return tuple(out)
        return inner
    return decorator

def returnArray(wrapArgs, lenArgs, includeOutput=False):
    def decorator(func):
        @functools.wraps(func)
        def inner(*args):
            orig = getattr(_egl, func.__name__)
            newArgs = list(args)
            for argnum in sorted(wrapArgs + lenArgs):
                if argnum in wrapArgs:
                    item = orig.argtypes[argnum]._type_()
                else:
                    item = EGLint()
                newArgs.insert(argnum, item)
            res = orig(*newArgs)
            out = []
            if includeOutput:
                out.append(res)
            lengths = []
            for argnum in sorted(wrapArgs + lenArgs):
                if argnum in wrapArgs:
                    arr = ctypes.cast(newArgs[argnum], orig.argtypes[argnum])
                    out.append(arr)
                else:
                    lengths.append(newArgs[argnum].value)
            for i in range(len(wrapArgs)):
                arr = out[i]
                if ctypes.sizeof(arr) // ctypes.sizeof(arr[0]) != lengths[i]:
                    raise Exception("Sizeof array does not match return")
            if len(out) == 1:
                return out[0]
            return tuple(out)
        return inner
    return decorator

def length(arr):
    return ctypes.sizeof(arr) // ctypes.sizeof(arr[0])

class EGLDisplay(ctypes.c_void_p):
    pass
class EGLConfig(ctypes.c_void_p):
    pass
class EGLSurface(ctypes.c_void_p):
    pass
class EGLContext(ctypes.c_void_p):
    pass

class EGLBoolean(ctypes.c_uint):
    pass
class EGLint(ctypes.c_int):
    pass

def EGLList(*l):
    return (EGLint * len(l))(*l)

_egl.eglInitialize.restype = EGLBoolean
_egl.eglInitialize.argtypes = [
    EGLDisplay,
    ctypes.POINTER(EGLint),
    ctypes.POINTER(EGLint)
]
@returnPointer([1, 2])
def eglInitialize(display): pass

_egl.eglGetDisplay.restype = EGLDisplay
_egl.eglGetDisplay.argtypes = [EGLint]
@wrap
def eglGetDisplay(displayID): pass

_egl.eglChooseConfig.restype = EGLBoolean
_egl.eglChooseConfig.argtypes = [
    EGLDisplay,
    ctypes.POINTER(EGLint),
    ctypes.POINTER(EGLConfig),
    EGLint,
    ctypes.POINTER(EGLint)
]
@returnArray([2], [4])
def eglChooseConfig(display, attribList, configSize): pass

_egl.eglCreatePbufferSurface.restype = EGLSurface
_egl.eglCreatePbufferSurface.argtypes = [
    EGLDisplay,
    EGLConfig,
    ctypes.POINTER(EGLint)
]
@wrap
def eglCreatePbufferSurface(display, config, attribList): pass

_egl.eglBindAPI.restype = EGLBoolean
_egl.eglBindAPI.argtypes = [EGLint]
@wrap
def eglBindAPI(api): pass

_egl.eglCreateContext.restype = EGLContext
_egl.eglCreateContext.argtypes = [
    EGLDisplay,
    EGLConfig,
    EGLContext,
    ctypes.POINTER(EGLint)
]
@wrap
def eglCreateContext(display, config, shareContext, attribList): pass

_egl.eglMakeCurrent.restype = EGLBoolean
_egl.eglMakeCurrent.argtypes = [
    EGLDisplay,
    EGLSurface,
    EGLSurface,
    EGLContext
]
@wrap
def eglMakeCurrent(display, draw, read, ctx): pass

_egl.eglDestroySurface.restype = EGLBoolean
_egl.eglDestroySurface.argtypes = [
    EGLDisplay,
    EGLSurface
]
@wrap
def eglDestroySurface(display, surface): pass

_egl.eglDestroyContext.restype = EGLBoolean
_egl.eglDestroyContext.argtypes = [
    EGLDisplay,
    EGLContext
]
@wrap
def eglDestroyContext(display, context): pass

_egl.eglTerminate.restype = EGLBoolean
_egl.eglTerminate.argtypes = [EGLDisplay]
@wrap
def eglTerminate(display): pass

# Constants

EGL_DEFAULT_DISPLAY = EGLint(0)
EGL_NO_CONTEXT = EGLContext(0)
EGL_NO_DISPLAY = EGLDisplay(0)
EGL_NO_SURFACE = EGLSurface(0)

EGL_DONT_CARE = EGLint(-1)

EGL_BUFFER_SIZE = EGLint(0x3020)
EGL_ALPHA_SIZE = EGLint(0x3021)
EGL_BLUE_SIZE = EGLint(0x3022)
EGL_GREEN_SIZE = EGLint(0x3023)
EGL_RED_SIZE = EGLint(0x3024)
EGL_DEPTH_SIZE = EGLint(0x3025)
EGL_STENCIL_SIZE = EGLint(0x3026)
EGL_CONFIG_CAVEAT = EGLint(0x3027)
EGL_CONFIG_ID = EGLint(0x3028)
EGL_LEVEL = EGLint(0x3029)
EGL_MAX_PBUFFER_HEIGHT = EGLint(0x302A)
EGL_MAX_PBUFFER_PIXELS = EGLint(0x302B)
EGL_MAX_PBUFFER_WIDTH = EGLint(0x302C)
EGL_NATIVE_RENDERABLE = EGLint(0x302D)
EGL_NATIVE_VISUAL_ID = EGLint(0x302E)
EGL_NATIVE_VISUAL_TYPE = EGLint(0x302F)
EGL_SAMPLES = EGLint(0x3031)
EGL_SAMPLE_BUFFERS = EGLint(0x3032)
EGL_SURFACE_TYPE = EGLint(0x3033)
EGL_TRANSPARENT_TYPE = EGLint(0x3034)
EGL_TRANSPARENT_BLUE_VALUE = EGLint(0x3035)
EGL_TRANSPARENT_GREEN_VALUE = EGLint(0x3036)
EGL_TRANSPARENT_RED_VALUE = EGLint(0x3037)
EGL_NONE = EGLint(0x3038)
EGL_BIND_TO_TEXTURE_RGB = EGLint(0x3039)
EGL_BIND_TO_TEXTURE_RGBA = EGLint(0x303A)
EGL_MIN_SWAP_INTERVAL = EGLint(0x303B)
EGL_MAX_SWAP_INTERVAL = EGLint(0x303C)
EGL_LUMINANCE_SIZE = EGLint(0x303D)
EGL_ALPHA_MASK_SIZE = EGLint(0x303E)
EGL_COLOR_BUFFER_TYPE = EGLint(0x303F)
EGL_RENDERABLE_TYPE = EGLint(0x3040)
EGL_MATCH_NATIVE_PIXMAP = EGLint(0x3041)
EGL_CONFORMANT = EGLint(0x3042)

EGL_SLOW_CONFIG = EGLint(0x3050)
EGL_NON_CONFORMANT_CONFIG = EGLint(0x3051)
EGL_TRANSPARENT_RGB = EGLint(0x3052)
EGL_RGB_BUFFER = EGLint(0x308E)
EGL_LUMINANCE_BUFFER = EGLint(0x308)

EGL_NO_TEXTURE = EGLint(0x305C)
EGL_TEXTURE_RGB = EGLint(0x305D)
EGL_TEXTURE_RGBA = EGLint(0x305E)
EGL_TEXTURE_2D = EGLint(0x305F)

EGL_PBUFFER_BIT = EGLint(0x0001)
EGL_PIXMAP_BIT = EGLint(0x0002)
EGL_WINDOW_BIT = EGLint(0x0004)
EGL_VG_COLORSPACE_LINEAR_BIT = EGLint(0x0020)
EGL_VG_ALPHA_FORMAT_PRE_BIT = EGLint(0x0040)
EGL_MULTISAMPLE_RESOLVE_BOX_BIT = EGLint(0x0200)
EGL_SWAP_BEHAVIOR_PRESERVED_BIT = EGLint(0x040)

EGL_OPENGL_ES_BIT = EGLint(0x0001)
EGL_OPENVG_BIT = EGLint(0x0002)
EGL_OPENGL_ES2_BIT = EGLint(0x0004)
EGL_OPENGL_BIT = EGLint(0x000)

EGL_VENDOR = EGLint(0x3053)
EGL_VERSION = EGLint(0x3054)
EGL_EXTENSIONS = EGLint(0x3055)
EGL_CLIENT_APIS = EGLint(0x308D)

EGL_HEIGHT = EGLint(0x3056)
EGL_WIDTH = EGLint(0x3057)
EGL_LARGEST_PBUFFER = EGLint(0x3058)
EGL_TEXTURE_FORMAT = EGLint(0x3080)
EGL_TEXTURE_TARGET = EGLint(0x3081)
EGL_MIPMAP_TEXTURE = EGLint(0x3082)
EGL_MIPMAP_LEVEL = EGLint(0x3083)
EGL_RENDER_BUFFER = EGLint(0x3086)
EGL_VG_COLORSPACE = EGLint(0x3087)
EGL_VG_ALPHA_FORMAT = EGLint(0x3088)
EGL_HORIZONTAL_RESOLUTION = EGLint(0x3090)
EGL_VERTICAL_RESOLUTION = EGLint(0x3091)
EGL_PIXEL_ASPECT_RATIO = EGLint(0x3092)
EGL_SWAP_BEHAVIOR = EGLint(0x3093)
EGL_MULTISAMPLE_RESOLVE = EGLint(0x3099)

EGL_BACK_BUFFER = EGLint(0x3084)
EGL_SINGLE_BUFFER = EGLint(0x3085)

EGL_CONTEXT_CLIENT_VERSION = EGLint(0x3098)

EGL_OPENGL_ES_API = EGLint(0x30A0)
EGL_OPENVG_API = EGLint(0x30A1)
EGL_OPENGL_API = EGLint(0x30A2)
