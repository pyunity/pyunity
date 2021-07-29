__all__ = ["Material", "Color"]

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
    """
    A class to represent a color.

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

    def __truediv__(self, other):
        return self.r / other, self.g / other, self.b / other

    def __repr__(self):
        return "Color(" + self.to_string() + ")"
    __str__ = __repr__

    def to_string(self):
        return "{}, {}, {}".format(self.r, self.g, self.b)

    @staticmethod
    def from_string(string):
        return Color(*list(map(int, string.split(", "))))
