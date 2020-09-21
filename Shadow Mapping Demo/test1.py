from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
pygame.init()

verts = [[x, y, z] for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
tris = [
    [0, 1, 2],
    [1, 3, 2],
    [4, 6, 5],
    [5, 6, 7],
    [0, 2, 4],
    [2, 6, 4],
    [1, 5, 3],
    [3, 5, 7],
    [2, 3, 6],
    [3, 7, 6],
    [0, 4, 1],
    [1, 4, 5],
]
norms = [
    [-1, 0, 0],
    [-1, 0, 0],
    [1, 0, 0],
    [1, 0, 0],
    [0, 0, -1],
    [0, 0, -1],
    [0, 0, 1],
    [0, 0, 1],
    [0, 1, 0],
    [0, 1, 0],
    [0, -1, 0],
    [0, -1, 0],
]

def Cube():
    glBegin(GL_TRIANGLES)
    glColor3f(1, 0, 0)
    for triangle, normal in zip(tris, norms):
        glNormal3fv(normal)
        for vert_index in triangle:
            glVertex3fv(verts[vert_index])
    glEnd()

window = pygame.display.set_mode((800, 500), pygame.DOUBLEBUF | pygame.OPENGL)

glMatrixMode(GL_PROJECTION)
gluPerspective(60, 1.6, 0.05, 50)
glMatrixMode(GL_MODELVIEW)

glLightfv(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 1))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))

glEnable(GL_DEPTH_TEST)
glEnable(GL_CULL_FACE)

angle = 0

done = False
clock = pygame.time.Clock()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glLight(GL_LIGHT0, GL_POSITION, (10, 10, 10, 1))

    glPushMatrix()
    glTranslatef(0, 0, -10)
    glRotatef(angle, -0.7, 0.3, 0.7)
    Cube()
    glPopMatrix()
    angle += 1 / 60 * 150

    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHTING)
    glDisable(GL_COLOR_MATERIAL)

    pygame.display.flip()
    clock.tick(60)