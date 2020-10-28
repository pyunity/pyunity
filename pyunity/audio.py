"""Classes to manage the playback of audio."""

import _io, os, warnings
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from .errors import *
from .core import *
from .config import *
import pygame
try:
    pygame.mixer.init()
except pygame.error:
    warnings.warn("Cannot load pygame mixer", PyUnityWarning)
    config.audio = False
    class AudioClip:
        def __init__(self, *args, **kwargs):
            warnings.warn("Cannot use AudioClip: pygame.mixer cannot be loaded", PyUnityWarning)
        
        def __getattr__(self, item):
            warnings.warn("Cannot use AudioClip: pygame.mixer cannot be loaded", PyUnityWarning)
            
    class AudioSource(Component):
        def __init__(self, *args, **kwargs):
            warnings.warn("Cannot use AudioSource: pygame.mixer cannot be loaded", PyUnityWarning)
        
        def __getattr__(self, item):
            warnings.warn("Cannot use AudioSource: pygame.mixer cannot be loaded", PyUnityWarning)
else:

    class AudioClip:
        """
        Class to store information about an audio file.
        
        Attributes
        ----------
        file : str
            Name of the file
        sound : pygame.mixer.Sound
            Sound file that can be played with
            a ``pygame.mixer.Channel``.
            Only set when the AudioClip is in
            an ``AudioSource`` n a running scene.
        
        """
        
        def __init__(self, file):
            self.SetSound(file)
        
        def SetSound(self, file):
            """
            Changes the audio file.
            
            Parameters
            ----------
            file : str
                Name of the audio file
                Must be a .ogg file, which can work
                on any platform.
            
            Raises
            ------
            PyUnityException
                If the provided file is not an OGG
                audio file
            TypeError
                If the provided file is not of type str
            
            """
            if isinstance(file, str):
                if os.path.exists(file):
                    if file.endswith(".ogg"):
                        self.file = file
                        if hasattr(self, "sound"):
                            self.sound = pygame.mixer.Sound(self.file)
                    else:
                        raise PyUnityException("Cannot use an audio file that is not of type OGG")
            else:
                raise TypeError("Argument 1: Expected str, got %r" % type(file).__name__)

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
        
        def __init__(self):
            super(AudioSource, self).__init__()
            self.clip = None
            self.PlayOnStart = True
            self.Loop = False
        
        def SetClip(self, clip):
            """
            Sets the clip to play.
            
            Parameters
            ----------
            clip : AudioClip
                Clip to set
            
            Raises
            ------
            TypeError
                If the provided clip is not of type AudioClip
            
            """
            if not isinstance(clip, AudioClip):
                raise TypeError("Argument 1: Expected AudioClip, got %r" % type(clip).__name__)
            self.clip = clip
        
        def Play(self):
            """Plays the current clip."""
            if self.clip is None:
                warnings.warn("AudioSource has no clip", PyUnityWarning)
            else:
                self.channel.play(self.clip.sound)
        
        def Pause(self):
            """Pauses the current clip."""
            if self.clip is None:
                warnings.warn("AudioSource has no clip", PyUnityWarning)
            else:
                self.channel.pause()
        
        def UnPause(self):
            """Unpauses the current clip."""
            if self.clip is None:
                warnings.warn("AudioSource has no clip", PyUnityWarning)
            else:
                self.channel.unpause()
        
        def Stop(self):
            """Stop the current clip."""
            if self.clip is None:
                warnings.warn("AudioSource has no clip", PyUnityWarning)
            else:
                self.channel.stop()