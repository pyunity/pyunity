from pyunity import *
from pyunity import config
import os

def main():
    scene = SceneManager.AddScene("Scene")
    if config.audio:
        path = os.path.realpath(os.path.dirname(__file__))
        clip = AudioClip(os.path.join(path, "explode.ogg"))
        scene.mainCamera.AddComponent(AudioSource).SetClip(clip)
    SceneManager.LoadScene(scene)


if __name__ == "__main__":
    main()
