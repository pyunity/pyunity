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

from . import Logger, config
from .core import Component, ShowInInspector, SingleComponent
import os
import warnings

channels = 0

if "PYUNITY_TESTING" in os.environ:
    config.audio = False
    Logger.LogLine(Logger.WARN, "Testing PyUnity, audio is disabled")
elif os.environ["PYUNITY_AUDIO"] == "0":
    config.audio = False
    Logger.LogLine(Logger.WARN, "Audio disabled via env var")
elif os.environ["PYUNITY_INTERACTIVE"] == "0":
    config.audio = False
    Logger.LogLine(Logger.WARN, "Non-interactive mode, audio is disabled")
else:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        try:
            from sdl2 import SDL_GetError
            from sdl2 import sdlmixer as mixer
        except ImportError:
            config.audio = False
            Logger.LogLine(Logger.WARN,
                           "Failed to import PySDL2, your system may not support it.")

    if config.audio:
        if mixer.Mix_Init(mixer.MIX_INIT_MP3 | mixer.MIX_INIT_OGG) == 0:
            config.audio = False
            Logger.LogLine(Logger.WARN, "Cannot load sdlmixer, audio is disabled")
        elif mixer.Mix_OpenAudio(22050, mixer.MIX_DEFAULT_FORMAT, 2, 4096) == -1:
            config.audio = False
            Logger.LogLine(Logger.WARN,
                           "SDL2_mixer could not be initialized: " + SDL_GetError().decode())

class AudioClip:
    """
    Class to store information about an audio file.

    Attributes
    ----------
    path : Pathlike
        Path to the file
    music : sdl2.sdlmixer.mixer.Mix_Chunk
        Sound chunk that can be played with
        an SDL2 Mixer Channel.
        Only set when the AudioClip is played
        in an :py:class:`AudioSource`.

    """

    def __init__(self, path):
        self.path = str(path)
        self.music = None

class AudioSource(Component):
    """
    Manages playback on an AudioSource.

    Attributes
    ----------
    clip : AudioClip
        Clip to play. Best way to set the clip
        is to use the :meth:`SetClip` function.
    playOnStart : bool
        Whether it plays on start or not.
    loop : bool
        Whether it loops or not. This is not
        fully supported.

    """

    playOnStart = ShowInInspector(bool, False)
    loop = ShowInInspector(bool, False)
    clip = ShowInInspector(AudioClip, None)

    def __init__(self):
        super(AudioSource, self).__init__()
        global channels
        self.channel = channels
        channels += 1
        if config.audio:
            mixer.Mix_AllocateChannels(channels)

    def SetClip(self, clip):
        """
        Sets a clip for the AudioSource to play.

        Parameters
        ----------
        clip : AudioClip
            AudioClip to play

        """
        self.clip = clip

    def Play(self):
        """
        Plays the AudioClip attached to the AudioSource.

        """
        if self.clip is None:
            Logger.LogLine(Logger.WARN, "AudioSource has no AudioClip")
            return
        if not config.audio:
            return
        if self.clip.music is None:
            self.clip.music = mixer.Mix_LoadWAV(self.clip.path.encode())
        if mixer.Mix_PlayChannel(self.channel, self.clip.music, 0) == -1:
            Logger.LogLine(Logger.WARN, "Unable to play file: %s" %
                           mixer.Mix_GetError().decode())

    def Stop(self):
        """
        Stops playing the AudioClip attached to the AudioSource.

        """
        if not config.audio:
            return
        if self.clip is None:
            Logger.LogLine(Logger.WARN, "AudioSource has no AudioClip")
        mixer.Mix_HaltChannel(self.channel)

    def Pause(self):
        """
        Pauses the AudioClip attached to the AudioSource.

        """
        if not config.audio:
            return
        if self.clip is None:
            Logger.LogLine(Logger.WARN, "AudioSource has no AudioClip")
        mixer.Mix_Pause(self.channel)

    def UnPause(self):
        """
        Unpauses the AudioClip attached to the AudioSource.

        """
        if not config.audio:
            return
        if self.clip is None:
            Logger.LogLine(Logger.WARN, "AudioSource has no AudioClip")
        mixer.Mix_Resume(self.channel)

    @property
    def Playing(self):
        """
        Gets if the AudioSource is playing.

        """
        if not config.audio:
            return False
        if self.clip is None:
            Logger.LogLine(Logger.WARN, "AudioSource has no AudioClip")
        return mixer.Mix_Playing(self.channel)

class AudioListener(SingleComponent):
    """
    Class to receive audio events and to base spatial
    sound from. By default the Main Camera has an
    AudioListener, but you can also remove it and
    add a new one to another GameObject in a Scene.
    There can only be one AudioListener and there must
    be one, otherwise sound is disabled.

    """

    def __init__(self):
        super(AudioListener, self).__init__()
        self.opened = 0

    def Init(self):
        """
        Initializes the AudioListener.

        """
        pass

    def DeInit(self):
        """
        Stops all AudioSources and frees memory that is used by
        the AudioClips.

        """
        if not config.audio:
            return
        for source in self.scene.FindComponents(AudioSource):
            mixer.Mix_HaltChannel(source.channel)
            mixer.Mix_FreeChunk(source.clip.music)
            source.clip.music = None
