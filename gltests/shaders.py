# https://riptutorial.com/opengl/example/32043/implement-a-camera-in-ogl-4-0-glsl-400
from OpenGL.GL import *
from PIL import Image
from ctypes import c_float, c_ubyte
import pygame
import math
pygame.init()

class Shader:
    def __init__(self, vertex, frag):
        self.vertexShader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(self.vertexShader, vertex, 1, None)
        glCompileShader(self.vertexShader)
        
        self.fragShader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(self.fragShader, frag, 1, None)
        glCompileShader(self.fragShader)

        self.program = glCreateProgram()
        glAttachShader(self.program, self.vertexShader)
        glAttachShader(self.program, self.fragShader)
        glLinkProgram(self.program)

        glDeleteShader(self.vertexShader)
        glDeleteShader(self.fragShader)

        self.prjMat = glGetUniformLocation(self.program, b"u_projectionMat44")
        self.viewMat = glGetUniformLocation(self.program, b"u_viewMat44")
        self.modelMat = glGetUniformLocation(self.program, b"u_modelMat44")
    
    def use(self):
        glUseProgram(self.program)

def Normalize(v):
    len = math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
    if not len:
        return (0, 0, 0)
    return (v[0] / len, v[1] / len, v[2] / len)

def Cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0], 0.0)

def Dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

class Camera:
    def __init__(self, pos, target, fov, aspect, near, far):
        self.pos = pos
        self.target = target
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far
    
    def Perspective(self):
        fn, f_n = self.far + self.near, self.far - self.near
        r, t = self.aspect, 1 / math.tan(math.radians(self.fov) / 2)
        return [[t / r, 0, 0, 0], [0, t, 0, 0], [0, 0, -fn / f_n, -1], [0, 0, -2 * self.far * self.near / f_n, 0]]
    
    def LookAt(self):
        mz = Normalize((self.pos[0] - self.target[0], self.pos[1] - self.target[1], self.pos[2] - self.target[2]))
        mx = Normalize(Cross([0, 1, 0], mz))
        my = Normalize(Cross(mz, mx))
        tx = Dot(mx, self.pos)
        ty = Dot(my, self.pos)
        tz = Dot((-mz[0], -mz[1], -mz[2]), self.pos)
        return [[mx[0], my[0], mz[0], 0], [mx[1], my[1], mz[1], 0], [mx[2], my[2], mz[2], 0], [tx, ty, tz, 1]]
    
    def Model(self):
        return [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

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

# img = loadTexture("C:\\Users\\daoxi\\Downloads\\pyunity.png")
shader = Shader(
"""#version 330 core
layout (location = 0) in vec3 inPos;
out vec4 gl_Position;
uniform mat4 u_projectionMat44;
uniform mat4 u_viewMat44;
uniform mat4 u_modelMat44;
void main()
{
    vec4 modelPos = u_modelMat44 * vec4(inPos, 1.0);
    vec4 viewPos  = u_viewMat44 * modelPos;
    gl_Position   = u_projectionMat44 * viewPos;
}""",
"""#version 330 core
out vec4 FragColor;

void main()
{
    FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
}"""
)

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

camera = Camera([0, 0, -7.5], [0, 0, 0], 60, 800 / 500, 0.03, 50)

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
    shader.use()
    glUniformMatrix4fv(shader.prjMat, 1, GL_FALSE, camera.Perspective())
    glUniformMatrix4fv(shader.viewMat, 1, GL_FALSE, camera.LookAt())
    glUniformMatrix4fv(shader.modelMat, 1, GL_FALSE, camera.Model())
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_BYTE, None)

    pygame.display.flip()
    clock.tick(60)