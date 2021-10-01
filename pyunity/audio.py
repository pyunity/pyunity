"""
Classes to manage the playback of audio.
It uses the sdl2.sdlmixer library.
A variable in the ``config`` module called
``audio`` will be set to ``False`` if the
mixer module cannot be initialized.

"""

__all__ = ["AudioSource", "AudioClip", "AudioListener"]

import warnings
import os
from . import config, Logger
from .core import Component, ShowInInspector

with warnings.catch_warnings():
    warnings.filterwarnings("ignore")
    try:
        from sdl2 import sdlmixer as mixer
        from sdl2 import SDL_GetError
    except ImportError:
        config.audio = False

channels = 0

if not config.audio:
    Logger.LogLine(
        Logger.WARN, "Failed to import PySDL2, your system may not support it.")
elif "PYUNITY_TESTING" in os.environ:
    config.audio = False
    Logger.LogLine(Logger.WARN, "Testing PyUnity, audio is disabled")
elif mixer.Mix_Init(mixer.MIX_INIT_MP3 | mixer.MIX_INIT_OGG) == 0:
    config.audio = False
    Logger.LogLine(Logger.WARN, "Cannot load sdlmixer, audio is disabled")
elif mixer.Mix_OpenAudio(22050, mixer.MIX_DEFAULT_FORMAT, 2, 4096) == -1:
    config.audio = False
    Logger.LogLine(Logger.WARN, "SDL2_mixer could not be initialized: " +
                   SDL_GetError().decode())

class _CustomMock:
    def __getattr__(self, item):
        Logger.LogLine(Logger.WARN, "Audio is currently disabled")
        return _CustomMock()

    def __setattr__(self, item, value):
        Logger.LogLine(Logger.WARN, "Audio is currently disabled")

    def __call__(self, *args, **kwargs):
        return _CustomMock()

if not config.audio:
    mixer = _CustomMock()

class AudioClip:
    """
    Class to store information about an audio file.

    Attributes
    ----------
    path : str
        Path to the file
    music : sdl2.sdlmixer.mixer.Mix_Chunk
        Sound chunk that can be played with
        an SDL2 Mixer Channel.
        Only set when the AudioClip is played
        in an :class:`AudioSource`.

    """

    def __init__(self, path):
        self.path = path
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
    clip = ShowInInspector(AudioClip)

    def __init__(self, transform):
        super(AudioSource, self).__init__(transform)
        global channels
        self.clip = None
        self.channel = channels
        channels += 1
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
        if self.clip.music is None:
            self.clip.music = mixer.Mix_LoadWAV(self.clip.path.encode())
        if mixer.Mix_PlayChannel(self.channel, self.clip.music, 0) == -1:
            Logger.LogLine(Logger.WARN, "Unable to play file: %s" %
                           mixer.Mix_GetError().decode())

    def Stop(self):
        """
        Stops playing the AudioClip attached to the AudioSource.

        """
        if self.clip is None:
            Logger.LogLine(Logger.WARN, "AudioSource has no AudioClip")
        mixer.Mix_HaltChannel(self.channel)

    def Pause(self):
        """
        Pauses the AudioClip attached to the AudioSource.

        """
        if self.clip is None:
            Logger.LogLine(Logger.WARN, "AudioSource has no AudioClip")
        mixer.Mix_Pause(self.channel)

    def UnPause(self):
        """
        Unpauses the AudioClip attached to the AudioSource.

        """
        if self.clip is None:
            Logger.LogLine(Logger.WARN, "AudioSource has no AudioClip")
        mixer.Mix_Resume(self.channel)

    @property
    def Playing(self):
        """
        Gets if the AudioSource is playing.

        """
        if self.clip is None:
            Logger.LogLine(Logger.WARN, "AudioSource has no AudioClip")
        return mixer.Mix_Playing(self.channel)

class AudioListener(Component):
    """
    Class to receive audio events and to base spatial
    sound from. By default the Main Camera has an
    AudioListener, but you can also remove it and
    add a new one to another GameObject in a Scene.
    There can only be one AudioListener, otherwise
    sound is disabled.

    """

    def __init__(self, transform):
        super(AudioListener, self).__init__(transform)
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
        from .scenes import SceneManager
        for source in SceneManager.CurrentScene().FindComponentsByType(AudioSource):
            mixer.Mix_HaltChannel(source.channel)
            mixer.Mix_FreeChunk(source.clip.music)
