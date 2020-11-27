import pygame
pygame.init()

screen = pygame.display.set_mode((800, 500))

clock = pygame.time.Clock()
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            print(event)
    
    clock.tick(60)