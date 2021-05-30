from OpenGL.GL import *
from PIL import Image
from ctypes import c_float, c_ubyte
import glm
import pygame

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
        
        success = glGetProgramiv(self.program, GL_LINK_STATUS)
        if not success:
            log = glGetProgramInfoLog(self.program, 512, None)
            print(log)

        glDeleteShader(self.vertexShader)
        glDeleteShader(self.fragShader)

        self.proj = glGetUniformLocation(self.program, b"projection")
        self.view = glGetUniformLocation(self.program, b"view")
    
    def use(self):
        glUseProgram(self.program)

screen = pygame.display.set_mode((800, 500), pygame.DOUBLEBUF | pygame.OPENGL)

shader = Shader(
"""#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;
layout (location = 2) in vec2 aTexCoord;

uniform mat4 projection;
uniform mat4 view;

out vec3 ourColor;
out vec2 TexCoord;

void main()
{
    gl_Position = projection * view * vec4(aPos, 1.0);
    ourColor = aColor;
    TexCoord = vec2(aTexCoord.x, aTexCoord.y);
}""",
"""#version 330 core
out vec4 FragColor;

in vec3 ourColor;
in vec2 TexCoord;

uniform sampler2D ourTexture;

void main()
{
    FragColor = texture(ourTexture, TexCoord);
}"""
)

vertices = [
    # vertex       # color     # texcoord
    -1,  1,  0,    1, 0, 0,    0, 0,
     1,  1,  0,    0, 1, 0,    1, 0,
     1, -1,  0,    0, 0, 1,    1, 1,
    -1, -1,  0,    1, 1, 0,    0, 1
]

indices = [
    0, 1, 2,
    0, 2, 3,
]

img = loadTexture("..\\..\\pyunity.png")

vbo = glGenBuffers(1)
vao = glGenVertexArrays(1)
glBindVertexArray(vao)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, (c_float * len(vertices))(*vertices), GL_STATIC_DRAW)

glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(c_float), None)
glEnableVertexAttribArray(0)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(c_float), 3 * sizeof(c_float))
glEnableVertexAttribArray(1)
glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(c_float), 6 * sizeof(c_float))
glEnableVertexAttribArray(2)

ibo = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices), (c_ubyte * len(indices))(*indices), GL_STATIC_DRAW)

view = glm.lookAt([0, 0, 7.5], [0, 0, 0], [0, 1, 0])
projection = glm.perspective(glm.radians(60), 800 / 500, 0.03, 50)
viewPtr, projPtr = glm.value_ptr(view), glm.value_ptr(projection)

done = False
clock = pygame.time.Clock()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    shader.use()
    glUniformMatrix4fv(shader.view, 1, GL_FALSE, viewPtr)
    glUniformMatrix4fv(shader.proj, 1, GL_FALSE, projPtr)
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_BYTE, None)

    pygame.display.flip()
    clock.tick(60)