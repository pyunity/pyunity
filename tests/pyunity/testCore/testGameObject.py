from pyunity import GameObject, Transform, Component, ComponentException
from . import TestCase

class TestGameObject(TestCase):
    def testName(self):
        gameObject = GameObject()
        assert gameObject.name == "GameObject"

    def testTag(self):
        gameObject = GameObject()
        assert gameObject.tag.tag == 0
        assert gameObject.tag.tagName == "Default"

    def testTransform(self):
        gameObject = GameObject()
        gameObject2 = GameObject("GameObject2", gameObject)
        assert isinstance(gameObject.transform, Transform)
        assert isinstance(gameObject2.transform, Transform)
        assert gameObject2.transform.parent is gameObject.transform
        assert gameObject.transform.parent is None
        assert gameObject2.transform.parent.gameObject.name == "GameObject"
        assert len(gameObject.transform.children) == 1
        assert len(gameObject2.transform.children) == 0

    def testComponent(self):
        gameObject = GameObject()
        assert isinstance(gameObject.transform, Transform)
        assert len(gameObject.components) == 1
        component = gameObject.AddComponent(Component)
        assert isinstance(component, Component)
        assert len(gameObject.components) == 2
        assert gameObject.GetComponent(Transform) is gameObject.transform
        with self.assertRaises(ComponentException) as exc:
            gameObject.AddComponent(Transform)
        assert exc.value == "Cannot add Transform to the GameObject; it already has one"