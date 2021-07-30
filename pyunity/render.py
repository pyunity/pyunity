"""
Classes to aid in rendering in a Scene.

"""
from typing import Dict
from OpenGL import GL as gl
from ctypes import c_float, c_ubyte, c_void_p
from .values import Color, RGB
from .errors import PyUnityException
from .core import ShowInInspector, SingleComponent, MeshRenderer
from .vector3 import Vector3
from .quaternion import Quaternion
from .files import Skybox
from . import config
import glm
import itertools
import os

float_size = gl.sizeof(c_float)

def convert(type, list):
    """
    Converts a Python array to a C type from
    ``ctypes``.

    Parameters
    ----------
    type : _ctypes.PyCSimpleType
        Type to cast to.
    list : list
        List to cast

    Returns
    -------
    Any
        A C array
    """
    return (type * len(list))(*list)

def gen_buffers(mesh):
    """
    Create buffers for a mesh.

    Parameters
    ----------
    mesh : Mesh
        Mesh to create buffers for

    Returns
    -------
    tuple
        Tuple containing a vertex buffer object and
        an index buffer object.
    """
    data = list(itertools.chain(*[[*item[0], *item[1], *item[2]]
                for item in zip(mesh.verts, mesh.normals, mesh.texcoords)]))
    indices = list(itertools.chain(*mesh.triangles))

    vbo = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, len(data) * float_size,
                    convert(c_float, data), gl.GL_STATIC_DRAW)
    ibo = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ibo)
    gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, len(indices),
                    convert(c_ubyte, indices), gl.GL_STATIC_DRAW)
    return vbo, ibo

def gen_array():
    """
    Generate a vertex array object.

    Returns
    -------
    Any
        A vertex buffer object of floats.
        Has 3 elements:

        # vertex    # normal    # texcoord
        x, y, z,    a, b, c,    u, v

    """
    vao = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(vao)
    gl.glVertexAttribPointer(
        0, 3, gl.GL_FLOAT, gl.GL_FALSE, 8 * float_size, None)
    gl.glEnableVertexAttribArray(0)
    gl.glVertexAttribPointer(
        1, 3, gl.GL_FLOAT, gl.GL_FALSE, 8 * float_size, c_void_p(3 * float_size))
    gl.glEnableVertexAttribArray(1)
    gl.glVertexAttribPointer(
        2, 2, gl.GL_FLOAT, gl.GL_FALSE, 8 * float_size, c_void_p(6 * float_size))
    gl.glEnableVertexAttribArray(2)
    return vao

class Shader:
    def __init__(self, vertex, frag, name):
        self.vertex = vertex
        self.frag = frag
        self.compiled = False
        shaders[name] = self

    def compile(self):
        self.vertexShader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        gl.glShaderSource(self.vertexShader, self.vertex, 1, None)
        gl.glCompileShader(self.vertexShader)

        success = gl.glGetShaderiv(self.vertexShader, gl.GL_COMPILE_STATUS)
        if not success:
            log = gl.glGetShaderInfoLog(self.vertexShader)
            raise PyUnityException(log)

        self.fragShader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        gl.glShaderSource(self.fragShader, self.frag, 1, None)
        gl.glCompileShader(self.fragShader)

        success = gl.glGetShaderiv(self.fragShader, gl.GL_COMPILE_STATUS)
        if not success:
            log = gl.glGetShaderInfoLog(self.fragShader)
            raise PyUnityException(log)

        self.program = gl.glCreateProgram()
        gl.glAttachShader(self.program, self.vertexShader)
        gl.glAttachShader(self.program, self.fragShader)
        gl.glLinkProgram(self.program)

        success = gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS)
        if not success:
            log = gl.glGetProgramInfoLog(self.program)
            raise PyUnityException(log)

        gl.glDeleteShader(self.vertexShader)
        gl.glDeleteShader(self.fragShader)
        self.compiled = True

    @staticmethod
    def fromFolder(path, name):
        with open(os.path.join(path, "vertex.glsl")) as f:
            vertex = f.read()

        with open(os.path.join(path, "fragment.glsl")) as f:
            fragment = f.read()

        return Shader(vertex, fragment, name)

    def setVec3(self, var, val):
        location = gl.glGetUniformLocation(self.program, var)
        gl.glUniform3f(location, *val)

    def setMat4(self, var, val):
        location = gl.glGetUniformLocation(self.program, var)
        gl.glUniformMatrix4fv(location, 1, gl.GL_FALSE, glm.value_ptr(val))

    def setInt(self, var, val):
        location = gl.glGetUniformLocation(self.program, var)
        gl.glUniform1i(location, val)

    def use(self):
        if not self.compiled:
            self.compile()
        gl.glUseProgram(self.program)


__dir = os.path.abspath(os.path.dirname(__file__))
shaders: Dict[str, Shader] = dict()
skyboxes: Dict[str, Skybox] = dict()
Shader.fromFolder(os.path.join(__dir, "shaders", "standard"), "Standard")
Shader.fromFolder(os.path.join(__dir, "shaders", "skybox"), "Skybox")
skyboxes["Water"] = Skybox(os.path.join(
    __dir, "shaders", "skybox", "textures"))

def compile_shaders():
    for shader in shaders.values():
        shader.compile()

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
    clearColor : RGB
        The clear color of the camera. Defaults to (0, 0, 0).

    """

    near = ShowInInspector(float, 0.05)
    far = ShowInInspector(float, 200)
    clearColor = ShowInInspector(Color, RGB(0, 0, 0))

    def __init__(self, transform):
        super(Camera, self).__init__(transform)
        self.size = config.size
        self.shader = shaders["Standard"]
        self.skyboxShader = shaders["Skybox"]
        self.skybox = skyboxes["Water"]
        self.shown["fov"] = ShowInInspector(int, 90, "fov")
        self.fov = 90
        self.clearColor = RGB(0, 0, 0)

        self.viewMat = glm.lookAt([0, 0, 0], [0, 0, 1], [0, 1, 0])
        self.lastPos = Vector3.zero()
        self.lastRot = Quaternion.identity()

    @property
    def fov(self):
        return self._fov

    @fov.setter
    def fov(self, fov):
        self._fov = fov
        self.projMat = glm.perspective(
            glm.radians(self._fov / self.size[0] * self.size[1]),
            self.size[0] / self.size[1],
            self.near,
            self.far)

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
        self.size = (width, height)
        self.projMat = glm.perspective(
            glm.radians(self._fov / self.size[0] * self.size[1]),
            self.size[0] / self.size[1],
            self.near,
            self.far)

    def getMatrix(self, transform):
        rotation = transform.rotation.angleAxisPair
        angle = glm.radians(rotation[0])
        axis = Vector3(rotation[1:]).normalized()

        rotated = glm.mat4_cast(glm.angleAxis(angle, list(axis)))
        position = glm.translate(rotated, list(
            transform.position * Vector3(1, 1, -1)))
        scaled = glm.scale(position, list(transform.scale))
        return scaled

    def getViewMat(self):
        if self.lastPos != self.transform.position or self.lastRot != self.transform.rotation:
            pos = self.transform.position * Vector3(1, 1, -1)
            look = pos + \
                self.transform.rotation.RotateVector(
                    Vector3.forward()) * Vector3(1, 1, -1)
            up = self.transform.rotation.RotateVector(
                Vector3.up()) * Vector3(1, 1, -1)
            self.viewMat = glm.lookAt(list(pos), list(look), list(up))
            # self.viewMat = glm.translate(glm.mat4_cast(glm.quat(
            #     *(self.transform.rotation.convert()))), list(self.transform.position))
            self.lastPos = self.transform.position
            self.lastRot = self.transform.rotation
        return self.viewMat

    def UseShader(self, name):
        self.shader = shaders[name]

    def Render(self, gameObjects):
        self.shader.use()
        viewMat = self.getViewMat()
        self.shader.setMat4(b"view", viewMat)
        self.shader.setMat4(b"projection", self.projMat)

        self.shader.setVec3(b"lightPos", [10, 10, 10])
        self.shader.setVec3(b"viewPos", list(
            self.transform.position * Vector3(1, 1, -1)))
        self.shader.setVec3(b"lightColor", [1, 1, 1])

        for gameObject in gameObjects:
            renderer = gameObject.GetComponent(MeshRenderer)
            if renderer and "self.inside_frustrum(renderer)":
                self.shader.setVec3(b"objectColor", renderer.mat.color / 255)
                self.shader.setMat4(
                    b"model", self.getMatrix(gameObject.transform))
                if renderer.mat.texture is not None:
                    self.shader.setInt(b"textured", 1)
                    renderer.mat.texture.use()
                else:
                    self.shader.setInt(b"textured", 0)
                renderer.Render()

        gl.glDepthFunc(gl.GL_LEQUAL)
        self.skyboxShader.use()
        self.skyboxShader.setMat4(b"view", glm.mat4(glm.mat3(viewMat)))
        self.skyboxShader.setMat4(b"projection", self.projMat)
        self.skybox.use()
        gl.glBindVertexArray(self.skybox.vao)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 36)
        gl.glBindVertexArray(0)
        gl.glDepthFunc(gl.GL_LESS)
