from .core import Component, SingleComponent

class Canvas(Component):
    def Render(self):
        for descendant in self.transform.GetDescendants():
            print(descendant.gameObject.name)

class RectTransform(SingleComponent):
    pass