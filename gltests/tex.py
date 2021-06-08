from OpenGL.GL import * # lgtm [py/polluting-import]
from OpenGL.GLU import * # lgtm [py/polluting-import]
from PIL import Image
import pygame
pygame.init()

def loadTexture(path):
    img = Image.open(path)
    img_data = img.tobytes()
    print(len(img_data), img.size)
    width, height = img.size
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0,
        GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glEnable(GL_TEXTURE_2D)
    return texture

screen = pygame.display.set_mode((800, 500), pygame.DOUBLEBUF | pygame.OPENGL)

img = loadTexture("..\\..\\pyunity.png")

gluPerspective(96, 800 / 500, 0.03, 50)
glTranslatef(0, 0, -3)

done = False
clock = pygame.time.Clock()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glRotatef(2, 1, 0, 0)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-1, 1, 0)
    glTexCoord2f(1, 0)
    glVertex3f(1, 1, 0)
    glTexCoord2f(1, 1)
    glVertex3f(1, -1, 0)
    glTexCoord2f(0, 1)
    glVertex3f(-1, -1, 0)
    glEnd()

    pygame.display.flip()
    clock.tick(60) 
