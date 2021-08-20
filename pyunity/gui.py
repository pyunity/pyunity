__all__ = ["Canvas", "RectAnchors", "RectOffset", "RectTransform", "Image2D"]

from .values import Vector2
from .core import Component, ShowInInspector
from .files import Texture2D

class Canvas(Component):
    def Render(self):
        for descendant in self.transform.GetDescendants():
            renderer = descendant.GetComponent(Image2D)
            if renderer is not None:
                renderer.Render()

class RectAnchors:
    def __init__(self):
        self.min = Vector2(0.5, 0.5)
        self.max = Vector2(0.5, 0.5)

class RectOffset:
    def __init__(self):
        self.min = Vector2.zero()
        self.max = Vector2.zero()

class RectTransform(Component):
    anchors = ShowInInspector(RectAnchors)
    offset = ShowInInspector(RectOffset)
    pivot = ShowInInspector(Vector2)
    scale = ShowInInspector(Vector2)
    rotation = ShowInInspector(float, 0)
    def __init__(self, transform):
        super(RectTransform, self).__init__(transform)
        self.anchors = RectAnchors()
        self.offset = RectOffset()
        self.pivot = Vector2(0.5, 0.5)
        self.scale = Vector2.one()

    def getPosition(self):
        pass

class Image2D(Component):
    texture = ShowInInspector(Texture2D)
    def __init__(self, transform):
        super(Image2D, self).__init__(transform)
        self.rectTransform = self.GetComponent(RectTransform)
