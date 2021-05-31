"""
Classes to aid in rendering in a Scene.

"""
from OpenGL import GL as gl
from OpenGL import GLU as glu
from ctypes import c_float, c_ubyte, c_void_p
from .errors import PyUnityException
from .core import SingleComponent, MeshRenderer
from .vector3 import Vector3
import glm
import itertools
import os

float_size = gl.sizeof(c_float)

def convert(type, list):
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
        self.vertex = vertex
        self.frag = frag
    
    def compile(self):
        self.vertexShader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        gl.glShaderSource(self.vertexShader, self.vertex, 1, None)
        gl.glCompileShader(self.vertexShader)
        
        self.fragShader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        gl.glShaderSource(self.fragShader, self.frag, 1, None)
        gl.glCompileShader(self.fragShader)

        self.program = gl.glCreateProgram()
        gl.glAttachShader(self.program, self.vertexShader)
        gl.glAttachShader(self.program, self.fragShader)
        gl.glLinkProgram(self.program)
        
        success = gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS)
        if not success:
            log = gl.glGetProgramInfoLog(self.program)
            raise PyUnityException(log.decode())

        gl.glDeleteShader(self.vertexShader)
        gl.glDeleteShader(self.fragShader)
    
    @staticmethod
    def fromFolder(path):
        with open(os.path.join(path, "vertex.glsl")) as f:
            vertex = f.read()
            
        with open(os.path.join(path, "fragment.glsl")) as f:
            fragment = f.read()
        
        return Shader(vertex, fragment)

    def setVec3(self, var, val):
        location = gl.glGetUniformLocation(self.program, var)
        gl.glUniform3f(location, *val)
    
    def setMat4(self, var, val):
        location = gl.glGetUniformLocation(self.program, var)
        gl.glUniformMatrix4fv(location, 1, gl.GL_FALSE, glm.value_ptr(val))
    
    def use(self):
        gl.glUseProgram(self.program)

class Camera(SingleComponent):
    """
    Component to hold data about the camera in a scene.

    Attributes
    ----------
    fov : int
        Fov in degrees measured horizontally. Defaults to 90.
    near : float
        Distance of the near plane in the camera frustrum. Defaults to 0.05.
    far : float
        Distance of the far plane in the camera frustrum. Defaults to 100.
    clearColor : tuple
        Tuple of 4 floats of the clear color of the camera. Defaults to (.1, .1, .1, 1).
        Color mode is RGBA.

    """

    def __init__(self):
        super(Camera, self).__init__()
        self.fov = 90
        self.near = 0.05
        self.far = 100
        self.clearColor = (0, 0, 0, 1)

    def Resize(self, width, height):
        """
        Resizes the viewport on screen size change.

        Parameters
        ----------
        width : int
            Width of new window
        height : int
            Height of new window

        """
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(
            self.fov / width * height,
            width / height,
            self.near,
            self.far)
        gl.glMatrixMode(gl.GL_MODELVIEW)
    
    def move(self, transform):
        """
        Transform the matrix by a specified transform.
        Parameters
        ----------
        transform : Transform
            Transform to move
        """
        gl.glRotatef(*transform.rotation.angleAxisPair)
        gl.glScalef(*transform.scale)
        gl.glTranslatef(*(transform.position * Vector3(1, 1, -1)))
    
    def Render(self, gameObjects):
        for gameObject in gameObjects:
            renderer = gameObject.GetComponent(MeshRenderer)
            if renderer and "self.inside_frustrum(renderer)":
                gl.glPushMatrix()
                self.move(gameObject.transform)
                renderer.Render()
                gl.glPopMatrix()

__dir = os.path.abspath(os.path.dirname(__file__))
shaders = {
    "Standard": Shader.fromFolder(os.path.join(__dir, "shaders", "standard"))
}