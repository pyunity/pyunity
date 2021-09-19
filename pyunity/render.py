"""
Classes to aid in rendering in a Scene.

"""
from typing import Dict
from OpenGL import GL as gl
from ctypes import c_float, c_ubyte, c_void_p
from .values import Color, RGB, Vector3, Vector2, Quaternion, ImmutableStruct
from .errors import PyUnityException
from .core import ShowInInspector, SingleComponent
from .files import Skybox, convert
from . import config, Logger
import glm
import itertools
import os

float_size = gl.sizeof(c_float)

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
        Has 3 elements::

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
        self.name = name
        shaders[name] = self

    def compile(self):
        """
        Compiles shader and generates program. Checks for errors.

        Notes
        =====
        This function will not work if there is no active framebuffer.
        
        """
        vertexShader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        gl.glShaderSource(vertexShader, self.vertex, 1, None)
        gl.glCompileShader(vertexShader)

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

        Logger.Log(Logger.INFO, "Compiled shader", repr(self.name))

    @staticmethod
    def fromFolder(path, name):
        """
        Create a Shader from a folder. It must contain ``vertex.glsl`` and ``fragment.glsl``.
        
        Parameters
        ==========
        path : str
            Path of folder to load
        name : str
            Name to register this shader to. Used with `Camera.SetShader`.

        """
        if not os.path.isdir(path):
            raise PyUnityException("Folder does not exist: " + repr(path))
        with open(os.path.join(path, "vertex.glsl")) as f:
            vertex = f.read()

        with open(os.path.join(path, "fragment.glsl")) as f:
            fragment = f.read()

        return Shader(vertex, fragment, name)

    def setVec3(self, var, val):
        """
        Set a ``vec3`` uniform variable.
        
        Parameters
        ==========
        var : bytes
            Variable name
        val : Any
            Value of uniform variable
        
        """
        location = gl.glGetUniformLocation(self.program, var)
        gl.glUniform3f(location, *val)

    def setMat4(self, var, val):
        """
        Set a ``mat4`` uniform variable.
        
        Parameters
        ==========
        var : bytes
            Variable name
        val : Any
            Value of uniform variable
        
        """
        location = gl.glGetUniformLocation(self.program, var)
        gl.glUniformMatrix4fv(location, 1, gl.GL_FALSE, glm.value_ptr(val))

    def setInt(self, var, val):
        """
        Set an ``int`` uniform variable.
        
        Parameters
        ==========
        var : bytes
            Variable name
        val : Any
            Value of uniform variable
        
        """
        location = gl.glGetUniformLocation(self.program, var)
        gl.glUniform1i(location, val)

    def setFloat(self, var, val):
        """
        Set a ``float`` uniform variable.
        
        Parameters
        ==========
        var : bytes
            Variable name
        val : Any
            Value of uniform variable
        
        """
        location = gl.glGetUniformLocation(self.program, var)
        gl.glUniform1f(location, val)

    def use(self):
        """Compile shader if it isn't compiled, and load it into OpenGL."""
        if not self.compiled:
            self.compile()
        gl.glUseProgram(self.program)

__dir = os.path.abspath(os.path.dirname(__file__))
shaders: Dict[str, Shader] = dict()
skyboxes: Dict[str, Skybox] = dict()
Shader.fromFolder(os.path.join(__dir, "shaders", "standard"), "Standard")
Shader.fromFolder(os.path.join(__dir, "shaders", "skybox"), "Skybox")
Shader.fromFolder(os.path.join(__dir, "shaders", "gui"), "GUI")
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
    shader = ShowInInspector(Shader, shaders["Standard"])
    skyboxEnabled = ShowInInspector(bool, True)
    skybox = ShowInInspector(Skybox, skyboxes["Water"])

    def __init__(self, transform):
        super(Camera, self).__init__(transform)
        self.size = Screen.size.copy()
        self.guiShader = shaders["GUI"]
        self.skyboxShader = shaders["Skybox"]
        self.shown["fov"] = ShowInInspector(int, 90, "fov")
        self.fov = 90
        self.clearColor = RGB(0, 0, 0)

        self.viewMat = glm.lookAt([0, 0, 0], [0, 0, -1], [0, 1, 0])
        self.lastPos = Vector3.zero()
        self.lastRot = Quaternion.identity()
        self.renderPass = False

    def setup_buffers(self):
        """Creates 2D quad VBO and VAO for GUI."""
        data = [
            0.0, 1.0,
            1.0, 1.0,
            1.0, 0.0,
            0.0, 0.0,
        ]

        self.guiVBO = gl.glGenBuffers(1)
        self.guiVAO = gl.glGenVertexArrays(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.guiVBO)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, len(data) * float_size,
                        convert(c_float, data), gl.GL_STATIC_DRAW)

        gl.glBindVertexArray(self.guiVAO)
        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(
            0, 2, gl.GL_FLOAT, gl.GL_FALSE, 2 * float_size, None)

    @property
    def fov(self):
        """FOV of camera"""
        return self._fov

    @fov.setter
    def fov(self, fov):
        self._fov = fov
        self.projMat = glm.perspective(
            glm.radians(self._fov / self.size.x * self.size.y),
            self.size.x / self.size.y,
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
        if width == 0 or height == 0:
            return
        gl.glViewport(0, 0, width, height)
        self.size = Vector2(width, height)
        self.projMat = glm.perspective(
            glm.radians(self._fov / self.size.x * self.size.y),
            self.size.x / self.size.y,
            self.near,
            self.far)
        Screen._edit(width, height)

    def getMatrix(self, transform):
        """Generates model matrix from transform."""
        rotation = transform.rotation.angleAxisPair
        angle = glm.radians(rotation[0])
        axis = Vector3(rotation[1:]).normalized()

        rotated = glm.mat4_cast(glm.angleAxis(angle, list(axis)))
        position = glm.translate(rotated, list(
            transform.position * Vector3(1, 1, -1)))
        scaled = glm.scale(position, list(transform.scale))
        return scaled

    def get2DMatrix(self, rectTransform):
        """Generates model matrix from RectTransform."""
        rect = rectTransform.GetRect() + rectTransform.offset
        rectMin = Vector2.min(rect.min, rect.max)
        size = (rect.max - rect.min).abs()
        pivot = size * rectTransform.pivot

        model = glm.translate(glm.mat4(1), glm.vec3(*(rectMin + pivot), 0))
        model = glm.rotate(model, glm.radians(
            rectTransform.rotation), glm.vec3(0, 0, 1))
        model = glm.translate(model, glm.vec3(*-pivot, 0))
        model = glm.scale(model, glm.vec3(*(size / 2), 1))

        return model

    def getViewMat(self):
        """Generates view matrix from Transform of camera."""
        if self.renderPass and self.lastPos != self.transform.position or self.lastRot != self.transform.rotation:
            ## OLD LOOKAT MATRIX GEN ##
            # pos = self.transform.position * Vector3(1, 1, -1)
            # look = pos + \
            #     self.transform.rotation.RotateVector(
            #         Vector3.forward()) * Vector3(1, 1, -1)
            # up = self.transform.rotation.RotateVector(
            #     Vector3.up()) * Vector3(1, 1, -1)
            # self.viewMat = glm.lookAt(list(pos), list(look), list(up))

            self.viewMat = glm.translate(glm.mat4_cast(glm.quat(*self.transform.rotation)),
                                         list(self.transform.position * Vector3(-1, -1, 1)))
            self.lastPos = self.transform.position
            self.lastRot = self.transform.rotation
            self.renderPass = False
        return self.viewMat

    def UseShader(self, name):
        """Sets current shader from name."""
        self.shader = shaders[name]

    def Render(self, renderers, lights):
        """
        Render specific renderers, taking into account light positions.
        
        Parameters
        ==========
        renderers : List[MeshRenderer]
            Which meshes to render
        lights : List[Light]
            Lights to load into shader
        
        """
        self.shader.use()
        viewMat = self.getViewMat()
        self.shader.setMat4(b"projection", self.projMat)
        self.shader.setMat4(b"view", viewMat)
        self.shader.setVec3(b"viewPos", list(
            self.transform.position * Vector3(1, 1, -1)))

        if len(lights):
            self.shader.setVec3(b"lightPos", list(
                lights[0].transform.position * Vector3(1, 1, -1)))
            self.shader.setVec3(b"lightColor", list(
                lights[0].color.to_rgb() / 255))
            self.shader.setInt(b"lighting", 1)

        for renderer in renderers:
            if "self.inside_frustrum(renderer)":
                self.shader.setVec3(b"objectColor", renderer.mat.color / 255)
                self.shader.setMat4(
                    b"model", self.getMatrix(renderer.transform))
                if renderer.mat.texture is not None:
                    self.shader.setInt(b"textured", 1)
                    renderer.mat.texture.use()
                renderer.Render()

        gl.glDepthFunc(gl.GL_LEQUAL)
        self.skyboxShader.use()
        self.skyboxShader.setMat4(b"view", glm.mat4(glm.mat3(viewMat)))
        self.skyboxShader.setMat4(b"projection", self.projMat)
        self.skybox.use()
        gl.glBindVertexArray(self.skybox.vao)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 36)
        gl.glDepthFunc(gl.GL_LESS)

    def Render2D(self, canvases):
        """
        Render all Image2D and Text components in specified canvases.

        Parameters
        ==========
        canvases : List[Canvas]
            Canvases to process. All processed GameObjects are cached
            to prevent duplicate rendering.
        
        """
        from .gui import Image2D, RectTransform, Text
        self.guiShader.use()
        self.guiShader.setMat4(
            b"projection", glm.ortho(0, *self.size, 0, -10, 10))
        gl.glBindVertexArray(self.guiVAO)

        gameObjects = []
        for canvas in canvases:
            for gameObject in canvas.transform.GetDescendants():
                if gameObject in gameObjects:
                    continue
                gameObjects.append(gameObject)
                rectTransform = gameObject.GetComponent(RectTransform)
                renderer = gameObject.GetComponent(Image2D)
                text = gameObject.GetComponent(Text)

                textures = []
                if renderer is not None and rectTransform is not None and renderer.texture is not None:
                    textures.append(renderer.texture)
                if text is not None:
                    textures.append(text.texture)
                
                for texture in textures:
                    texture.use()
                    self.guiShader.setMat4(
                        b"model", self.get2DMatrix(rectTransform))
                    self.guiShader.setFloat(b"depth", renderer.depth)
                    gl.glDrawArrays(gl.GL_QUADS, 0, 4)

class Screen(metaclass=ImmutableStruct):
    _names = ["width", "height", "size", "aspect"]
    width = config.size[0]
    height = config.size[1]
    size = Vector2(config.size)
    aspect = config.size[0] / config.size[1]

    @classmethod
    def _edit(cls, width, height):
        cls._set("width", width)
        cls._set("height", height)
        cls._set("size", Vector2(width, height))
        cls._set("aspect", width / height)
