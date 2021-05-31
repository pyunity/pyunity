"""
Classes to aid in rendering in a Scene.

"""
from OpenGL import GL as gl
from ctypes import c_float, c_ubyte, c_void_p
import glm
import itertools

float_size = gl.sizeof(c_float)

def convert(type, list):
    print(type, list)
    return (type * len(list))(*list)

def gen_buffers(mesh):
    data = list(itertools.chain(*[[*item[0], *item[1]] for item in zip(mesh.verts, mesh.normals)]))
    indices = list(itertools.chain(*mesh.triangles))

    vbo = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, len(data) * float_size, convert(c_float, data), gl.GL_STATIC_DRAW)
    ibo = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ibo)
    gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, len(indices), convert(c_ubyte, indices), gl.GL_STATIC_DRAW)
    return vbo, ibo

def gen_array():
    vao = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(vao)
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 6 * float_size, None)
    gl.glEnableVertexAttribArray(0)
    gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 6 * float_size, c_void_p(3 * float_size))
    gl.glEnableVertexAttribArray(1)
    return vao

class Shader:
    def __init__(self, vertex, frag):
        self.vertexShader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        gl.glShaderSource(self.vertexShader, vertex, 1, None)
        gl.glCompileShader(self.vertexShader)
        
        self.fragShader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        gl.glShaderSource(self.fragShader, frag, 1, None)
        gl.glCompileShader(self.fragShader)

        self.program = gl.glCreateProgram()
        gl.glAttachShader(self.program, self.vertexShader)
        gl.glAttachShader(self.program, self.fragShader)
        gl.glLinkProgram(self.program)
        
        success = gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS)
        if not success:
            log = gl.glGetProgramInfoLog(self.program)
            print(log)

        gl.glDeleteShader(self.vertexShader)
        gl.glDeleteShader(self.fragShader)

    def setVec3(self, var, val):
        location = gl.glGetUniformLocation(self.program, var)
        gl.glUniform3f(location, *val)
    
    def setMat4(self, var, val):
        location = gl.glGetUniformLocation(self.program, var)
        gl.glUniformMatrix4fv(location, 1, gl.GL_FALSE, glm.value_ptr(val))
    
    def use(self):
        gl.glUseProgram(self.program)
