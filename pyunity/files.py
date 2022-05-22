# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

"""
Module to load files and scripts.
Also manages project structure.

"""

__all__ = ["Behaviour", "Texture2D", "Prefab", "Asset",
           "File", "Project", "Skybox", "Scripts"]

from .errors import PyUnityException, ProjectParseException
from .core import Component, GameObject, SavesProjectID, Transform
from .values import ABCMeta, abstractmethod
from . import Logger
from types import ModuleType
from pathlib import Path
from PIL import Image
import OpenGL.GL as gl
import ctypes
import sys
import os

def convert(type, list):
    """
    Converts a Python array to a C type from
    :mod:`ctypes`.

    Parameters
    ----------
    type : _ctypes.PyCSimpleType
        Type to cast to.
    list : list
        List to cast

    Returns
    -------
    object
        A C array
    """
    return (type * len(list))(*list)

class Behaviour(Component):
    """
    Base class for behaviours that can be scripted.

    """

    def Start(self):
        """
        Called every time a scene is loaded up.

        """
        pass

    def Update(self, dt):
        """
        Called every frame.

        Parameters
        ----------
        dt : float
            Time since last frame, sent by the scene
            that the Behaviour is in.

        """
        pass

    def FixedUpdate(self, dt):
        """
        Called every frame, in each physics step.

        Parameters
        ----------
        dt : float
            Length of this physics step

        """
        pass

    def LateUpdate(self, dt):
        """
        Called every frame, after physics processing.

        Parameters
        ----------
        dt : float
            Time since last frame, sent by the scene
            that the Behaviour is in.

        """
        pass

class Scripts:
    """Utility class for loading scripts in a folder."""

    var = {}

    @staticmethod
    def CheckScript(text):
        """
        Check if ``text`` is a valid script for PyUnity.

        Parameters
        ----------
        text : list
            List of lines

        Returns
        -------
        bool
            If script is valid or not.

        Notes
        -----
        This function checks each line to see if it matches at
        least one of these criteria:

        1. The line is an ``import`` statement
        2. The line is just whitespace or blank
        3. The line is just a comment preceded by whitespace or nothing
        4. The line is a class definition
        5. The line has an indentation at the beginning

        These checks are essential to ensure no malicious code is run to
        break the PyUnity engine.

        """
        for line in text:
            if line.startswith("import") or \
                    (line.startswith("from") and " import " in line):
                continue
            elif line.isspace() or line == "":
                continue
            elif "#" in line:
                before = line.split("#")[0]
                if before.isspace() or before == "":
                    continue
            elif line.startswith("class "):
                continue
            elif line.startswith(" ") or line.startswith("\t"):
                continue
            return False
        return True

    @staticmethod
    def GenerateModule():
        if "PyUnityScripts" in sys.modules:
            if hasattr(sys.modules["PyUnityScripts"], "__pyunity__"):
                return sys.modules["PyUnityScripts"]
            Logger.LogLine(
                Logger.WARN, "PyUnityScripts is already a package")
        module = ModuleType("PyUnityScripts", None)
        module.__pyunity__ = True
        module.__all__ = []
        module._lookup = {}
        sys.modules["PyUnityScripts"] = module
        return module

    @staticmethod
    def LoadScript(path):
        """
        Loads a PyUnity script by path.

        Parameters
        ----------
        path : Pathlike
            A path to a PyUnity script

        Returns
        -------
        ModuleType
            The module that contains all the imported scripts

        Notes
        -----
        This function will add a module to ``sys.modules`` that
        is called ``PyUnityScripts``, and can be imported like any
        other module. The module will also have a variable called
        ``__pyunity__`` which shows that it is from PyUnity and not
        a real module. If an existing module named ``PyUnityScripts``
        is present and does not have the ``__pyunity__`` variable set,
        then a warning will be issued and it will be replaced.

        """
        pathobj = Path(path).absolute()
        if not pathobj.is_file():
            raise PyUnityException(
                f"The specified file does not exist: {str(path)!r}")

        if hasattr(sys.modules.get("PyUnityScripts", None), "__pyunity__"):
            module = sys.modules["PyUnityScripts"]
        else:
            module = Scripts.GenerateModule()

        with open(path) as f:
            text = f.read().rstrip().splitlines()

        name = pathobj.name[:-3]
        if Scripts.CheckScript(text):
            c = compile("\n".join(text), name + ".py", "exec")
            exec(c, Scripts.var)
            if name not in Scripts.var:
                raise PyUnityException(
                    f"Cannot find class {name!r} in {str(pathobj)!r}")
            setattr(module, name, Scripts.var[name])
            module.__all__.append(name)
            module._lookup[str(path)] = Scripts.var[name]
        else:
            Logger.LogLine(Logger.WARN,
                           f"{str(pathobj)!r} is not a valid PyUnity script")

        return module

class Asset(SavesProjectID, metaclass=ABCMeta):
    @abstractmethod
    def SaveAsset(self, ctx):
        pass

class Texture2D(Asset):
    """
    Class to represent a texture.

    """

    def __init__(self, pathOrImg):
        if isinstance(pathOrImg, (str, Path)):
            self.path = str(pathOrImg)
            self.img = Image.open(self.path).convert("RGBA")
            self.imgData = self.img.tobytes()
        else:
            self.path = None
            self.img = pathOrImg
            self.imgData = self.img.tobytes()
        self.loaded = False
        self.texture = None
        self.mipmaps = False

    def load(self):
        """
        Loads the texture and sets up an OpenGL
        texture name.

        """
        width, height = self.img.size
        if self.texture is None:
            self.texture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER,
                           gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER,
                           gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER,
                           gl.GL_LINEAR_MIPMAP_LINEAR if self.mipmaps else gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER,
                           gl.GL_LINEAR)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, width, height, 0,
                        gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, self.imgData)
        if self.mipmaps:
            gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
        gl.glEnable(gl.GL_TEXTURE_2D)
        self.loaded = True

    def setImg(self, im):
        self.loaded = False
        self.img = im
        self.path = None
        self.imgData = self.img.tobytes()

    def use(self):
        """
        Binds the texture for usage. The texture is
        reloaded if it hasn't already been.

        """
        if not self.loaded:
            self.load()
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture)

    def SaveAsset(self, ctx):
        ctx.filename = Path("Textures") / (ctx.gameObject.name + ".png")
        path = ctx.project.path / ctx.filename
        self.img.save(path)

    @classmethod
    def FromOpenGL(cls, texture):
        obj = cls.__new__(cls)
        obj.loaded = True
        obj.texture = texture
        return obj

class Skybox:
    """Skybox model consisting of 6 images"""
    names = ["right.jpg", "left.jpg", "top.jpg",
             "bottom.jpg", "front.jpg", "back.jpg"]
    points = [
        -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1,
        1, 1, -1, -1, 1, -1, -1, -1, 1, -1, -1, -1,
        -1, 1, -1, -1, 1, -1, -1, 1, 1, -1, -1, 1,
        1, -1, -1, 1, -1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, -1, 1, -1, -1, -1, -1, 1, -1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, -1, 1, -1, -1, 1,
        -1, 1, -1, 1, 1, -1, 1, 1, 1, 1, 1, 1,
        -1, 1, 1, -1, 1, -1, -1, -1, -1, -1, -1, 1,
        1, -1, -1, 1, -1, -1, -1, -1, 1, 1, -1, 1
    ]

    def __init__(self, path):
        self.path = path
        self.compiled = False

    def compile(self):
        self.texture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_CUBE_MAP, self.texture)

        for i, name in enumerate(Skybox.names):
            imgPath = Path(self.path) / name
            img = Image.open(imgPath).convert("RGBA")
            imgData = img.tobytes()
            width, height = img.size
            gl.glTexImage2D(gl.GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, gl.GL_RGBA,
                            width, height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, imgData)

        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_MIN_FILTER,
                           gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_MAG_FILTER,
                           gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_WRAP_S,
                           gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_WRAP_T,
                           gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_WRAP_R,
                           gl.GL_CLAMP_TO_EDGE)

        self.vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, len(Skybox.points) * gl.sizeof(ctypes.c_float),
                        convert(ctypes.c_float, Skybox.points), gl.GL_STATIC_DRAW)

        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)
        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(
            0, 3, gl.GL_FLOAT, gl.GL_FALSE, 3 * gl.sizeof(ctypes.c_float), None)

        Logger.LogLine(Logger.INFO, "Loaded skybox")
        self.compiled = True

    def use(self):
        if os.environ["PYUNITY_INTERACTIVE"] == "1":
            if not self.compiled:
                self.compile()
            gl.glBindTexture(gl.GL_TEXTURE_CUBE_MAP, self.texture)

class Prefab(Asset):
    """Prefab model"""
    def __init__(self, gameObject, prune=True):
        if prune:
            self.gameObjects = []
            self.assets = []
            components = []
            mapping = {}

            for transform in gameObject.transform.GetDescendants():
                obj = transform.gameObject
                mapping[obj] = g
                g = GameObject(obj.name)
                g.tag = obj.tag
                g.enabled = obj.enabled
                self.gameObjects.append(g)

                parentTransform = obj.transform.parent
                if parentTransform is None:
                    newParent = None
                else:
                    newParent = mapping[parentTransform.gameObject].transform
                g.transform.ReparentTo(newParent)

                for component in obj.components:
                    if isinstance(component, Transform):
                        continue
                    new = g.AddComponent(type(component))
                    mapping[component] = new
                    components.append(new)

            # 2nd pass setting attributes
            for transform in gameObject.transform.GetDescendants():
                for component in transform.gameObject.components:
                    if isinstance(component, Transform):
                        continue
                    for k in component.saved:
                        v = getattr(component, k)
                        if isinstance(v, GameObject):
                            if v not in mapping:
                                continue
                            v = mapping[v]
                        elif isinstance(v, Component):
                            if v.gameObject not in mapping:
                                continue
                            v = mapping[v]
                        if isinstance(v, Asset):
                            self.assets.append(v)
                        setattr(mapping[component], k, v)

            self.gameObject = self.gameObjects[0]
        else:
            self.gameObjects = []
            self.assets = []

            for transform in gameObject.transform.GetDescendants():
                if transform.gameObject.scene is not None:
                    raise PyUnityException(
                        "Cannot create prefab with GameObjects that are part of a scene")
                self.gameObjects.append(transform.gameObject)

                for component in transform.gameObject.components:
                    if isinstance(component, Transform):
                        continue
                    for k in component.saved:
                        v = getattr(component, k)
                        if isinstance(v, Asset):
                            self.assets.append(v)

            self.gameObject = gameObject

    def Contains(self, obj):
        if not isinstance(obj, (GameObject, Component)):
            raise PyUnityException(
                f"Cannot check if {type(obj).__name__} is part of a Prefab")

        if isinstance(obj, GameObject):
            return obj in self.gameObjects
        else:
            return obj.gameObject in self.gameObjects

    def Instantiate(self, scene, position=None, rotation=None, scale=None, worldSpace=False):
        mapping = {}
        for gameObject in self.gameObjects:
            copy = GameObject(gameObject.name)
            copy.tag = gameObject.tag
            copy.enabled = gameObject.enabled
            mapping[gameObject] = copy
            scene.Add(copy)

            parentTransform = gameObject.transform.parent
            if parentTransform is None:
                newParent = None
            else:
                newParent = mapping[parentTransform.gameObject].transform
            copy.transform.ReparentTo(newParent)

            for component in gameObject.components:
                if isinstance(component, Transform):
                    continue
                new = g.AddComponent(type(component))
                mapping[component] = new

            for transform in gameObject.transform.GetDescendants():
                for component in transform.gameObject.components:
                    if isinstance(component, Transform):
                        continue
                    for k in component.saved:
                        v = getattr(component, k)
                        setattr(mapping[component], k, v)

        return mapping[self.gameObject]

    def SaveAsset(self, ctx):
        ctx.filename = Path("Textures") / (ctx.gameObject.name + ".png")
        path = ctx.project.path / ctx.filename
        ctx.savers[Prefab](self, path, ctx.project)

class File:
    def __init__(self, path, uuid):
        self.path = os.path.normpath(path)
        self.uuid = uuid

class Project:
    def __init__(self, name="Project"):
        self.name = name
        self.path = Path.cwd().resolve() / self.name
        self._ids = {}
        self._idMap = {}
        self.fileIDs = {}
        self.filePaths = {}
        self.firstScene = 0
        os.makedirs(self.name, exist_ok=True)
        self.Write()

    def Write(self):
        with open(Path(self.name) / (self.name + ".pyunity"), "w+") as f:
            f.write(f"Project\n    name: {self.name}\n    firstScene: {self.firstScene}\nFiles")
            for id_ in self.fileIDs:
                normalized = self.fileIDs[id_].path.replace(os.path.sep, "/")
                f.write(f"\n    {id_}: {normalized}")

    def ImportFile(self, file, write=True):
        fullPath = self.path / file.path
        if not fullPath.is_file():
            raise PyUnityException(f"The specified file does not exist: {fullPath}")
        self.fileIDs[file.uuid] = file
        self.filePaths[file.path] = file
        if write:
            self.Write()

    def SetAsset(self, file, obj):
        if file not in self.filePaths:
            raise PyUnityException(f"File is not part of project: {file!r}")

        uuid = self.filePaths[file].uuid
        self._idMap[uuid] = obj
        self._ids[obj] = uuid

    @staticmethod
    def FromFolder(folder):
        folder = Path(folder).resolve()
        if not folder.is_dir():
            raise PyUnityException(f"The specified folder does not exist: {folder}")

        name = folder.name
        filename = folder / (name + ".pyunity")
        if not filename.is_file():
            raise PyUnityException(f"The specified folder is not a PyUnity project: {folder}")

        with open(filename) as f:
            contents = f.read().rstrip().splitlines()

        if contents.pop(0) != "Project":
            raise ProjectParseException(f"Expected \"Project\" as first section")

        if "Files" not in contents:
            raise ProjectParseException(f"Expected \"Files\" as second section")

        if contents.count("Files") > 1:
            raise ProjectParseException(f"Expected \"Files\" only once, found {contents.count('files')}")

        contents1 = contents[:contents.index("Files")]
        contents2 = contents[contents.index("Files") + 1:]
        projectData = {x[0]: x[1] for x in map(lambda x: x[4:].split(": "), contents1)}
        fileData = {x[0]: x[1] for x in map(lambda x: x[4:].split(": "), contents2)}

        if "name" not in projectData:
            raise ProjectParseException(f"Expected \"name\" value in Project section")
        project = Project.__new__(Project)
        project.name = projectData["name"]
        project.firstScene = int(projectData["firstScene"])
        project.path = folder
        project._ids = {}
        project._idMap = {}

        project.fileIDs = {}
        project.filePaths = {}
        for uuid, path in fileData.items():
            file = File(path, uuid)
            project.fileIDs[uuid] = file
            project.filePaths[path] = file

        return project
