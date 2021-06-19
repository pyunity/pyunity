"""
Classes to manage the playback of audio.
It uses the pygame.mixer library, and if
it cannot be initialized, then dummy
classes are made to prevent stop of program.
A variable in the ``config`` module called
``audio`` will be set to ``False`` if this
happens.

"""

__all__ = ["AudioSource", "AudioClip", "AudioListener"]

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore")
    from sdl2.sdlmixer import *
    from sdl2 import SDL_GetError

from . import config, logger as Logger
from .core import Component

channels = 0

if Mix_Init(MIX_INIT_MP3 | MIX_INIT_OGG) == 0:
    config.audio = False
    Logger.LogLine(Logger.WARN, "Cannot load sdlmixer, audio is disabled")

class AudioSource(Component):
    attrs = ["PlayOnStart", "Loop"]
    def __init__(self):
        super(AudioSource, self).__init__()
        global channels
        self.channel = channels
        channels += 1

        Mix_AllocateChannels(channels)
    
        self.PlayOnStart = False
        self.Loop = False
    
    def SetClip(self, clip):
        self.clip = clip

    def Play(self):
        if self.clip is None:
            Logger.LogLine(Logger.WARN, "AudioSource has no AudioClip")
            return
        if self.clip.music is None:
            self.clip.music = Mix_LoadWAV(self.clip.path.encode())
        if Mix_PlayChannel(self.channel, self.clip.music, 0) == -1:
            print("Unable to play file: %s" % Mix_GetError())
    
    def Stop(self):
        if self.clip is None:
            Logger.LogLine(Logger.WARN, "AudioSource has no AudioClip")
        Mix_HaltChannel(self.channel)
    
    def Pause(self):
        if self.clip is None:
            Logger.LogLine(Logger.WARN, "AudioSource has no AudioClip")
        Mix_Pause(self.channel)
    
    def UnPause(self):
        if self.clip is None:
            Logger.LogLine(Logger.WARN, "AudioSource has no AudioClip")
        Mix_Resume(self.channel)
    
    @property
    def Playing(self):
        if self.clip is None:
            Logger.LogLine(Logger.WARN, "AudioSource has no AudioClip")
        return Mix_Playing(self.channel)

class AudioClip:
    def __init__(self, path):
        self.path = path
        self.music = None

class AudioListener(Component):
    def Init(self):
        if Mix_OpenAudio(22050, MIX_DEFAULT_FORMAT, 2, 4096) == -1:
            print("SDL2_mixer could not be initialized!\nSDL_Error: %s" % SDL_GetError())
    
    def DeInit(self):
        from .scenes import SceneManager
        for source in SceneManager.CurrentScene().FindComponentsByType(AudioSource):
            Mix_HaltChannel(source.channel)
            Mix_FreeChunk(source.clip.music)
        Mix_CloseAudio()
