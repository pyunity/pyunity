import pygame, os
os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init()

from .. import config

class Window:
    def __init__(self, size, name):
        self.window = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption(name)
    
    def start(self, update_func):
        done = False
        clock = pygame.time.Clock()
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            
            pressed = pygame.key.get_pressed()
            alt_pressed = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
            if pressed[pygame.K_ESCAPE] or (alt_pressed and pressed[pygame.K_F4]):
                done = True
                break
            
            update_func()
            pygame.display.flip()
            clock.tick(config.fps)
        
        exit()