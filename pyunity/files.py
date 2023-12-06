## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""
Module to load files and scripts.
Also manages project structure.

"""

__all__ = ["Behaviour", "Texture2D", "Prefab", "Asset",
           "File", "Project", "Skybox", "Scripts",
           "ProjectSavingContext"]

from . import Logger
from .core import Component, GameObject, SavesProjectID, Space, Transform
from .errors import ProjectParseException, PyUnityException
from .values import ABCMeta, abstractmethod
from PIL import Image
import OpenGL.GL as gl
from uuid import uuid4
from types import ModuleType
from pathlib import Path
from functools import wraps
import os
import sys
import copy
import ctypes
import textwrap

def convert(type, list):
    """
    Converts a Python array to a C type from
    :mod:`ctypes`.

    Parameters
    ----------
    type : Type[ctypes.PyCSimpleType]
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

    def Awake(self):
        """
        Called every time a scene is loaded up,
        regardless whether the Behaviour is
        enabled or not. Cannot be an ``async``
        function.

        """
        pass

    async def Start(self):
        """
        Called every time a scene is loaded up.
        Only called when the Behaviour is enabled.
        Can be either a normal function or an
        ``async`` function.

        """
        pass

    async def Update(self, dt):
        """
        Called every frame.
        Can be either a normal function or an
        ``async`` function.

        Parameters
        ----------
        dt : float
            Time since last frame, sent by the scene
            that the Behaviour is in.

        """
        pass

    async def FixedUpdate(self, dt):
        """
        Called every frame, in each physics step.
        Can be either a normal function or an
        ``async`` function.

        Parameters
        ----------
        dt : float
            Length of this physics step

        """
        pass

    async def LateUpdate(self, dt):
        """
        Called every frame, after physics processing.
        Can be either a normal function or an
        ``async`` function.

        Parameters
        ----------
        dt : float
            Time since last frame, sent by the scene
            that the Behaviour is in.

        """
        pass

    async def OnPreRender(self):
        """
        Called before rendering happens.
        Can be either a normal function or an
        ``async`` function.

        """
        pass

    async def OnPostRender(self):
        """
        Called after rendering happens.
        Can be either a normal function or an
        ``async`` function.

        """
        pass

    def OnDestroy(self):
        """
        Called at the end of each Scene. Cannot
        be an ``async`` function.

        """
        pass

class Scripts:
    """Utility class for loading scripts in a folder."""

    template = textwrap.dedent("""
    from pyunity import *

    class {}(Behaviour):
        async def Start(self):
            pass

        async def Update(self, dt):
            pass
    """)[1:]
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
    def LoadScript(path, force=False):
        """
        Loads a PyUnity script by path.

        Parameters
        ----------
        path : Pathlike
            A path to a PyUnity script
        force : bool
            Continue on error

        Returns
        -------
        type
            The compiled PyUnity script

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

        Scripts.GenerateModule()
        import PyUnityScripts

        with open(path) as f:
            text = f.read().rstrip().splitlines()

        name = pathobj.name[:-3]
        if Scripts.CheckScript(text):
            c = compile("\n".join(text), name + ".py", "exec")
            try:
                exec(c, Scripts.var)
            except Exception as e:
                if not force:
                    raise
                Logger.LogException(e)
            if name not in Scripts.var:
                raise PyUnityException(
                    f"Cannot find class {name!r} in {str(pathobj)!r}")
            setattr(PyUnityScripts, name, Scripts.var[name])
            PyUnityScripts.__all__.append(name)
            PyUnityScripts._lookup[str(pathobj)] = Scripts.var[name]
            return Scripts.var[name]
        else:
            Logger.LogLine(Logger.WARN,
                           f"{str(pathobj)!r} is not a valid PyUnity script")
            return None

    @staticmethod
    def Reset():
        Scripts.var = {}
        if "PyUnityScripts" in sys.modules:
            sys.modules.pop("PyUnityScripts")

class Asset(SavesProjectID, metaclass=ABCMeta):
    @abstractmethod
    def GetAssetFile(self, gameObject):
        pass

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
        elif isinstance(pathOrImg, Image.Image):
            self.path = None
            self.img = pathOrImg
            self.imgData = self.img.tobytes()
        else:
            raise TypeError(f"Expected str, Path or Image: got {type(pathOrImg).__name__}")
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

    def GetAssetFile(self, gameObject):
        return Path("Textures") / (gameObject.name + ".png")

    def SaveAsset(self, ctx):
        path = ctx.project.path / ctx.filename
        path.parent.mkdir(parents=True, exist_ok=True)
        self.img.save(path)

    @classmethod
    def FromOpenGL(cls, texture):
        # TODO: set mipmaps?
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
            gl.glBindVertexArray(self.vao)

class Prefab(Asset):
    """Prefab model"""
    def __init__(self, root, prune=True):
        if prune:
            self.gameObjects = []
            self.assets = []
            components = []
            mapping = {}

            for transform in root.transform.GetDescendants():
                gameObject = transform.gameObject
                copy = GameObject(gameObject.name)
                copy.tag = gameObject.tag
                copy.enabled = gameObject.enabled
                mapping[gameObject] = copy
                self.gameObjects.append(copy)

                parentTransform = gameObject.transform.parent
                if parentTransform is None:
                    newParent = None
                else:
                    newParent = mapping[parentTransform.gameObject].transform
                copy.transform.ReparentTo(newParent)

                for component in gameObject.components:
                    if isinstance(component, Transform):
                        mapping[component] = copy.transform
                        for k in component._shown:
                            v = getattr(component, k)
                            setattr(mapping[component], k, v)
                    else:
                        new = copy.AddComponent(type(component))
                        mapping[component] = new
                        components.append(new)

            # 2nd pass setting attributes
            for transform in root.transform.GetDescendants():
                for component in transform.gameObject.components:
                    if isinstance(component, Transform):
                        continue
                    for k in component._saved:
                        v = getattr(component, k)
                        if isinstance(v, (GameObject, Component)):
                            if v not in mapping:
                                continue
                            v = mapping[v]
                        elif isinstance(v, Asset):
                            self.assets.append(v)
                        setattr(mapping[component], k, v)

            self.gameObject = self.gameObjects[0]
        else:
            self.gameObjects = []
            self.assets = []

            for transform in root.transform.GetDescendants():
                if transform.gameObject.scene is not None:
                    raise PyUnityException(
                        "Cannot create prefab with GameObjects that are part of a scene")
                self.gameObjects.append(transform.gameObject)

                for component in transform.gameObject.components:
                    if isinstance(component, Transform):
                        continue
                    for k in component._saved:
                        v = getattr(component, k)
                        if isinstance(v, Asset):
                            self.assets.append(v)

            self.gameObject = root

    def Contains(self, obj):
        if not isinstance(obj, (GameObject, Component)):
            raise PyUnityException(
                f"Cannot check if {type(obj).__name__} is part of a Prefab")

        if isinstance(obj, GameObject):
            return obj in self.gameObjects
        else:
            return obj.gameObject in self.gameObjects

    def Instantiate(self,
                    scene=None,
                    parent=None,
                    position=None,
                    rotation=None,
                    scale=None,
                    space=Space.World):
        """
        Instantiate this prefab.

        Parameters
        ----------
        scene : Scene, optional
            The scene to instantiate in. If None, the
            current scene is selected.
        parent : GameObject, optional
            The parent to instantiate the Prefab under.
            If None, the prefab will be instantiated
            at the root of the scene.
        position : Vector3, optional
            Position of the newly created GameObject, by
            default the GameObject's original position
        rotation : Quaternion, optional
            Rotation of the newly created GameObject, by
            default the GameObject's original rotation
        scale : Vector3, optional
            Scale of the newly created GameObject, by default
            the GameObject's original scale
        worldSpace : Space, optional
            Whether the above 3 properties are world space or
            local space, by default world space

        Returns
        -------
        GameObject
            The newly created GameObject

        Raises
        ------
        PyUnityException
            If ``scene`` is None but no scene is running

        """
        if scene is None:
            from .scenes import SceneManager
            scene = SceneManager.CurrentScene()
            if scene is None:
                raise PyUnityException("No scene running")

        root = copy.deepcopy(self.gameObject)
        for transform in root.transform.GetDescendants():
            scene.Add(transform.gameObject)

        if parent is not None:
            if not isinstance(parent, (GameObject, Transform)):
                raise PyUnityException(
                    "Provided parent is not a GameObject or a Transform")
            if isinstance(parent, GameObject):
                parent = parent.transform
            root.transform.ReparentTo(parent)

        if space == Space.World:
            if position is not None:
                root.transform.position = position
            if rotation is not None:
                root.transform.rotation = rotation
            if scale is not None:
                root.transform.scale = scale
        else:
            if position is not None:
                root.transform.localPosition = position
            if rotation is not None:
                root.transform.localRotation = rotation
            if scale is not None:
                root.transform.localScale = scale
        return root

    def GetAssetFile(self, gameObject):
        return Path("Prefabs") / (gameObject.name + ".prefab")

    def SaveAsset(self, ctx):
        for asset in self.assets:
            ctx.project.ImportAsset(asset, ctx.gameObject)

        path = ctx.project.path / ctx.filename
        ctx.savers[Prefab](self, path, ctx.project)

class ProjectSavingContext:
    def __init__(self, asset, gameObject, project, filename=""):
        if not isinstance(asset, Asset):
            raise ProjectParseException(
                f"{type(asset).__name__} does not subclass Asset")
        ## Not needed since scenes do not belong to GameObjects
        # if not isinstance(gameObject, GameObject):
        #     raise ProjectParseException(
        #         f"{gameObject!r} is not a GameObject")
        if not isinstance(project, Project):
            raise ProjectParseException(
                f"{project!r} is not a GameObject")

        self.asset = asset
        self.gameObject = gameObject
        self.project = project
        self.filename = filename

        from . import Loader
        self.savers = Loader.savers

class File:
    def __init__(self, path, uuid):
        self.path = os.path.normpath(path)
        self.uuid = uuid

def checkScene(func):
    @wraps(func)
    def inner(*args, **kwargs):
        from . import SceneManager
        if SceneManager.CurrentScene() is not None:
            raise PyUnityException("Cannot modify project while scene is running")
        return func(*args, **kwargs)
    # TODO: disable this check according to a condition?
    return inner

class Project:
    def __init__(self, name="Project"):
        self.path = Path(name)
        if not self.path.is_absolute():
            self.path = self.path.resolve()
        self.name = self.path.name
        self._ids = {}
        self._idMap = {}
        self.fileIDs = {}
        self.filePaths = {}
        self.firstScene = 0
        os.makedirs(self.name, exist_ok=True)
        self.Write()

    @property
    def assets(self):
        assets = []
        for uuid in self.fileIDs:
            if uuid in self._ids:
                assets.append(self._ids[uuid])
        return assets

    @checkScene
    def Write(self):
        with open(Path(self.name) / (self.name + ".pyunity"), "w+") as f:
            f.write(f"Project\n    name: {self.name}\n    firstScene: {self.firstScene}\nFiles")
            for id_ in self.fileIDs:
                normalized = self.fileIDs[id_].path.replace(os.path.sep, "/")
                f.write(f"\n    {id_}: {normalized}")

    @checkScene
    def ImportFile(self, file, uuid=None, write=True):
        if uuid is not None:
            file = File(file, uuid)
        fullPath = self.path / file.path
        if not fullPath.is_file():
            raise PyUnityException(f"The specified file does not exist: {fullPath}")
        self.fileIDs[file.uuid] = file
        self.filePaths[file.path] = file
        if write:
            self.Write()

    @checkScene
    def ImportAsset(self, asset, gameObject=None, filename=None):
        if asset not in self._ids:
            exists = False
            uuid = str(uuid4())
            self._ids[asset] = uuid
            self._idMap[uuid] = asset
            if filename is None:
                filename = asset.GetAssetFile(gameObject)
        else:
            exists = True
            uuid = self._ids[asset]
            filename = self.fileIDs[uuid].path

        context = ProjectSavingContext(
            asset=asset,
            gameObject=gameObject,
            project=self,
            filename=filename)
        asset.SaveAsset(context)

        if not exists:
            file = File(filename, self._ids[asset])
            self.ImportFile(file, write=False)

    @checkScene
    def SetAsset(self, file, obj):
        if file not in self.filePaths:
            raise PyUnityException(f"File is not part of project: {file!r}")

        uuid = self.filePaths[file].uuid
        self._idMap[uuid] = obj
        self._ids[obj] = uuid

    @checkScene
    def GetUuid(self, obj):
        if obj is None:
            return None
        if obj in self._ids:
            return self._ids[obj]
        uuid = str(uuid4())
        self._ids[obj] = uuid
        self._idMap[uuid] = obj
        return self._ids[obj]

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
