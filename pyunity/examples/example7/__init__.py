# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import config, SceneManager, AudioClip, AudioSource
from importlib_resources import files, as_file
from contextlib import ExitStack

def main():
    stack = ExitStack()

    scene = SceneManager.AddScene("Scene")
    if config.audio:
        ref = files(__package__) / "explode.ogg"
        path = stack.enter_context(as_file(ref))
        clip = AudioClip(path)
        source = scene.mainCamera.AddComponent(AudioSource)
        source.SetClip(clip)
        source.playOnStart = True

    SceneManager.LoadScene(scene)
    stack.close()

if __name__ == "__main__":
    main()
