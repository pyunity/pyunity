## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

__all__ = [
    "EGLBoolean", "EGLConfig", "EGLContext", "EGLDisplay", "EGLList",
    "EGLSurface", "EGLint", "eglBindAPI", "eglChooseConfig",
    "eglCreateContext", "eglCreatePbufferSurface", "eglDestroyContext",
    "eglDestroySurface", "eglGetDisplay", "eglGetError", "eglInitialize",
    "eglMakeCurrent", "eglTerminate", "EGL"
]

from pyunity import Logger, WindowProviderException
from functools import wraps
import os
import ctypes
import ctypes.util

directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib")
if os.path.isdir(directory):
    os.add_dll_directory(directory)

search = True
if "PYUNITY_EGL_PATH" in os.environ:
    try:
        _egl = ctypes.CDLL(os.environ["PYUNITY_EGL_PATH"])
        search = False
    except OSError:
        Logger.LogLine(Logger.DEBUG,
                       "PYUNITY_EGL_PATH environment variable specified but "
                       "path not found")
if search:
    _names = ["libegl", "libEGL"]
    for name in _names:
        _libname = ctypes.util.find_library(name)
        if _libname is None:
            if os.name == "nt":
                _libname = name + ".dll"
            else:
                _libname = name + ".so"

        try:
            _egl = ctypes.CDLL(_libname)
        except OSError:
            _egl = None
    if _egl is None:
        raise WindowProviderException("Cannot find libegl library")

def wrap(func):
    orig = getattr(_egl, func.__name__)

    @wraps(func)
    def inner(*args):
        res = orig(*args)
        if orig.restype is EGLBoolean and res.value == 0:
            raise WindowProviderException(f"{func.__name__} failed")
    return inner

def returnPointer(wrapArgs, includeOutput=False):
    def decorator(func):
        @wraps(func)
        def inner(*args):
            orig = getattr(_egl, func.__name__)
            newArgs = list(args)
            for argnum in wrapArgs:
                item = orig.argtypes[argnum]._type_()
                newArgs.insert(argnum, item)
            res = orig(*newArgs)
            if orig.restype is EGLBoolean and res.value == 0:
                raise WindowProviderException(f"{func.__name__} failed")
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

def returnArray(wrapArgs, lenArgs, inArgs, includeOutput=False):
    def decorator(func):
        @wraps(func)
        def inner(*args):
            orig = getattr(_egl, func.__name__)
            newArgs = list(args)
            for argnum in sorted(wrapArgs + lenArgs):
                if argnum in wrapArgs:
                    i = wrapArgs.index(argnum)
                    item = (orig.argtypes[argnum]._type_ * args[inArgs[i]])()
                else:
                    item = EGLint()
                newArgs.insert(argnum, item)
            res = orig(*newArgs)
            if orig.restype is EGLBoolean and res.value == 0:
                raise WindowProviderException(f"{func.__name__} failed")
            out = []
            if includeOutput:
                out.append(res)
            lengths = []
            for argnum in sorted(wrapArgs + lenArgs):
                if argnum in wrapArgs:
                    # arr = ctypes.cast(newArgs[argnum], orig.argtypes[argnum])
                    out.append(newArgs[argnum])
                else:
                    lengths.append(newArgs[argnum].value)
            # for i in range(len(wrapArgs)):
            #     arr = out[i]
            #     if ctypes.sizeof(arr) // ctypes.sizeof(arr[0]) != lengths[i]:
            #         raise WindowProviderException("Sizeof array does not match return")
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

_egl.eglGetError.restype = EGLint
@wrap
def eglGetError(): pass

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
@returnPointer([2, 4])
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
class EGL:
    DEFAULT_DISPLAY = EGLint(0)
    NO_CONTEXT = EGLContext(0)
    NO_DISPLAY = EGLDisplay(0)
    NO_SURFACE = EGLSurface(0)

    DONT_CARE = EGLint(-1)

    BUFFER_SIZE = EGLint(0x3020)
    ALPHA_SIZE = EGLint(0x3021)
    BLUE_SIZE = EGLint(0x3022)
    GREEN_SIZE = EGLint(0x3023)
    RED_SIZE = EGLint(0x3024)
    DEPTH_SIZE = EGLint(0x3025)
    STENCIL_SIZE = EGLint(0x3026)
    CONFIG_CAVEAT = EGLint(0x3027)
    CONFIG_ID = EGLint(0x3028)
    LEVEL = EGLint(0x3029)
    MAX_PBUFFER_HEIGHT = EGLint(0x302A)
    MAX_PBUFFER_PIXELS = EGLint(0x302B)
    MAX_PBUFFER_WIDTH = EGLint(0x302C)
    NATIVE_RENDERABLE = EGLint(0x302D)
    NATIVE_VISUAL_ID = EGLint(0x302E)
    NATIVE_VISUAL_TYPE = EGLint(0x302F)
    SAMPLES = EGLint(0x3031)
    SAMPLE_BUFFERS = EGLint(0x3032)
    SURFACE_TYPE = EGLint(0x3033)
    TRANSPARENT_TYPE = EGLint(0x3034)
    TRANSPARENT_BLUE_VALUE = EGLint(0x3035)
    TRANSPARENT_GREEN_VALUE = EGLint(0x3036)
    TRANSPARENT_RED_VALUE = EGLint(0x3037)
    NONE = EGLint(0x3038)
    BIND_TO_TEXTURE_RGB = EGLint(0x3039)
    BIND_TO_TEXTURE_RGBA = EGLint(0x303A)
    MIN_SWAP_INTERVAL = EGLint(0x303B)
    MAX_SWAP_INTERVAL = EGLint(0x303C)
    LUMINANCE_SIZE = EGLint(0x303D)
    ALPHA_MASK_SIZE = EGLint(0x303E)
    COLOR_BUFFER_TYPE = EGLint(0x303F)
    RENDERABLE_TYPE = EGLint(0x3040)
    MATCH_NATIVE_PIXMAP = EGLint(0x3041)
    CONFORMANT = EGLint(0x3042)

    SLOW_CONFIG = EGLint(0x3050)
    NON_CONFORMANT_CONFIG = EGLint(0x3051)
    TRANSPARENT_RGB = EGLint(0x3052)
    RGB_BUFFER = EGLint(0x308E)
    LUMINANCE_BUFFER = EGLint(0x308)

    NO_TEXTURE = EGLint(0x305C)
    TEXTURE_RGB = EGLint(0x305D)
    TEXTURE_RGBA = EGLint(0x305E)
    TEXTURE_2D = EGLint(0x305F)

    PBUFFER_BIT = EGLint(0x0001)
    PIXMAP_BIT = EGLint(0x0002)
    WINDOW_BIT = EGLint(0x0004)
    VG_COLORSPACE_LINEAR_BIT = EGLint(0x0020)
    VG_ALPHA_FORMAT_PRE_BIT = EGLint(0x0040)
    MULTISAMPLE_RESOLVE_BOX_BIT = EGLint(0x0200)
    SWAP_BEHAVIOR_PRESERVED_BIT = EGLint(0x040)

    OPENGL_ES_BIT = EGLint(0x0001)
    OPENVG_BIT = EGLint(0x0002)
    OPENGL_ES2_BIT = EGLint(0x0004)
    OPENGL_BIT = EGLint(0x000)

    VENDOR = EGLint(0x3053)
    VERSION = EGLint(0x3054)
    EXTENSIONS = EGLint(0x3055)
    CLIENT_APIS = EGLint(0x308D)

    HEIGHT = EGLint(0x3056)
    WIDTH = EGLint(0x3057)
    LARGEST_PBUFFER = EGLint(0x3058)
    TEXTURE_FORMAT = EGLint(0x3080)
    TEXTURE_TARGET = EGLint(0x3081)
    MIPMAP_TEXTURE = EGLint(0x3082)
    MIPMAP_LEVEL = EGLint(0x3083)
    RENDER_BUFFER = EGLint(0x3086)
    VG_COLORSPACE = EGLint(0x3087)
    VG_ALPHA_FORMAT = EGLint(0x3088)
    HORIZONTAL_RESOLUTION = EGLint(0x3090)
    VERTICAL_RESOLUTION = EGLint(0x3091)
    PIXEL_ASPECT_RATIO = EGLint(0x3092)
    SWAP_BEHAVIOR = EGLint(0x3093)
    MULTISAMPLE_RESOLVE = EGLint(0x3099)

    BACK_BUFFER = EGLint(0x3084)
    SINGLE_BUFFER = EGLint(0x3085)

    CONTEXT_CLIENT_VERSION = EGLint(0x3098)

    OPENGL_ES_API = EGLint(0x30A0)
    OPENVG_API = EGLint(0x30A1)
    OPENGL_API = EGLint(0x30A2)
