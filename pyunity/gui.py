from .values import Vector2
from .core import Component, ShowInInspector

class Canvas(Component):
    def Render(self):
        for descendant in self.transform.GetDescendants():
            print(descendant.gameObject.name)

class RectAnchors:
    def __init__(self):
        self.min = Vector2(0.5, 0.5)
        self.max = Vector2(0.5, 0.5)

class RectTransform:
    anchoredPos = ShowInInspector(Vector2, None, "position")
    anchors = ShowInInspector(RectAnchors, None)
    pivot = ShowInInspector(Vector2, None)
    def __init__(self, transform=None):
        super(RectTransform, self).__init__(transform)
        self.anchoredPos = Vector2.zero()
        self.anchors = RectAnchors()
        self.pivot = Vector2(0.5, 0.5)
