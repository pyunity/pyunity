## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""
Classes to aid in rendering in a Scene.

"""

__all__ = ["Camera", "Screen", "Shader", "Light", "LightType"]

from . import Logger, config
from .core import ShowInInspector, SingleComponent, addFields
from .errors import PyUnityException
from .files import Skybox, convert
from .meshes import RGB, Color, floatSize
from .resources import resolver
from .values import ImmutableStruct, Quaternion, Vector2, Vector3
import glm
import OpenGL.GL as gl
from ctypes import c_float
from pathlib import Path
import os
import enum
import hashlib
import collections.abc

def fillScreen(scale=1):
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
    VERSION = "1.10" # Must be 4 long
    def __init__(self, vertex, frag, name):
        self.vertex = vertex
        self.frag = frag
        self.compiled = False
        self.name = name
        self.uniforms = {}
        shaders[name] = self

    def __deepcopy__(self, memo=None):
        memo[id(self)] = self
        return self

    def loadCache(self, file):
        file = Path(file)
        if not file.is_file():
            return

        formats = gl.glGetIntegerv(gl.GL_PROGRAM_BINARY_FORMATS)
        if not isinstance(formats, collections.abc.Sequence):
            formats = [formats]

        with open(file, "rb") as f:
            binary = f.read()

        # Format:
        # version (4 long)
        # formatLength (1 long)
        # format (formatLength long)
        # content (rest of file)

        ver = binary[:4].decode()
        binary = binary[4:]
        if ver != Shader.VERSION:
            Logger.LogLine(Logger.WARN, "Shader", repr(self.name),
                           "is not up-to-date")
            Logger.LogLine(Logger.WARN, "Recompiling shader", repr(self.name))
            return

        formatLength = int(binary[0])
        hexstr = binary[1: formatLength + 1]
        binary = binary[formatLength + 1:]
        binaryFormat = int(hexstr.decode(), base=16)
        self.program = gl.glCreateProgram()

        if binaryFormat not in formats:
            Logger.LogLine(Logger.WARN,
                           "Shader binaryFormat not supported")
            Logger.LogLine(Logger.WARN, "Recompiling shader", repr(self.name))
            return

        try:
            gl.glProgramBinary(
                self.program, binaryFormat, binary, len(binary))
        except gl.GLError as e:
            Logger.LogLine(Logger.WARN, "glProgramBinary failed")
            Logger.LogLine(Logger.ERROR, f"ERROR: {e!r}", silent=True)
            Logger.LogLine(Logger.WARN, "Recompiling shader", repr(self.name))
            return

        success = gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS)
        if not success:
            log = gl.glGetProgramInfoLog(self.program)
            Logger.LogLine(Logger.WARN, "GL_LINK_STATUS unsuccessful")
            Logger.LogLine(Logger.ERROR, "ERROR:", log.decode(), silent=True)
            Logger.LogLine(Logger.WARN, "Recompiling shader", repr(self.name))
            return

        self.compiled = True
        Logger.LogLine(Logger.INFO, "Loaded shader", repr(self.name),
                       "hash", file.name.rsplit(".", 1)[0])

    def compile(self):
        """
        Compiles shader and generates program. Checks for errors.

        Notes
        -----
        This function will not work if there is no active framebuffer.

        """
        formats = gl.glGetIntegerv(gl.GL_PROGRAM_BINARY_FORMATS)
        if not isinstance(formats, collections.abc.Sequence):
            formats = [formats]

        folder = Logger.getDataFolder() / "ShaderCache"
        sha256 = hashlib.sha256(self.vertex.encode("utf-8"))
        sha256.update(self.frag.encode("utf-8"))
        sha256.update(hex(formats[0])[2:].encode())
        digest = sha256.hexdigest()
        file = folder / (digest + ".bin")

        self.loadCache(file)
        if self.compiled:
            return

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
        if length == 0:
            return
        out = gl.glGetProgramBinary(self.program, length)

        folder.mkdir(parents=True, exist_ok=True)
        with open(file, "wb+") as f:
            # Format:
            # version (4 long)
            # formatLength (1 long)
            # format (formatLength long)
            # content (rest of file)
            f.write(Shader.VERSION.encode())
            hexstr = hex(out[1])[2:]
            f.write(bytes([len(hexstr)]))
            f.write(hexstr.encode())
            f.write(bytes(out[0]))

        Logger.LogLine(
            Logger.INFO, "Saved shader", repr(self.name),
            "hash", digest)

    @staticmethod
    def fromFolder(path, name):
        """
        Create a Shader from a folder. It must contain ``vertex.glsl`` and ``fragment.glsl``.

        Parameters
        ----------
        path : Pathlike
            Path of folder to load
        name : str
            Name to register this shader to. Used with :meth:`Camera.SetShader`.

        """
        p = Path(path)
        if not p.is_dir():
            raise PyUnityException(f"Folder does not exist: {path!r}")
        with open(p / "vertex.glsl") as f:
            vertex = f.read()

        with open(p / "fragment.glsl") as f:
            fragment = f.read()

        return Shader(vertex, fragment, name)

    def setVec3(self, var, val):
        """
        Set a ``vec3`` uniform variable.

        Parameters
        ----------
        var : bytes
            Variable name
        val : Vector3
            Value of uniform variable

        """
        self.uniforms[var.decode()] = val
        location = gl.glGetUniformLocation(self.program, var)
        gl.glUniform3f(location, *val)

    def setMat3(self, var, val):
        """
        Set a ``mat3`` uniform variable.

        Parameters
        ----------
        var : bytes
            Variable name
        val : glm.mat3
            Value of uniform variable

        """
        self.uniforms[var.decode()] = val
        location = gl.glGetUniformLocation(self.program, var)
        gl.glUniformMatrix3fv(location, 1, gl.GL_FALSE, glm.value_ptr(val))

    def setMat4(self, var, val):
        """
        Set a ``mat4`` uniform variable.

        Parameters
        ----------
        var : bytes
            Variable name
        val : glm.mat4
            Value of uniform variable

        """
        self.uniforms[var.decode()] = val
        location = gl.glGetUniformLocation(self.program, var)
        gl.glUniformMatrix4fv(location, 1, gl.GL_FALSE, glm.value_ptr(val))

    def setInt(self, var, val):
        """
        Set an ``int`` uniform variable.

        Parameters
        ----------
        var : bytes
            Variable name
        val : int
            Value of uniform variable

        """
        self.uniforms[var.decode()] = val
        location = gl.glGetUniformLocation(self.program, var)
        gl.glUniform1i(location, val)

    def setFloat(self, var, val):
        """
        Set a ``float`` uniform variable.

        Parameters
        ----------
        var : bytes
            Variable name
        val : float
            Value of uniform variable

        """
        self.uniforms[var.decode()] = val
        location = gl.glGetUniformLocation(self.program, var)
        gl.glUniform1f(location, val)

    def use(self):
        """Compile shader if it isn't compiled, and load it into OpenGL."""
        if os.environ["PYUNITY_INTERACTIVE"] == "1":
            if not self.compiled:
                self.compile()
            gl.glUseProgram(self.program)

shaders = {}
skyboxes = {}
Shader.fromFolder(resolver.getPath("shaders/standard/"), "Standard")
Shader.fromFolder(resolver.getPath("shaders/skybox/"), "Skybox")
Shader.fromFolder(resolver.getPath("shaders/gui/"), "GUI")
Shader.fromFolder(resolver.getPath("shaders/depth/"), "Depth")
skyboxes["Water"] = Skybox(resolver.getPath("shaders/skybox/textures/"))

def compileShaders():
    for shader in shaders.values():
        shader.compile()

def compileSkyboxes():
    for skybox in skyboxes.values():
        skybox.compile()

def resetShaders():
    for shader in shaders.values():
        shader.compiled = False

def resetSkyboxes():
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

    def __init__(self):
        super(Light, self).__init__()
        self.near = 0.03
        self.far = 20

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

@addFields(
    fov=ShowInInspector(int),
    orthoSize=ShowInInspector(float))
class Camera(SingleComponent):
    """
    Component to hold data about the camera in a scene.

    Attributes
    ----------
    near : float
        Distance of the near plane in the camera frustum. Defaults to 0.05.
    far : float
        Distance of the far plane in the camera frustum. Defaults to 100.
    clearColor : Color
        The clear color of the camera. Defaults to black.
    shader : Shader
        The shader to use for 3D objects.
    skyboxEnabled : bool
        Toggle skybox on or off. Defaults to True.
    skybox : Skybox
        Selected skybox to render.
    ortho : bool
        Orthographic or perspective proection. Defaults to False.
    customProjMat: glm.mat4 or None
        If not None, will be used over any other type of projection matrix.
        Unavailable from the Editor and also not saved.
    shadows : bool
        Whether to render depthmaps and use them. Defaults to True.
    canvas : Canvas
        Target canvas to render. Defaults to None.
    depthMapSize : int
        Depth map texture size. Do not modify after scene has started.
        Defaults to 1024.

    """

    near = ShowInInspector(float, 0.05)
    far = ShowInInspector(float, 200)
    clearColor = ShowInInspector(Color, RGB(0, 0, 0))
    shader = ShowInInspector(Shader, shaders["Standard"])
    skyboxEnabled = ShowInInspector(bool, True)
    skybox = ShowInInspector(Skybox, skyboxes["Water"])
    ortho = ShowInInspector(bool, False, "Orthographic")
    shadows = ShowInInspector(bool, False)
    depthMapSize = ShowInInspector(int, 1024)

    def __init__(self):
        super(Camera, self).__init__()
        self.size = Screen.size.copy()
        self.guiShader = shaders["GUI"]
        self.skyboxShader = shaders["Skybox"]
        self.depthShader = shaders["Depth"]
        self.customProjMat = None

        self.fov = 90
        self.orthoSize = 5

        self.viewMat = glm.lookAt([0, 0, 0], [0, 0, -1], [0, 1, 0])
        self.renderPass = False

    def setupBuffers(self):
        """Creates 2D quad VBO and VAO for GUI."""
        if hasattr(self, "guiVBO") and hasattr(self, "guiVAO"):
            return

        data = [
            0.0, 1.0,
            1.0, 1.0,
            1.0, 0.0,
            0.0, 0.0,
        ]

        self.guiVBO = gl.glGenBuffers(1)
        self.guiVAO = gl.glGenVertexArrays(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.guiVBO)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, len(data) * floatSize,
                        convert(c_float, data), gl.GL_STATIC_DRAW)

        gl.glBindVertexArray(self.guiVAO)
        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(
            0, 2, gl.GL_FLOAT, gl.GL_FALSE, 2 * floatSize, None)

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
        if self.scene.mainCamera is self:
            Screen._edit(width, height)

    def getMatrix(self, transform):
        """Generates model matrix from transform."""
        if not transform.hasChanged and transform.modelMatrix is not None:
            return transform.modelMatrix
        angle, axis = transform.rotation.angleAxisPair
        angle = -glm.radians(angle)
        axis = Vector3(1, 1, -1) * axis.normalized()

        position = glm.translate(glm.mat4(), list(
            transform.position * Vector3(1, 1, -1)))
        rotated = position * glm.mat4_cast(glm.angleAxis(angle, list(axis)))
        scaled = glm.scale(rotated, list(transform.scale))
        transform.modelMatrix = scaled
        transform.hasChanged = False
        return scaled

    def get2DMatrix(self, rectTransform):
        """Generates model matrix from RectTransform."""
        rect = rectTransform.GetRect(self.size) + rectTransform.offset
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
        if self.renderPass and self.transform.hasChanged:
            # pos = self.transform.position * Vector3(1, 1, -1)
            # look = pos + \
            #     self.transform.rotation.RotateVector(
            #         Vector3.forward()) * Vector3(1, 1, -1)
            # up = self.transform.rotation.RotateVector(
            #     Vector3.up()) * Vector3(1, 1, -1)
            # self.viewMat = glm.lookAt(list(pos), list(look), list(up))

            angle, axis = self.transform.rotation.angleAxisPair
            angle = glm.radians(-angle)
            axis = axis.normalized() * Vector3(-1, -1, 1)
            rot = glm.angleAxis(angle, list(axis))
            self.viewMat = glm.translate(
                glm.mat4_cast(rot),
                list(self.transform.position * Vector3(-1, -1, 1)))
            self.renderPass = False
            self.transform.hasChanged = False
        return self.viewMat

    def UseShader(self, name):
        """Sets current shader from name."""
        self.shader = shaders[name]

    def SetupShader(self, lights):
        self.shader.use()
        if self.customProjMat is not None:
            self.shader.setMat4(b"projection", self.customProjMat)
        elif self.ortho:
            self.shader.setMat4(b"projection", self.orthoMat)
        else:
            self.shader.setMat4(b"projection", self.projMat)
        self.shader.setInt(b"useShadowMap", int(self.shadows))
        self.shader.setMat4(b"view", self.getViewMat())
        self.shader.setVec3(b"viewPos", list(
            self.transform.position * Vector3(1, 1, -1)))

        self.shader.setInt(b"numLights", len(lights))
        for i, light in enumerate(lights):
            lightName = f"lights[{i}].".encode()
            self.shader.setVec3(lightName + b"pos",
                                light.transform.position * Vector3(1, 1, -1))
            self.shader.setFloat(lightName + b"strength", light.intensity * 10)
            self.shader.setVec3(lightName + b"color",
                                light.color.toRGB() / 255)
            self.shader.setInt(lightName + b"type", int(light.type))
            direction = light.transform.forward
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
        look = pos + light.transform.forward * Vector3(1, 1, -1)
        up = light.transform.up * Vector3(1, 1, -1)
        view = glm.lookAt(list(pos), list(look), list(up))
        light.lightSpaceMatrix = proj * view

        location = b"lightSpaceMatrix"
        self.depthShader.setMat4(location, light.lightSpaceMatrix)

    def Draw(self, renderers):
        """
        Draw specific renderers, taking into account light positions.

        Parameters
        ----------
        renderers : List[MeshRenderer]
            Which meshes to render

        """
        self.shader.use()
        for renderer in renderers:
            model = self.getMatrix(renderer.transform)
            normModel = glm.transpose(glm.inverse(glm.mat3(model)))
            self.shader.setMat4(b"model", model)
            self.shader.setMat3(b"normModel", normModel)
            self.shader.setVec3(b"objectColor", renderer.mat.color.toRGB() / 255)
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

    def RenderDepth(self, renderers, lights):
        previousFBO = gl.glGetIntegerv(gl.GL_DRAW_FRAMEBUFFER_BINDING)
        previousViewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
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

        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, previousFBO)
        gl.glViewport(*previousViewport)

    def RenderScene(self, renderers, lights):
        gl.glClearColor(*(self.clearColor.toRGB() / 255), 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        self.SetupShader(lights)
        self.Draw(renderers)

    def Render(self, renderers, lights):
        self.RenderDepth(renderers, lights)
        self.RenderScene(renderers, lights)
        self.RenderSkybox()
        self.Render2D()

    def RenderSkybox(self):
        if self.skyboxEnabled:
            gl.glDepthFunc(gl.GL_LEQUAL)
            self.skyboxShader.use()
            self.skyboxShader.setMat4(b"view", glm.mat4(glm.mat3(self.getViewMat())))
            self.skyboxShader.setMat4(b"projection", self.projMat)
            self.skybox.use()
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, 36)
            gl.glDepthFunc(gl.GL_LESS)

    def Render2D(self):
        """
        Draw all Image2D and Text components in the Camera's
        target canvas.

        If the Camera has no Canvas, this function does nothing.

        """
        if self.canvas is None:
            return

        from .gui import GuiRenderComponent
        self.Setup2D()
        renderers = []
        for gameObject in self.canvas.transform.GetDescendants():
            components = gameObject.GetComponents(GuiRenderComponent)
            renderers.extend(components)
        self.Draw2D(renderers)

    def Setup2D(self):
        self.setupBuffers()
        self.guiShader.use()
        self.guiShader.setMat4(
            b"projection", glm.ortho(0, *self.size, 0, 10, -10))
        gl.glBindVertexArray(self.guiVAO)

    def Draw2D(self, renderers):
        from .gui import RectTransform

        for renderer in renderers:
            rectTransform = renderer.GetComponent(RectTransform)
            if rectTransform is None:
                continue
            if renderer.PreRender() is not None:
                continue
            if renderer.texture is None:
                continue
            renderer.texture.use()
            self.guiShader.setMat4(
                b"model", self.get2DMatrix(rectTransform))
            self.guiShader.setFloat(b"depth", renderer.depth)
            self.guiShader.setInt(b"image", 0)
            self.guiShader.setInt(b"flipX", renderer.flipX)
            self.guiShader.setInt(b"flipY", renderer.flipY)
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
