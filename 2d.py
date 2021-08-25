from pyunity import *

class Rotator2D(Behaviour):
    rectTransform = ShowInInspector(RectTransform)
    def Update(self, dt):
        self.rectTransform.rotation += 180 * dt

scene = SceneManager.AddScene("Scene")
imgObject = GameObject("Image")
rectTransform = imgObject.AddComponent(RectTransform)
rectTransform.scale = Vector2(100, 100)
img = imgObject.AddComponent(Image2D)
img.texture = Texture2D("pyunity/examples/example9/logo.png")
imgObject.AddComponent(Rotator2D).rectTransform = rectTransform
scene.Add(imgObject)

SceneManager.LoadScene(scene)