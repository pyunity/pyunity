import warnings
import ctypes

with warnings.catch_warnings():
    warnings.filterwarnings("ignore")
    from sdl2.sdlmixer import *
    from sdl2 import SDL_GetError

channels = 0

class AudioSource:
    def __init__(self, clip):
        global channels
        self.clip = clip
        self.playing = False
        self.channel = channels
        channels += 1

        Mix_AllocateChannels(channels)
    
    def Play(self):
        def finished(channel):
            print("Channel %d finished playing" % channel)
            self.playing = False
        
        self.playing = True
        self.func = ctypes.CFUNCTYPE(None, ctypes.c_int)(finished)
        if Mix_PlayChannel(self.channel, self.clip.music, 0) == -1:
            print("Unable to play file: %s" % Mix_GetError())
        Mix_ChannelFinished(self.func)
    
    def Stop(self):
        Mix_HaltChannel(self.channel)
        self.playing = False
    
    def Pause(self):
        Mix_Pause(self.channel)
        self.playing = False
    
    def UnPause(self):
        Mix_Resume(self.channel)
        self.playing = True

class AudioClip:
    def __init__(self, path):
        self.path = path
        self.music = Mix_LoadWAV(path.encode())

class AudioListener:
    def __init__(self, sources=[]):
        self.sources = sources

        if Mix_OpenAudio(22050, MIX_DEFAULT_FORMAT, 2, 4096) == -1:
            print("SDL2_mixer could not be initialized!\nSDL_Error: %s" % SDL_GetError())
    
    def add_source(self, source):
        self.sources.append(source)
    
    def wait_for_sources(self):
        while True:
            playing = 0
            for i in range(channels):
                if Mix_Playing(i):
                    playing += 1
            if playing == 0:
                break
    
    def deinit(self):
        for source in self.sources:
            Mix_HaltChannel(source.channel)
            Mix_FreeChunk(source.clip.music)
        Mix_CloseAudio()

listener = AudioListener()
for i in range(16):
    clip = AudioClip("pyunity/examples/example8/explode.ogg")
    source = AudioSource(clip)
    listener.add_source(source)
    source.Play()
listener.wait_for_sources()
listener.deinit()
