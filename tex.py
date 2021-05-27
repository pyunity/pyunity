from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from ctypes import c_float, c_ubyte
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

img = loadTexture("C:\\Users\\daoxi\\Downloads\\pyunity.png")

vertices = [
    -1, 1, 0,
    1, 1, 0,
    1, -1, 0,
    -1, -1, 0,
]

indices = [
    0, 1, 2,
    0, 2, 3,
]

vbo = glGenBuffers(1)
vao = glGenVertexArrays(1)
glBindVertexArray(vao)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, (c_float * len(vertices))(*vertices), GL_STATIC_DRAW)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(c_float), None)
glEnableVertexAttribArray(0)

ibo = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices), (c_ubyte * len(indices))(*indices), GL_STATIC_DRAW)

gluPerspective(96, 800 / 500, 0.03, 50)
glTranslatef(0, 0, -3)

done = False
clock = pygame.time.Clock()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # glBegin(GL_QUADS)
    # glTexCoord2f(0, 0)
    # glVertex3f(-1, 1, 0)
    # glTexCoord2f(1, 0)
    # glVertex3f(1, 1, 0)
    # glTexCoord2f(1, 1)
    # glVertex3f(1, -1, 0)
    # glTexCoord2f(0, 1)
    # glVertex3f(-1, -1, 0)
    # glEnd()

    # glDrawArrays(GL_QUADS, 0, 4)
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_BYTE, None)

    pygame.display.flip()
    clock.tick(60)