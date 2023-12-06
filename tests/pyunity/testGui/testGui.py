## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import (RGB, Button, CheckBox, FontLoader, Gui, Image2D,
                     RectTransform, SceneManager, Text)
from . import SceneTestCase

class TestGui(SceneTestCase):
    def testMakeButton(self):
        scene = SceneManager.AddScene("Scene")
        rectTransform, button, text = Gui.MakeButton(
            "Button", scene, "Button text",
            FontLoader.LoadFont("Consolas", 20), RGB(255, 0, 0))
        assert len(scene.gameObjects) == 5

        buttonObj = scene.gameObjects[2]
        assert buttonObj.name == "Button"
        assert len(buttonObj.components) == 3
        assert buttonObj is button.gameObject
        assert buttonObj.GetComponent(RectTransform) is rectTransform
        assert buttonObj.GetComponent(Button) is button

        textObj = scene.gameObjects[3]
        assert len(buttonObj.components) == 3
        assert textObj is text.gameObject
        assert textObj.GetComponent(RectTransform) is not None
        assert textObj.GetComponent(Text) is text

        textureObj = scene.gameObjects[4]
        assert len(buttonObj.components) == 3
        assert textureObj.GetComponent(Image2D) is not None
        assert textureObj.GetComponent(RectTransform) is not None

    def testMakeCheckBox(self):
        from pyunity import gui
        scene = SceneManager.AddScene("Scene")
        rectTransform, checkbox = Gui.MakeCheckBox("Checkbox", scene)
        img = checkbox.GetComponent(Image2D)
        assert len(scene.gameObjects) == 3

        checkboxObj = scene.gameObjects[2]
        assert checkboxObj.name == "Checkbox"
        assert len(checkboxObj.components) == 4
        assert checkboxObj is checkbox.gameObject
        assert checkboxObj.GetComponent(RectTransform) is rectTransform
        assert checkboxObj.GetComponent(CheckBox) is checkbox
        assert img is not None
        assert img.texture is gui.checkboxDefaults[0]
