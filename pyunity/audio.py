"""
Classes to manage the playback of audio.
It uses the pygame.mixer library, and if
it cannot be initialized, then dummy
classes are made to prevent stop of program.
A variable in the ``config`` module called
``audio`` will be set to ``False`` if this
happens.

"""

from . import config
from .core import *
from .errors import PyUnityException
from . import logger as Logger
__all__ = ["AudioClip", "AudioSource"]

import pygame
import os
try:
    pygame.mixer.init()
except pygame.error:
    Logger.LogLine(Logger.WARN, "Cannot load pygame mixer")
    config.audio = False
    class AudioClip:
        def __init__(self, *args, **kwargs):
            Logger.LogLine(Logger.WARN,
                           "Cannot use AudioClip: pygame.mixer cannot be loaded")

        def __getattr__(self, item):
            Logger.LogLine(Logger.WARN,
                           "Cannot use AudioClip: pygame.mixer cannot be loaded")

        def __setattr__(self, item, value):
            Logger.LogLine(Logger.WARN,
                           "Cannot use AudioClip: pygame.mixer cannot be loaded")

    class AudioSource(Component):
        def __init__(self, *args, **kwargs):
            super(AudioSource, self).__init__()
            Logger.LogLine(Logger.WARN,
                           "Cannot use AudioSource: pygame.mixer cannot be loaded")

        def __getattr__(self, item):
            Logger.LogLine(Logger.WARN,
                           "Cannot use AudioSource: pygame.mixer cannot be loaded")

        def __setattr__(self, item, value):
            Logger.LogLine(Logger.WARN,
                           "Cannot use AudioSource: pygame.mixer cannot be loaded")
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
                        raise PyUnityException(
                            "Cannot use an audio file that is not of type OGG")
                else:
                    raise PyUnityException("Cannot find file: " + file)
            else:
                raise TypeError("Argument 1: Expected str, got %r" %
                                type(file).__name__)

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

        attrs = ["gameObject", "PlayOnStart", "Loop"]

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
                raise TypeError(
                    "Argument 1: Expected AudioClip, got %r" % type(clip).__name__)
            self.clip = clip

        def Play(self):
            """Plays the current clip."""
            if self.clip is None:
                Logger.LogLine(Logger.WARN, "AudioSource has no clip")
            else:
                self.channel.play(self.clip.sound)

        def Pause(self):
            """Pauses the current clip."""
            if self.clip is None:
                Logger.LogLine(Logger.WARN, "AudioSource has no clip")
            else:
                self.channel.pause()

        def UnPause(self):
            """Unpauses the current clip."""
            if self.clip is None:
                Logger.LogLine(Logger.WARN, "AudioSource has no clip")
            else:
                self.channel.unpause()

        def Stop(self):
            """Stop the current clip."""
            if self.clip is None:
                Logger.LogLine(Logger.WARN, "AudioSource has no clip")
            else:
                self.channel.stop()
