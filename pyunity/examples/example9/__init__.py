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
    imgObject = GameObject("Image")
    rectTransform = imgObject.AddComponent(RectTransform)
    rectTransform.offset = RectOffset.Square(100)
    imgObject.AddComponent(Mover2D).rectTransform = rectTransform

    img = imgObject.AddComponent(Image2D)
    img.texture = Texture2D(os.path.join(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))), "example8", "logo.png"))
    scene.Add(imgObject)

    SceneManager.LoadScene(scene)

if __name__ == "__main__":
    main()
