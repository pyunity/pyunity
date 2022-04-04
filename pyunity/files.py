"""
Module to load files and scripts.
Also manages project structure.

"""

__all__ = ["Behaviour", "Texture2D", "Prefab",
           "File", "Project", "Skybox", "Scripts"]

from .errors import PyUnityException, ProjectParseException
from .core import Component, ShowInInspector
from . import Logger
from OpenGL import GL as gl
from PIL import Image
from types import ModuleType
import os
import sys
import ctypes

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
    object
        A C array
    """
    return (type * len(list))(*list)

class Behaviour(Component):
    """
    Base class for behaviours that can be scripted.

    Attributes
    ----------
    gameObject : GameObject
        GameObject that the component belongs to.
    transform : Transform
        Transform that the component belongs to.

    """

    _script = ShowInInspector(type)

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
                if line.split("#")[0].isspace():
                    continue
            elif line.startswith("class "):
                continue
            elif line.startswith(" ") or line.startswith("\t"):
                continue
            return False
        return True

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
        if not os.path.isfile(path):
            raise PyUnityException(f"The specified file does not exist: {path}")

        if "PyUnityScripts" in sys.modules and hasattr(sys.modules["PyUnityScripts"], "__pyunity__"):
            module = sys.modules["PyUnityScripts"]
        else:
            if "PyUnityScripts" in sys.modules:
                Logger.LogLine(
                    Logger.WARN, "PyUnityScripts is already a package")
            module = ModuleType("PyUnityScripts", None)
            module.__pyunity__ = True
            module.__all__ = []
            module._lookup = {}
            sys.modules["PyUnityScripts"] = module

        with open(path) as f:
            text = f.read().rstrip().splitlines()

        name = os.path.basename(path)[:-3]
        if Scripts.CheckScript(text):
            c = compile("\n".join(text), name + ".py", "exec")
            exec(c, Scripts.var)
            setattr(module, name, Scripts.var[name])
            module.__all__.append(name)
            module._lookup[path] = Scripts.var[name]

        return module

class Texture2D:
    """
    Class to represent a texture.

    """

    def __init__(self, path_or_im):
        if isinstance(path_or_im, str):
            self.path = path_or_im
            self.img = Image.open(self.path).convert("RGBA")
            self.img_data = self.img.tobytes()
        else:
            self.path = None
            self.img = path_or_im
            self.img_data = self.img.tobytes()
        self.loaded = False
        self.texture = None

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
            gl.GL_LINEAR_MIPMAP_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER,
            gl.GL_LINEAR)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, width, height, 0,
                        gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, self.img_data)
        gl.glEnable(gl.GL_TEXTURE_2D)
        self.loaded = True

    def setImg(self, im):
        self.loaded = False
        self.img = im
        self.path = None
        self.img_data = self.img.tobytes()

    def use(self):
        """
        Binds the texture for usage. The texture is
        reloaded if it hasn't already been.

        """
        if not self.loaded:
            self.load()
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture)

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
        self.images = []

    def compile(self):
        self.texture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_CUBE_MAP, self.texture)

        loaded = len(self.images)
        for i, name in enumerate(Skybox.names):
            if loaded:
                img = self.images[i]
            else:
                img_path = os.path.join(self.path, name)
                img = Image.open(img_path).convert("RGBA")
                self.images.append(img)
            img_data = img.tobytes()
            width, height = img.size
            gl.glTexImage2D(gl.GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, gl.GL_RGBA,
                            width, height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, img_data)

        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP,
                           gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP,
                           gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP,
                           gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP,
                           gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_CUBE_MAP,
                           gl.GL_TEXTURE_WRAP_R, gl.GL_CLAMP_TO_EDGE)

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

class Prefab:
    """Prefab model"""
    def __init__(self, gameObject, components):
        self.gameObject = gameObject
        self.components = components

class File:
    def __init__(self, path, uuid):
        self.path = os.path.normpath(path)
        self.uuid = uuid

class Project:
    def __init__(self, name="Project"):
        self.name = name
        self.path = os.path.join(os.path.abspath(os.getcwd()), self.name)
        self._ids = {}
        self._idMap = {}
        self.fileIDs = {}
        self.filePaths = {}
        self.firstScene = 0
        os.makedirs(self.name, exist_ok=True)
        self.Write()

    def Write(self):
        with open(os.path.join(self.name, self.name + ".pyunity"), "w+") as f:
            f.write(f"Project\n    name: {self.name}\n    firstScene: {self.firstScene}\nFiles")
            for id_ in self.fileIDs:
                normalized = self.fileIDs[id_].path.replace(os.path.sep, "/")
                f.write(f"\n    {id_}: {normalized}")

    def ImportFile(self, file, write=True):
        fullPath = os.path.join(self.path, file.path)
        if not os.path.isfile(fullPath):
            raise PyUnityException(f"The specified file does not exist: {fullPath}")
        self.fileIDs[file.uuid] = file
        self.filePaths[file.path] = file
        if write:
            self.Write()

    @staticmethod
    def FromFolder(folder):
        folder = os.path.abspath(folder)
        if not os.path.isdir(folder):
            raise PyUnityException(f"The specified folder does not exist: {folder}")

        name = os.path.basename(os.path.abspath(folder))
        filename = os.path.join(folder, name + ".pyunity")
        if not os.path.isfile(filename):
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
        for k, v in fileData.items():
            file = File(v, k)
            project.fileIDs[k] = file
            project.filePaths[v] = file

        return project
