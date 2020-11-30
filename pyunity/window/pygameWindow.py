"""Class to create a window using Pygame."""

import pygame
import os
os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init()

class Window:
    """
    A window provider that uses PyGame.

    """

    def __init__(self, config, name, resize):
        self.config = config
        self.resize = resize

        self.window = pygame.display.set_mode(
            config.size, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)
        pygame.display.set_caption(name)

        self.keys = {
            "up": [0 for i in range(323)],
            "down": [0 for i in range(323)],
            "pressed": [0 for i in range(323)],
        }

    def start(self, update_func):
        """
        Start the main loop of the window.

        Parameters
        ----------
        update_func : function
            The function that calls the OpenGL calls.

        """
        self.update_func = update_func
        done = False
        clock = pygame.time.Clock()
        pygame.display.flip()
        while not done:
            self.keys["up"] = [0 for i in range(323)]
            self.keys["down"] = [0 for i in range(323)]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.VIDEORESIZE:
                    self.resize(*event.dict['size'])
                    self.update_func()
                    pygame.display.flip()
                elif event.type == pygame.KEYDOWN:
                    self.keys["down"][event.key] = 1
                elif event.type == pygame.KEYUP:
                    self.keys["up"][event.key] = 1

            pressed = pygame.key.get_pressed()
            self.keys["pressed"] = pressed
            alt_pressed = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
            if pressed[pygame.K_ESCAPE] or (alt_pressed and pressed[pygame.K_F4]):
                done = True

            self.update_func()
            pygame.display.flip()
            clock.tick(self.config.fps)

        pygame.display.quit()

    def get_keys(self):
        return self.keys["pressed"]

    def get_keys_down(self):
        return self.keys["down"]

    def get_keys_up(self):
        return self.keys["up"]
