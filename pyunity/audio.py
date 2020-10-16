from .errors import *
import _io, os, warnings
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
pygame.mixer.init()
from .core import *

class AudioClip:
    def __init__(self, file):
        self.SetSound(file)
    
    def SetSound(self, file):
        if isinstance(file, str):
            if os.path.exists(file):
                if file.endswith(".ogg"):
                    self.file = file
                else:
                    raise PyUnityException("Cannot use an audio file that is not of type OGG")
        else:
            raise PyUnityException("Argument 1: Expected str, got %r" % type(file).__name__)

class AudioSource(Component):
    def __init__(self):
        super(AudioSource, self).__init__()
        self.clip = None
        self.PlayOnStart = True
    
    def SetClip(self, clip):
        if not isinstance(clip, AudioClip):
            raise PyUnityException("Argument 1: Expected AudioClip, got %r" % type(clip).__name__)
        self.clip = clip
    
    def Play(self):
        if self.clip is None:
            warnings.warn("AudioSource has no clip", PyUnityWarning)
        else:
            self.channel.play(self.clip.sound)
    
    def Pause(self):
        if self.clip is None:
            warnings.warn("AudioSource has no clip", PyUnityWarning)
        else:
            self.channel.pause()
    
    def UnPause(self):
        if self.clip is None:
            warnings.warn("AudioSource has no clip", PyUnityWarning)
        else:
            self.channel.unpause()
    
    def Stop(self):
        if self.clip is None:
            warnings.warn("AudioSource has no clip", PyUnityWarning)
        else:
            self.channel.stop()