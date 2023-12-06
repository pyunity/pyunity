## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

__all__ = ["Acos", "Asin", "Atan", "Atan2", "Ceil", "Clamp", "Clamp01", "Cos",
           "DEG_TO_RAD", "DeltaAngle", "EPSILON", "Exp", "Floor", "GLM_SUPPORT",
           "INFINITY", "InverseLerp", "Lerp", "LerpUnclamped", "Log",
           "NEG_INFINITY", "PI", "RAD_TO_DEG", "Sign", "Sin", "SmoothDamper",
           "SmoothStep", "Sqrt", "Tan"]

from .. import Logger
import os
import sys
import math

GLM_SUPPORT = True
try:
    import glm
    if glm is math:
        # Wrapper scripts may replace glm with math in sys.modules
        sys.modules.pop("math", "")
        import glm
except ImportError:
    GLM_SUPPORT = False

if GLM_SUPPORT:
    Logger.LogLine(Logger.INFO, "GLM support enabled")
else:
    Logger.LogLine(Logger.INFO,
                   "GLM support disabled; falling back to builtin math")

PI = math.pi
DEG_TO_RAD = PI / 180
RAD_TO_DEG = 180 / PI
INFINITY = math.inf
NEG_INFINITY = -math.inf
EPSILON = sys.float_info.epsilon

def _wraps(orig, glmfunc=None):
    if glmfunc is None:
        glmfunc = orig

    def decorator(func):
        if "PYUNITY_SPHINX_CHECK" in os.environ:
            return func
        if isinstance(orig, str):
            if GLM_SUPPORT:
                return getattr(glm, glmfunc)
            else:
                return getattr(math, orig)
        return orig
    return decorator

@_wraps("acos")
def Acos(num):
    """
    Returns the angle whose cosine is
    ``num``. Return value is in radians.

    Parameters
    ----------
    num : float
        Input number

    """
    pass

@_wraps("asin")
def Asin(num):
    """
    Returns the angle whose sine is
    ``num``. Return value is in radians.

    Parameters
    ----------
    num : float
        Input number

    """
    pass

@_wraps("atan")
def Atan(num):
    """
    Returns the angle whose tangent is
    ``num``. Return value is in radians.

    Parameters
    ----------
    num : float
        Input number

    """
    pass

@_wraps("atan2", "atan")
def Atan2(x, y):
    """
    Returns the two-argument arctangent
    of ``x/y``.

    Parameters
    ----------
    x : float
        Input x
    y : float
        Input y

    """
    pass

@_wraps("ceil")
def Ceil(num):
    """
    Returns the smallest integer greater than or equal to ``num``.

    Parameters
    ----------
    num : float
        Input number

    """
    pass

def Clamp(num, a, b):
    """
    Returns ``a`` if ``num`` is smaller than
    or equal to ``a``, ``b`` if ``num`` is
    greater than or equal to ``b``, or ``num``
    if it is between ``a`` and ``b``.

    Parameters
    ----------
    num : float
        Input number
    a : float
        Lower bound
    b : float
        Upper bound

    """
    return min(max(num, a), b)

def Clamp01(num):
    """
    Returns ``num`` clamped between 0 and 1.

    Parameters
    ----------
    num : float
        Input number

    """
    if num < 0:
        return 0
    if num > 1:
        return 1
    return num

@_wraps("cos")
def Cos(num):
    """
    Returns the cosine of ``num``. Must be
    passed in radians.

    Parameters
    ----------
    num : float
        Input number

    """
    pass

def DeltaAngle(a, b):
    """
    Calculates the shortest difference between
    two given angles given in degrees.

    Parameters
    ----------
    a : float
        Input a
    b : float
        Input b

    """

    return abs(a - b) % 360

@_wraps("exp")
def Exp(num):
    """
    Returns e raised to the power of ``num``.

    Parameters
    ----------
    num : float
        Exponent

    """
    pass

@_wraps("floor")
def Floor(num):
    """
    Returns the largest integer smaller than or equal to ``num``.

    Parameters
    ----------
    num : float
        Input number

    """
    pass

def InverseLerp(num, a, b):
    """
    Determines where ``num`` lies between two points
    ``a`` and ``b``.

    Parameters
    ----------
    num : float
        Number to check
    a : float
        Lower bound
    b : float
        Upper bound

    """
    if a == b:
        return 0
    prop = (num - a) / (b - a)
    return Clamp01(prop)

def Lerp(num, a, b):
    """
    Linearly interpolates between ``a`` and ``b``
    by ``num``.

    Parameters
    ----------
    num : float
        Amount to interpolate by
    a : float
        Lower bound
    b : float
        Upper bound

    """
    return a + (b - a) * Clamp01(num)

def LerpUnclamped(num, a, b):
    """
    Linearly interpolates between ``a`` and ``b``
    by ``num`` with no limit for ``num``.

    Parameters
    ----------
    num : float
        Amount to interpolate by
    a : float
        Lower bound
    b : float
        Upper bound

    """
    return a + (b - a) * num

@_wraps("log")
def Log(num):
    """
    Returns the base 10 logarithm of ``num``.

    Parameters
    ----------
    num : float
        Input number

    """
    pass

def Sign(num):
    """
    Returns the sign of ``num`` (either -1 or 1,
    or 0 if ``num`` is 0).

    Parameters
    ----------
    num : float
        Input number

    """
    if num == 0:
        return 0
    if num > 0:
        return 1
    return -1

@_wraps("sin")
def Sin(num):
    """
    Returns the sine of ``num``. Must be
    passed in radians.

    Parameters
    ----------
    num : float
        Input number

    """
    pass

def SmoothStep(num):
    """
    Used in conjunction with :func:`Lerp` to
    smoothly interpolate between two numbers.
    This function takes a number between 0 and 1
    and returns a number between 0 and 1,
    which has a steeper graph around 0.5
    and a smoother graph near 0 and 1.

    Parameters
    ----------
    num : float
        Input number (between 0 and 1)

    Notes
    -----
    This uses the mathematical equation
    f(x) = 3x^2 - 2x^3.

    """
    # 3x^2 - 2x^3
    return (3 - 2 * num) * num * num

@_wraps("sqrt")
def Sqrt(num):
    """
    Returns the square root of ``num``.

    Parameters
    ----------
    num : float
        Input number

    """
    pass

@_wraps("tan")
def Tan(num):
    """
    Returns the tangent of ``num``. Must be
    passed in radians.

    Parameters
    ----------
    num : float
        Input number

    """
    pass

class SmoothDamper:
    def __init__(self, maxSpeed=INFINITY):
        self.velocity = 0.0
        self.maxSpeed = maxSpeed

    def SmoothDamp(self, current, target, smoothTime, dt):
        smoothTime = max(0.0001, smoothTime)
        omega = 2 / smoothTime

        x = omega * dt
        exp = 1 / (1 + x + 0.48 * x * x + 0.235 * x * x * x)
        change = current - target
        originalTo = target

        maxChange = self.maxSpeed * smoothTime
        change = Clamp(change, -maxChange, maxChange)
        target = current - change

        temp = (self.velocity + omega * change) * dt
        self.velocity = (self.velocity - omega * temp) * exp
        output = target + (change + temp) * exp
        if (originalTo - current > 0.0) == (output > originalTo):
            output = originalTo
            self.velocity = (output - originalTo) / dt
        return output

    def Reset(self):
        self.velocity = 0.0
