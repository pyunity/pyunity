from pyunity import *
import os

class Mover2D(Behaviour):
    rectTransform = ShowInInspector(RectTransform)
    speed = ShowInInspector(float, 200)
    def Start(self):
        self.rectTransform.offset.Move(Screen.size / 2)

    def Update(self, dt):
        movement = Vector2(Input.GetAxis("Horizontal"), -
                           Input.GetAxis("Vertical"))
        self.rectTransform.offset.Move(movement * dt * self.speed)
        self.rectTransform.rotation += 180 * dt

class FPSTracker(Behaviour):
    text = ShowInInspector(Text)
    def Start(self):
        self.a = 0

    def Update(self, dt):
        self.a += dt
        if self.a > 0.05:
            self.text.text = str(1 / dt)
            self.a = 0

def main():
    scene = SceneManager.AddScene("Scene")
    canvas = GameObject("Canvas")
    canvas.AddComponent(Canvas)
    scene.Add(canvas)

    imgObject = GameObject("Image", canvas)
    rectTransform = imgObject.AddComponent(RectTransform)
    rectTransform.offset = RectOffset.Square(100)
    imgObject.AddComponent(Mover2D).rectTransform = rectTransform

    img = imgObject.AddComponent(Image2D)
    img.depth = -0.1
    img.texture = Texture2D(os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), "example8", "logo.png"))
    scene.Add(imgObject)

    rect, button, text = Gui.MakeButton(
        "Button", scene, "Click me", FontLoader.LoadFont("Consolas", 20))
    rect.transform.ReparentTo(canvas.transform)
    rect.offset = RectOffset(Vector2(40, 25), Vector2(190, 50))
    button.callback = lambda: Logger.Log("Clicked")

    t = GameObject("Text", canvas)
    rect = t.AddComponent(RectTransform)
    rect.anchors.SetPoint(Vector2(1, 0))
    rect.offset.min = Vector2(-150, 25)
    text = t.AddComponent(Text)
    text.text = "60"
    text.color = RGB(0, 0, 0)
    t.AddComponent(FPSTracker).text = text
    scene.Add(t)

    SceneManager.LoadScene(scene)

if __name__ == "__main__":
    main()
