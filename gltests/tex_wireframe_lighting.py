from OpenGL.GL import * # lgtm [py/polluting-import]
from PIL import Image
from ctypes import c_float, c_ubyte, c_void_p
import glm
import pygame

def convert(type, list):
    return (type * len(list))(*list)

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

class Quat:
    def __init__(self, angle, axis):
        self.angle = angle
        self.axis = axis
    
    def angleaxis(self):
        return self.angle, self.axis

class Transform:
    def __init__(self, position, rotation, scale):
        self.position = position
        self.rotation = rotation
        self.scale = scale
    
    def matrix(self):
        scaled = glm.scale(glm.mat4(1), self.scale)
        rotated = scaled * glm.mat4_cast(glm.angleAxis(*self.rotation.angleaxis()))
        position = glm.translate(rotated, self.position)
        return position

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
            log = glGetProgramInfoLog(self.program)
            print(log)

        glDeleteShader(self.vertexShader)
        glDeleteShader(self.fragShader)

    def setVec3(self, var, val):
        location = glGetUniformLocation(self.program, var)
        glUniform3f(location, *val)
    
    def setMat4(self, var, val):
        location = glGetUniformLocation(self.program, var)
        glUniformMatrix4fv(location, 1, GL_FALSE, glm.value_ptr(val))
    
    def use(self):
        glUseProgram(self.program)

screen = pygame.display.set_mode((800, 500), pygame.DOUBLEBUF | pygame.OPENGL)

shader = Shader(
"""#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;
layout (location = 2) in vec2 aTexCoord;

uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;

out vec4 gl_Position;
out vec2 TexCoord;
out vec3 normal;
out vec3 FragPos;

void main() {
    gl_Position = projection * view * model * vec4(aPos, 1.0);
    TexCoord = aTexCoord;
    normal = vec3(model * vec4(aNormal, 1.0));
    FragPos = vec3(model * vec4(aPos, 1.0));
}""",
"""#version 330 core
out vec4 FragColor;
in vec2 TexCoord;
in vec3 normal;
in vec3 FragPos;

uniform vec3 lightPos;
uniform vec3 viewPos;
uniform vec3 objectColor;
uniform vec3 lightColor;
uniform sampler2D aTexture;

void main() {
    float ambientStrength = 0.1;
    vec3 ambient = ambientStrength * lightColor;

    vec3 norm = normalize(normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;

    float specularStrength = 0.5;
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec3 specular = specularStrength * spec * lightColor;

    vec3 result = (ambient + diffuse) * objectColor;
    FragColor = texture(aTexture, TexCoord) * vec4(result, 1.0);
}"""
)

vertices = [
    # vertex       # normal      # texcoord
    -1,  1,  1,    0,  0,  1,    1, 0,
     1,  1,  1,    0,  0,  1,    0, 0,
     1, -1,  1,    0,  0,  1,    0, 1,
    -1, -1,  1,    0,  0,  1,    1, 1,

    -1,  1, -1,    0,  0, -1,    1, 0,
     1,  1, -1,    0,  0, -1,    0, 0,
     1, -1, -1,    0,  0, -1,    0, 1,
    -1, -1, -1,    0,  0, -1,    1, 1,

    -1,  1, -1,    0,  1,  0,    1, 0,
     1,  1, -1,    0,  1,  0,    0, 0,
     1,  1,  1,    0,  1,  0,    0, 1,
    -1,  1,  1,    0,  1,  0,    1, 1,

    -1, -1, -1,    0, -1,  0,    1, 0,
     1, -1, -1,    0, -1,  0,    0, 0,
     1, -1,  1,    0, -1,  0,    0, 1,
    -1, -1,  1,    0, -1,  0,    1, 1,

    -1,  1, -1,   -1,  0,  0,    1, 0,
    -1,  1,  1,   -1,  0,  0,    0, 0,
    -1, -1,  1,   -1,  0,  0,    0, 1,
    -1, -1, -1,   -1,  0,  0,    1, 1,

     1,  1, -1,    1,  0,  0,    1, 0,
     1,  1,  1,    1,  0,  0,    0, 0,
     1, -1,  1,    1,  0,  0,    0, 1,
     1, -1, -1,    1,  0,  0,    1, 1,
]

indices = [
    0, 1, 2,
    0, 2, 3,
    4, 6, 5,
    4, 7, 6,
    8, 9, 10,
    8, 10, 11,
    12, 14, 13,
    12, 15, 14,
    16, 17, 18,
    16, 18, 19,
    20, 22, 21,
    20, 23, 22
]

img = loadTexture("..\\..\\pyunity.png")

vbo = glGenBuffers(1)
vao = glGenVertexArrays(1)
glBindVertexArray(vao)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, len(vertices) * sizeof(c_float), convert(c_float, vertices), GL_STATIC_DRAW)

glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(c_float), None)
glEnableVertexAttribArray(0)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(c_float), c_void_p(3 * sizeof(c_float)))
glEnableVertexAttribArray(1)
glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(c_float), c_void_p(6 * sizeof(c_float)))
glEnableVertexAttribArray(2)

ibo = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices), convert(c_ubyte, indices), GL_STATIC_DRAW)

view = glm.lookAt([0, 3, 10], [0, 0, 0], [0, 1, 0])
projection = glm.perspective(glm.radians(60), 800 / 500, 0.03, 50)

transform = Transform([0, 0, 0], Quat(0, [0.2672612419124244, -0.5345224838248488, 0.8017837257372732]), [1, 1, 1])

glEnable(GL_DEPTH_TEST)

done = False
a = 0
clock = pygame.time.Clock()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    transform.rotation.angle += 0.03
    
    shader.use()
    shader.setMat4(b"view", view)
    shader.setMat4(b"projection", projection)
    shader.setMat4(b"model", transform.matrix())

    shader.setVec3(b"lightPos", [5, 5, 5])
    shader.setVec3(b"viewPos", [0, 3, 10])
    shader.setVec3(b"objectColor", [1, 1, 1])
    shader.setVec3(b"lightColor", [1, 1, 1])
    
    glBindTexture(GL_TEXTURE_2D, 0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_BYTE, None)
    glBindTexture(GL_TEXTURE_2D, img)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_BYTE, None)

    pygame.display.flip()
    clock.tick(60)