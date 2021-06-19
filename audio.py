import warnings
import ctypes

with warnings.catch_warnings():
    warnings.filterwarnings("ignore")
    from sdl2.sdlmixer import *

class AudioSource:
    def __init__(self, clip):
        self.clip = clip
        self.playing = False
    
    def Play(self):
        def finished():
            self.playing = False
        
        self.playing = True
        self.func = ctypes.CFUNCTYPE(None)(finished)
        if Mix_PlayMusic(self.clip.music, 0) == -1:
            print("Unable to play Ogg file: %s" % Mix_GetError())
        Mix_HookMusicFinished(self.func)

class AudioClip:
    def __init__(self, path):
        self.path = path
        self.music = Mix_LoadMUS(path.encode())

class AudioListener:
    def __init__(self, sources=[]):
        self.sources = sources

        if Mix_OpenAudio(22050, MIX_DEFAULT_FORMAT, 2, 4096) == -1:
            print("SDL2_mixer could not be initialized!\nSDL_Error: %s" % SDL_GetError())
    
    def add_source(self, source):
        self.sources.append(source)
    
    def wait_for_sources(self):
        finished = 0
        while finished != len(self.sources):
            finished = 0
            for source in self.sources:
                if source.playing == False:
                    finished += 1
            print(finished)
    
    def deinit(self):
        Mix_HaltMusic()
        for source in self.sources:
            Mix_FreeMusic(source.clip.music)
        Mix_CloseAudio()

listener = AudioListener()
clip = AudioClip("pyunity/examples/example8/explode.ogg")
source = AudioSource(clip)
listener.add_source(source)
source.Play()
listener.wait_for_sources()
listener.deinit()
