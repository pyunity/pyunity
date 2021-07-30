__all__ = ["Material", "Color", "RGB", "HSV"]

import colorsys

class Material:
    """
    Class to hold data on a material.

    Attributes
    ----------
    color : Color
        An albedo tint.
    texture : Texture2D
        A texture to map onto the mesh provided by a MeshRenderer

    """

    def __init__(self, color, texture=None):
        self.color = color
        self.texture = texture

class Color:
    def __truediv__(self, other):
        a, b, c = tuple(self)
        return a / other, b / other, c / other
    
    def __mul__(self, other):
        a, b, c = tuple(self)
        return a * other, b * other, c * other
    
    @staticmethod
    def from_string(self, string):
        if string.startswith("RGB"):
            return RGB(*list(map(int, string.split(", ")[1:])))
        elif string.startswith("HSV"):
            return HSV(*list(map(int, string.split(", ")[1:])))

class RGB(Color):
    """
    A class to represent an RGB color.

    Parameters
    ----------
    r : int
        Red value (0-255)
    g : int
        Green value (0-255)
    b : int
        Blue value (0-255)

    """

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    
    def __list__(self):
        return [self.r, self.g, self.b]

    def __iter__(self):
        yield self.r
        yield self.g
        yield self.b
    
    def __repr__(self):
        return "RGB(%d, %d, %d)" % tuple(self)
    __str__ = __repr__

    def to_hsv(self):
        return HSV.from_rgb(self.r, self.g, self.b)
    
    @staticmethod
    def from_hsv(h, s, v):
        r, g, b = colorsys.hsv_to_rgb(h / 360, s / 100, v / 100)
        return RGB(int(r * 255), int(g * 255), int(b * 255))
    
    def to_string(self):
        return str(self)

class HSV(Color):
    """
    A class to represent a HSV color.

    Parameters
    ----------
    h : int
        Hue (0-360)
    s : int
        Saturation (0-100)
    v : int
        Value (0-100)

    """
    def __init__(self, h, s, v):
        self.h = h
        self.s = s
        self.v = v
    
    def __list__(self):
        return [self.h, self.s, self.v]
    
    def __iter__(self):
        yield self.h
        yield self.s
        yield self.v
    
    def __repr__(self):
        return "HSV(%d, %d, %d)" % tuple(self)
    __str__ = __repr__
    
    def to_rgb(self):
        return RGB.from_hsv(self.h, self.s, self.v)
    
    @staticmethod
    def from_rgb(r, g, b):
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        return HSV(int(h * 360), int(s * 100), int(v * 100))
    
    def to_string(self):
        return str(self.to_rgb())
