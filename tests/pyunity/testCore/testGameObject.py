## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import (
    GameObject, Transform, Component, ComponentException, Collider)
from . import TestCase

class TestGameObject(TestCase):
    def testName(self):
        gameObject = GameObject()
        assert gameObject.name == "GameObject"

    def testBare(self):
        gameObject = GameObject.BareObject("Bare")
        assert gameObject.name == "Bare"
        assert len(gameObject.components) == 0
        assert gameObject.transform is None
        assert gameObject.scene is None

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
            gameObject.AddComponent(1)
        assert exc.value == "Cannot add 1 to the GameObject; it is not a component"

        with self.assertRaises(ComponentException) as exc:
            gameObject.AddComponent(int)
        assert exc.value == "Cannot add int to the GameObject; it is not a component"

        with self.assertRaises(ComponentException) as exc:
            gameObject.AddComponent(Transform)
        assert exc.value == "Cannot add Transform to the GameObject; it already has one"

        with self.assertRaises(ComponentException) as exc:
            gameObject.RemoveComponent(Collider)
        assert exc.value == "Cannot remove Collider from the GameObject; it doesn't have one"

        with self.assertRaises(ComponentException) as exc:
            gameObject.RemoveComponent(Transform)
        assert exc.value == "Cannot remove a Transform from a GameObject"

        with self.assertRaises(ComponentException) as exc:
            gameObject.RemoveComponents(Transform)
        assert exc.value == "Cannot remove a Transform from a GameObject"

        numComponents = len(gameObject.components)
        gameObject.RemoveComponents(Collider)
        assert len(gameObject.components) == numComponents
