from pyunity import config, SceneManager, AudioClip, AudioSource
import os

def main():
    scene = SceneManager.AddScene("Scene")
    if config.audio:
        path = os.path.abspath(os.path.dirname(__file__))
        clip = AudioClip(os.path.join(path, "explode.ogg"))
        source = scene.mainCamera.AddComponent(AudioSource)
        source.SetClip(clip)
        source.playOnStart = True

    SceneManager.LoadScene(scene)

if __name__ == "__main__":
    main()
