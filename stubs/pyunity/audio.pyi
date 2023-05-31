## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""
Classes to manage the playback of audio.
It uses the sdl2.sdlmixer library.
A variable in the ``config`` module called
``audio`` will be set to ``False`` if the
mixer module cannot be initialized.

"""

__all__ = ["AudioSource", "AudioClip", "AudioListener"]

from .core import Component, Transform

class AudioClip:
    path: str
    def __init__(self, path: str) -> None: ...

class AudioSource(Component):
    playOnStart: bool
    loop: bool
    clip: AudioClip
    def __init__(self, transform: Transform) -> None: ...
    def SetClip(self, clip: AudioClip) -> None: ...
    def Play(self) -> None: ...
    def Stop(self) -> None: ...
    def Pause(self) -> None: ...
    def UnPause(self) -> None: ...
    @property
    def Playing(self) -> bool: ...

class AudioListener(Component):
    opened: int
    def __init__(self, transform: Transform) -> None: ...
    def Init(self) -> None: ...
    def DeInit(self) -> None: ...
