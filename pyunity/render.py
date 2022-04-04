"""
Classes to aid in rendering in a Scene.

"""

__all__ = ["Camera", "Screen", "Shader", "Light", "LightType"]

from .values import Color, RGB, Vector3, Vector2, Quaternion, ImmutableStruct
from .errors import *
from .core import ShowInInspector, SingleComponent
from .files import Skybox, convert
from . import config, Logger
from typing import Dict
from OpenGL import GL as gl
from ctypes import c_float, c_ubyte, c_void_p
import enum
import hashlib
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

def fill_screen(scale=1):
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glLoadIdentity()
    gl.glBegin(gl.GL_QUADS)
    gl.glColor3f(1, 0, 0)
    gl.glVertex3f(-scale, scale, 0)
    gl.glColor3f(1, 1, 0)
    gl.glVertex3f(scale, scale, 0)
    gl.glColor3f(0, 1, 0)
    gl.glVertex3f(scale, -scale, 0)
    gl.glColor3f(0, 0, 1)
    gl.glVertex3f(-scale, -scale, 0)
    gl.glEnd()

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
        folder = os.path.join(os.path.dirname(Logger.folder), "ShaderCache")
        sha256 = hashlib.sha256(self.vertex.encode("utf-8"))
        sha256.update(self.frag.encode("utf-8"))
        digest = sha256.hexdigest()

        if os.path.isfile(os.path.join(folder, digest + ".bin")):
            with open(os.path.join(folder, digest + ".bin"), "rb") as f:
                binary = f.read()

            binaryFormat = int(binary[0])
            self.program = gl.glCreateProgram()
            gl.glProgramBinary(
                self.program, binaryFormat, binary[1:], len(binary))

            success = gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS)
            if success:
                self.compiled = True
                Logger.LogLine(Logger.INFO, "Loaded shader",
                    repr(self.name), "hash", digest)
                return
            else:
                log = gl.glGetProgramInfoLog(self.program)
                Logger.LogLine(Logger.WARN, log.decode())

        vertexShader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        gl.glShaderSource(vertexShader, self.vertex, 1, None)
        gl.glCompileShader(vertexShader)

        success = gl.glGetShaderiv(vertexShader, gl.GL_COMPILE_STATUS)
        if not success:
            log = gl.glGetShaderInfoLog(vertexShader)
            raise PyUnityException(log.decode())

        fragShader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        gl.glShaderSource(fragShader, self.frag, 1, None)
        gl.glCompileShader(fragShader)

        success = gl.glGetShaderiv(fragShader, gl.GL_COMPILE_STATUS)
        if not success:
            log = gl.glGetShaderInfoLog(fragShader)
            raise PyUnityException(log.decode())

        self.program = gl.glCreateProgram()
        gl.glAttachShader(self.program, vertexShader)
        gl.glAttachShader(self.program, fragShader)
        gl.glLinkProgram(self.program)

        success = gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS)
        if not success:
            log = gl.glGetProgramInfoLog(self.program)
            raise PyUnityException(log)

        gl.glDeleteShader(vertexShader)
        gl.glDeleteShader(fragShader)
        self.compiled = True

        Logger.LogLine(Logger.INFO, "Compiled shader", repr(self.name))

        length = gl.glGetProgramiv(self.program, gl.GL_PROGRAM_BINARY_LENGTH)
        out = gl.glGetProgramBinary(self.program, length)

        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, digest + ".bin"), "wb+") as f:
            f.write(bytes([out[1]]))
            f.write(bytes(out[0]))

        Logger.LogLine(
            Logger.INFO, "Saved shader", repr(self.name), "hash", digest)

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
            raise PyUnityException(f"Folder does not exist: {path!r}")
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
        if os.environ["PYUNITY_INTERACTIVE"] == "1":
            if not self.compiled:
                self.compile()
            gl.glUseProgram(self.program)

__dir = os.path.abspath(os.path.dirname(__file__))
shaders: Dict[str, Shader] = dict()
skyboxes: Dict[str, Skybox] = dict()
skyboxes["Water"] = Skybox(os.path.join(
    __dir, "shaders", "skybox", "textures"))
Shader.fromFolder(os.path.join(__dir, "shaders", "standard"), "Standard")
Shader.fromFolder(os.path.join(__dir, "shaders", "skybox"), "Skybox")
Shader.fromFolder(os.path.join(__dir, "shaders", "gui"), "GUI")
Shader.fromFolder(os.path.join(__dir, "shaders", "depth"), "Depth")

def compile_shaders():
    if os.environ["PYUNITY_INTERACTIVE"] == "1":
        for shader in shaders.values():
            shader.compile()

def compile_skyboxes():
    if os.environ["PYUNITY_INTERACTIVE"] == "1":
        for skybox in skyboxes.values():
            skybox.compile()

def reset_shaders():
    for shader in shaders.values():
        shader.compiled = False

def reset_skyboxes():
    for skybox in skyboxes.values():
        skybox.compiled = False

class LightType(enum.IntEnum):
    Point = 0
    Directional = 1
    Spot = 2

class Light(SingleComponent):
    """
    Component to hold data about the light in a scene.

    Attributes
    ----------
    intensity : int
        Intensity of light
    color : Color
        Light color (will mix with material color)
    type : LightType
        Type of light (currently only Point and
        Directional are supported)

    """

    intensity = ShowInInspector(int, 20)
    color = ShowInInspector(Color, RGB(255, 255, 255))
    type = ShowInInspector(LightType, LightType.Directional)

    def __init__(self, transform):
        super(Light, self).__init__(transform)
        self.near = 0.03
        self.far = 30

    def setupBuffers(self, depthMapSize):
        self.depthFBO = gl.glGenFramebuffers(1)
        self.depthMap = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.depthMap)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_DEPTH_COMPONENT,
            depthMapSize, depthMapSize, 0, gl.GL_DEPTH_COMPONENT,
            gl.GL_FLOAT, None)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER,
            gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER,
            gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S,
            gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T,
            gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_COMPARE_MODE,
            gl.GL_COMPARE_REF_TO_TEXTURE)

        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.depthFBO)
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_DEPTH_ATTACHMENT,
            gl.GL_TEXTURE_2D, self.depthMap, 0)
        gl.glDrawBuffer(gl.GL_NONE)
        gl.glReadBuffer(gl.GL_NONE)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)

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
    clearColor = ShowInInspector(Color)
    shader = ShowInInspector(Shader, shaders["Standard"])
    skyboxEnabled = ShowInInspector(bool, True)
    skybox = ShowInInspector(Skybox, skyboxes["Water"])
    ortho = ShowInInspector(bool, False, "Orthographic")
    shadows = ShowInInspector(bool, True)
    depthMapSize = ShowInInspector(int, 1024)

    def __init__(self, transform):
        super(Camera, self).__init__(transform)
        self.size = Screen.size.copy()
        self.guiShader = shaders["GUI"]
        self.skyboxShader = shaders["Skybox"]
        self.depthShader = shaders["Depth"]
        self.clearColor = RGB(0, 0, 0)

        self.shown["fov"] = ShowInInspector(int, 90, "fov")
        self.shown["orthoSize"] = ShowInInspector(float, 5, "Ortho Size")
        self.fov = 90
        self.orthoSize = 5

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
    def fov(self, value):
        self._fov = value
        self.projMat = glm.perspective(
            glm.radians(self._fov / self.size.x * self.size.y),
            self.size.x / self.size.y,
            self.near,
            self.far)

    @property
    def orthoSize(self):
        return self._orthoSize

    @orthoSize.setter
    def orthoSize(self, value):
        self._orthoSize = value
        width = value * self.size.x / self.size.y
        self.orthoMat = glm.ortho(
            -width, width, -value, value, self.near, self.far)

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
        angle, axis = transform.rotation.angleAxisPair
        angle = glm.radians(angle)
        axis = axis.normalized()

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
        if self.renderPass and (self.lastPos != self.transform.position or
                                self.lastRot != self.transform.rotation):
            pos = self.transform.position * Vector3(1, 1, -1)
            look = pos + \
                self.transform.rotation.RotateVector(
                    Vector3.forward()) * Vector3(1, 1, -1)
            up = self.transform.rotation.RotateVector(
                Vector3.up()) * Vector3(1, 1, -1)
            self.viewMat = glm.lookAt(list(pos), list(look), list(up))

            # self.viewMat = glm.translate(
            #     glm.mat4_cast(glm.quat(*self.transform.rotation)),
            #     list(self.transform.position * Vector3(-1, -1, 1)))
            self.lastPos = self.transform.position
            self.lastRot = self.transform.rotation
            self.renderPass = False
        return self.viewMat

    def UseShader(self, name):
        """Sets current shader from name."""
        self.shader = shaders[name]

    def SetupShader(self, lights):
        self.shader.use()
        if self.ortho:
            self.shader.setMat4(b"projection", self.orthoMat)
        else:
            self.shader.setMat4(b"projection", self.projMat)
        self.shader.setInt(b"useShadowMap", int(self.shadows))
        self.shader.setMat4(b"view", self.getViewMat())
        self.shader.setVec3(b"viewPos", list(
            self.transform.position * Vector3(1, 1, -1)))

        self.shader.setInt(b"light_num", len(lights))
        for i, light in enumerate(lights):
            lightName = f"lights[{i}].".encode()
            self.shader.setVec3(lightName + b"pos",
                                light.transform.position * Vector3(1, 1, -1))
            self.shader.setFloat(lightName + b"strength", light.intensity * 10)
            self.shader.setVec3(lightName + b"color",
                                light.color.to_rgb() / 255)
            self.shader.setInt(lightName + b"type", int(light.type))
            direction = light.transform.rotation.RotateVector(Vector3.forward())
            self.shader.setVec3(lightName + b"dir",
                                direction * Vector3(1, 1, -1))
            if self.shadows:
                gl.glActiveTexture(gl.GL_TEXTURE1 + i)
                gl.glBindTexture(gl.GL_TEXTURE_2D, light.depthMap)
                self.shader.setInt(f"shadowMaps[{i}]".encode(), i + 1)
                location = f"lightSpaceMatrices[{i}]".encode()
                self.shader.setMat4(location, light.lightSpaceMatrix)

    def SetupDepthShader(self, light):
        self.depthShader.use()
        proj = glm.ortho(-10, 10, -10, 10, light.near, light.far)
        pos = light.transform.position * Vector3(1, 1, -1)
        look = pos + light.transform.rotation.RotateVector(
            Vector3.forward()) * Vector3(1, 1, -1)
        up = light.transform.rotation.RotateVector(
            Vector3.up()) * Vector3(1, 1, -1)
        view = glm.lookAt(list(pos), list(look), list(up))
        light.lightSpaceMatrix = proj * view

        location = b"lightSpaceMatrix"
        self.depthShader.setMat4(location, light.lightSpaceMatrix)

    def Draw(self, renderers):
        """
        Draw specific renderers, taking into account light positions.

        Parameters
        ==========
        renderers : List[MeshRenderer]
            Which meshes to render
        lights : List[Light]
            Lights to load into shader

        """
        self.shader.use()
        for renderer in renderers:
            model = self.getMatrix(renderer.transform)
            self.shader.setVec3(b"objectColor", renderer.mat.color / 255)
            self.shader.setMat4(b"model", model)
            if renderer.mat.texture is not None:
                self.shader.setInt(b"textured", 1)
                renderer.mat.texture.use()
            renderer.Render()

    def DrawDepth(self, renderers):
        self.depthShader.use()
        for renderer in renderers:
            model = self.getMatrix(renderer.transform)
            self.depthShader.setMat4(b"model", model)
            renderer.Render()

    def Render(self, renderers, lights, canvases):
        if self.shadows:
            gl.glDisable(gl.GL_CULL_FACE)
            for light in lights:
                if not hasattr(light, "depthFBO"):
                    light.setupBuffers(self.depthMapSize)
                gl.glViewport(0, 0, self.depthMapSize, self.depthMapSize)
                gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, light.depthFBO)
                self.SetupDepthShader(light)
                gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
                self.DrawDepth(renderers)
            gl.glEnable(gl.GL_CULL_FACE)

            # from PIL import Image
            # data = gl.glReadPixels(0, 0, self.depthMapSize, self.depthMapSize,
            #     gl.GL_DEPTH_COMPONENT, gl.GL_UNSIGNED_BYTE, outputType=int)
            # im = Image.fromarray(data, "L")
            # im.rotate(180).save("test.png")

        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
        gl.glViewport(0, 0, *self.size)
        gl.glClearColor(*(self.clearColor.to_rgb() / 255), 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        self.SetupShader(lights)
        self.Draw(renderers)

        self.RenderSkybox()
        self.Draw2D(canvases)

    def RenderSkybox(self):
        if self.skyboxEnabled:
            gl.glDepthFunc(gl.GL_LEQUAL)
            self.skyboxShader.use()
            self.skyboxShader.setMat4(b"view", glm.mat4(glm.mat3(self.getViewMat())))
            self.skyboxShader.setMat4(b"projection", self.projMat)
            self.skybox.use()
            gl.glBindVertexArray(self.skybox.vao)
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, 36)
            gl.glDepthFunc(gl.GL_LESS)

    def Draw2D(self, canvases):
        """
        Draw all Image2D and Text components in specified canvases.

        Parameters
        ==========
        canvases : List[Canvas]
            Canvases to process. All processed GameObjects are cached
            to prevent duplicate rendering.

        """
        from .gui import Image2D, RectTransform, Text
        self.guiShader.use()
        self.guiShader.setMat4(
            b"projection", glm.ortho(0, *self.size, 0, 10, -10))
        gl.glBindVertexArray(self.guiVAO)
        gl.glDepthMask(gl.GL_FALSE)

        gameObjects = []
        renderers = []
        for canvas in canvases:
            for gameObject in canvas.transform.GetDescendants():
                if gameObject in gameObjects:
                    continue
                gameObjects.append(gameObject)
                rectTransform = gameObject.GetComponent(RectTransform)
                if rectTransform is None:
                    continue

                renderer = gameObject.GetComponent(Image2D)
                text = gameObject.GetComponent(Text)

                if renderer is not None:
                    renderers.append((renderer, rectTransform))
                if text is not None:
                    renderers.append((text, rectTransform))
                    if text.texture is None:
                        text.GenTexture()

        for renderer, rectTransform in renderers:
            if renderer.texture is None:
                continue
            renderer.texture.use()
            self.guiShader.setMat4(
                b"model", self.get2DMatrix(rectTransform))
            self.guiShader.setFloat(b"depth", renderer.depth)
            gl.glDrawArrays(gl.GL_QUADS, 0, 4)
        gl.glDepthMask(gl.GL_TRUE)

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
