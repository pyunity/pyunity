# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import config, SceneManager, AudioClip, AudioSource
from importlib.resources import files

def main():
    scene = SceneManager.AddScene("Scene")
    if config.audio:
        path = files(__package__) / "explode.ogg"
        clip = AudioClip(path)
        source = scene.mainCamera.AddComponent(AudioSource)
        source.SetClip(clip)
        source.playOnStart = True

    SceneManager.LoadScene(scene)

if __name__ == "__main__":
    main()
