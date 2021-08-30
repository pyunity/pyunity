__all__ = ["Canvas", "RectData", "RectAnchors", "RectOffset", "RectTransform", "Image2D"]

from .values import Vector2
from .core import Component, ShowInInspector
from .files import Texture2D

class Canvas(Component):
    def Render(self):
        for descendant in self.transform.GetDescendants():
            renderer = descendant.GetComponent(Image2D)
            if renderer is not None:
                renderer.Render()

class RectData:
    def __init__(self, min_or_both=None, max=None):
        if min_or_both is None:
            self.min = Vector2.zero()
            self.max = Vector2.zero()
        elif max is None:
            self.min = min_or_both.copy()
            self.min = min_or_both.copy()
        else:
            self.min = min_or_both.copy()
            self.max = max.copy()
    
    def __repr__(self):
        return "<{} min={} max={}>".format(self.__class__.__name__, self.min, self.max)

class RectAnchors(RectData):
    def SetPoint(self, p):
        self.min = p.copy()
        self.max = p.copy()
    
    def RelativeTo(self, other):
        if other.max == other.min:
            parentSize = Vector2.one()
        else:
            parentSize = other.max - other.min
        absAnchorMin = other.min + (self.anchors.min * parentSize)
        absAnchorMax = other.max - (self.anchors.max * parentSize)
        return RectData(absAnchorMin, absAnchorMax)

class RectOffset(RectData):
    pass

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

        if self.transform.parent is None:
            self.parent = None
        else:
            self.parent = self.transform.parent.GetComponent(RectTransform)

    def GetRect(self):
        if self.parent is None:
            return self.anchors
        else:
            return self.anchors.RelativeTo(self.parent.anchors)

class Image2D(Component):
    texture = ShowInInspector(Texture2D)
    def __init__(self, transform):
        super(Image2D, self).__init__(transform)
        self.rectTransform = self.GetComponent(RectTransform)
