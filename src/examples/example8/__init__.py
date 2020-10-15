from pyunity import *
import os

def main():
    scene = SceneManager.AddScene("Scene")
    path = os.path.realpath(os.path.dirname(__file__))
    clip = AudioClip(os.path.join(path, "explode.ogg"))
    scene.mainCamera.AddComponent(AudioSource).SetClip(clip)
    scene.Run()

if __name__ == "__main__":
    main()