"""Class to create a window using Pygame."""

from ..core import Clock
from .. import config
import sdl2
import sdl2.ext
from sdl2 import video

class Window:
    """
    A window provider that uses PyGame.

    """

    def __init__(self, name, resize):
        self.resize = resize

        self.screen = sdl2.SDL_CreateWindow(
            name.encode(), sdl2.SDL_WINDOWPOS_UNDEFINED,
            sdl2.SDL_WINDOWPOS_UNDEFINED, *config.size,
            sdl2.SDL_WINDOW_OPENGL
        )

        video.SDL_GL_SetAttribute(video.SDL_GL_MULTISAMPLEBUFFERS, 1)
        video.SDL_GL_SetAttribute(video.SDL_GL_MULTISAMPLESAMPLES, 8)
        video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MAJOR_VERSION, 3)
        video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MINOR_VERSION, 3)
        video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_PROFILE_MASK, video.SDL_GL_CONTEXT_PROFILE_CORE)

        self.context = sdl2.SDL_GL_CreateContext(self.screen)

        renderer = sdl2.SDL_CreateRenderer(self.screen, -1, 0)
        sdl2.SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255)
        sdl2.SDL_RenderClear(renderer)
        sdl2.SDL_RenderPresent(renderer)

    def quit(self):
        pass

    def start(self, update_func):
        self.update_func = update_func

        done = False
        clock = Clock()
        clock.Start(config.fps)
        while not done:
            events = sdl2.ext.get_events()
            for event in events:
                if event.type == sdl2.SDL_QUIT:
                    done = True
            
            self.update_func()
            sdl2.SDL_GL_SwapWindow(self.screen)

            clock.Maintain()

        self.quit()