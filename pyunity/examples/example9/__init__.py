# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import Behaviour, ShowInInspector, RectTransform, Screen, Vector2, Input, CheckBox, Text, SceneManager, GameObject, Canvas, Texture2D, Gui, RectOffset, Logger, Image2D, FontLoader, RGB, Camera, Vector3, RenderTarget, MeshRenderer, Mesh, Material, Event, WaitForUpdate
from pyunity.resources import getPath

class Mover2D(Behaviour):
    rectTransform = ShowInInspector(RectTransform)
    speed = ShowInInspector(float, 300)
    async def Start(self):
        self.rectTransform.offset.Move(Screen.size / 2)

    async def Update(self, dt):
        movement = Vector2(Input.GetAxis("Horizontal"), -
                           Input.GetAxis("Vertical"))
        self.rectTransform.offset.Move(movement * dt * self.speed)
        self.rectTransform.rotation += 270 * dt

class FPSTracker(Behaviour):
    text = ShowInInspector(Text)
    async def Start(self):
        frames = []
        time = 0
        while True:
            dt = await WaitForUpdate()
            time += dt
            frames.append(dt)
            if len(frames) > 200:
                frames.pop(0)
            if time > 0.1:
                self.text.text = str(1 / (sum(frames) / len(frames)))
                time = 0

class CheckboxTracker(Behaviour):
    check = ShowInInspector(CheckBox)
    text = ShowInInspector(Text)
    def Update(self, dt):
        self.text.text = "On" if self.check.checked else "Off"

class Rotator(Behaviour):
    def Update(self, dt):
        self.transform.eulerAngles += Vector3(0, 90, 135) * dt

class CallbackReceiver(Behaviour):
    def Callback(self):
        Logger.Log("Clicked")

def main():
    scene = SceneManager.AddScene("Scene")
    canvas = GameObject("Canvas")
    scene.mainCamera.canvas = canvas.AddComponent(Canvas)
    scene.Add(canvas)

    imgObject = GameObject("Image", canvas)
    rectTransform = imgObject.AddComponent(RectTransform)
    rectTransform.offset = RectOffset.Rectangle(100)
    imgObject.AddComponent(Mover2D).rectTransform = rectTransform

    img = imgObject.AddComponent(Image2D)
    img.depth = -0.1
    img.texture = Texture2D(getPath("examples/example8/logo.png"))
    scene.Add(imgObject)

    rect, button, text = Gui.MakeButton(
        "Button", scene, "-> Click me", FontLoader.LoadFont("Consolas", 20))
    rect.transform.ReparentTo(canvas.transform)
    rect.offset = RectOffset(Vector2(40, 25), Vector2(190, 50))
    receiver = button.AddComponent(CallbackReceiver)
    button.callback = Event(receiver.Callback)

    rect, checkbox = Gui.MakeCheckBox("Checkbox", scene)
    rect.transform.ReparentTo(canvas.transform)
    rect.offset = RectOffset(Vector2(300, 50), Vector2(325, 75))

    label = GameObject("Label")
    text = label.AddComponent(Text)
    text.text = "Off"
    text.color = RGB(0, 0, 0)
    label.AddComponent(RectTransform).offset = RectOffset(
        Vector2(330, 50), Vector2(425, 75))
    label.transform.ReparentTo(canvas.transform)
    scene.Add(label)
    tracker = rect.AddComponent(CheckboxTracker)
    tracker.text = text
    tracker.check = checkbox

    t = GameObject("Text", canvas)
    rect = t.AddComponent(RectTransform)
    rect.anchors.SetPoint(Vector2(1, 0))
    rect.offset.min = Vector2(-150, 25)
    text = t.AddComponent(Text)
    text.text = "60"
    text.color = RGB(0, 0, 0)
    t.AddComponent(FPSTracker).text = text
    scene.Add(t)

    cam = GameObject("Camera")
    cam.transform.position = Vector3(-5, 2, -5)
    cam.transform.LookAtPoint(Vector3.zero())
    camera = cam.AddComponent(Camera)
    camera.shadows = False
    scene.Add(cam)

    target = GameObject("Target", canvas)
    rect = target.AddComponent(RectTransform)
    rect.anchors.min = Vector2(0.6, 0.6)
    rect.anchors.max = Vector2(1, 1)
    target.AddComponent(RenderTarget).source = camera
    scene.Add(target)

    label = GameObject("Label", canvas)
    rect = label.AddComponent(RectTransform)
    rect.anchors.min = Vector2(0.6, 0.55)
    rect.anchors.max = Vector2(1, 0.6)
    text = label.AddComponent(Text)
    text.text = "RenderTarget"
    text.color = RGB(0, 0, 0)
    scene.Add(label)

    cube = GameObject("Cube")
    renderer = cube.AddComponent(MeshRenderer)
    renderer.mesh = Mesh.cube(2)
    renderer.mat = Material(RGB(255, 0, 0))
    cube.AddComponent(Rotator)
    scene.Add(cube)

    SceneManager.LoadScene(scene)

if __name__ == "__main__":
    main()
