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
    img.texture = Texture2D(os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), "example8", "logo.png"))
    scene.Add(imgObject)

    rect, button = Gui.MakeButton("Button", scene)
    rect.transform.ReparentTo(canvas.transform)
    rect.offset = RectOffset(Vector2(100, 70), Vector2(250, 100))
    button.callback = lambda: print("Clicked")

    t = GameObject("text", canvas)
    text = t.AddComponent(Text)
    text.text = "Hello"
    text.color = RGB(0, 0, 0)
    text.font = FontLoader.LoadFont("Consolas", 24)

    rect = t.AddComponent(RectTransform)
    rect.offset.min = Vector2(40, 25)
    rect.offset.max = Vector2(240, 50)
    scene.Add(t)

    SceneManager.LoadScene(scene)

if __name__ == "__main__":
    main()
