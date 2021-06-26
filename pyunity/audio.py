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

with warnings.catch_warnings():
    warnings.filterwarnings("ignore")
    from sdl2 import sdlmixer as mixer
    from sdl2 import SDL_GetError

from . import config, logger as Logger
from .core import Component

channels = 0

if "PYUNITY_TESTING" in os.environ:
    config.audio = False
    Logger.LogLine(Logger.WARN, "Testing PyUnity, audio is disabled")
elif mixer.Mix_Init(mixer.MIX_INIT_MP3 | mixer.MIX_INIT_OGG) == 0:
    config.audio = False
    Logger.LogLine(Logger.WARN, "Cannot load sdlmixer, audio is disabled")

class AudioSource(Component):
    """
    Manages playback on an AudioSource.

    Attributes
    ----------
    clip : AudioClip
        Clip to play. Best way to set the clip
        is to use the ``SetClip`` function.
    PlayOnStart : bool
        Whether it plays on start or not.
    Loop : bool
        Whether it loops or not. This is not
        fully supported.
    
    """
    
    attrs = ["PlayOnStart", "Loop"]

    def __init__(self):
        super(AudioSource, self).__init__()
        global channels
        self.clip = None
        self.channel = channels
        channels += 1
        print(channels)
        mixer.Mix_AllocateChannels(channels)
    
        self.PlayOnStart = False
        self.Loop = False
    
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
            print("Unable to play file: %s" % mixer.Mix_GetError())
    
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
        in an ``AudioSource``.
    
    """

    def __init__(self, path):
        self.path = path
        self.music = None

class AudioListener(Component):
    """
    Class to receive audio events and to base spatial
    sound from. By default the Main Camera has an
    AudioListener, but you can also remove it and
    add a new one to another GameObject in a Scene.
    There can only be one AudioListener, otherwise
    sound is disabled.

    """

    def Init(self):
        """
        Initializes the SDL2 Mixer.

        """
        if mixer.Mix_OpenAudio(22050, mixer.MIX_DEFAULT_FORMAT, 2, 4096) == -1:
            print("SDL2_mixer could not be initialized!\nSDL_Error: %s" % SDL_GetError())
    
    def DeInit(self):
        """
        Stops all AudioSources, frees memory that is used by
        the AudioClips and de-initializes the SDL2 Mixer.
        
        """
        from .scenes import SceneManager
        for source in SceneManager.CurrentScene().FindComponentsByType(AudioSource):
            mixer.Mix_HaltChannel(source.channel)
            mixer.Mix_FreeChunk(source.clip.music)
        mixer.Mix_CloseAudio()
