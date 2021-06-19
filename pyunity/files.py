"""
Module to load files and scripts.
Also manages project structure.

"""

__all__ = ["Behaviour", "Texture2D", "Prefab", "File", "Project"]

from OpenGL import GL as gl
from PIL import Image
from .core import Component, Material, Color
from . import Logger
from types import ModuleType
from uuid import uuid4
import glob
import os
import sys

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

    attrs = []

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

class Scripts:
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
    def LoadScripts(path):
        """
        Loads all scripts found in ``path``.

        Parameters
        ----------
        path : Pathlike
            A path to a folder containing all the scripts

        Returns
        -------
        ModuleType
            A module that contains all the imported scripts

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
        files = glob.glob(os.path.join(path, "*.py"))
        a = {}

        if "PyUnityScripts" in sys.modules and hasattr(sys.modules["PyUnityScripts"], "__pyunity__"):
            module = sys.modules["PyUnityScripts"]
        else:
            if "PyUnityScripts" in sys.modules:
                Logger.LogLine(Logger.WARN, "PyUnityScripts is already a package!")
            module = ModuleType("PyUnityScripts", None)
            module.__pyunity__ = True
            module.__all__ = []
            sys.modules["PyUnityScripts"] = module

        for file in files:
            with open(file) as f:
                text = f.read().rstrip().splitlines()

            name = os.path.basename(file[:-3])
            if Scripts.CheckScript(text):
                exec("\n".join(text), a)
                setattr(module, name, a[name])
                module.__all__.append(name)

        return module

class Texture2D:
    """
    Class to represent a texture.

    """

    def __init__(self, path):
        self.path = path
        self.loaded = False
        self.img = Image.open(self.path).convert("RGBA")
        self.img_data = self.img.tobytes()

    def load(self):
        """
        Loads the texture and sets up an OpenGL
        texture name.

        """
        img = Image.open(self.path).convert("RGBA")
        img_data = img.tobytes()
        width, height = img.size
        self.texture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture)
        gl.glTexParameterf(
            gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameterf(
            gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, width, height, 0,
                        gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, img_data)
        gl.glEnable(gl.GL_TEXTURE_2D)
        self.loaded = True

    def use(self):
        """
        Binds the texture for usage. The texture is
        reloaded if it hasn't already been.

        """
        if not self.loaded:
            self.load()
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture)

class Prefab:
    def __init__(self, gameObject, components):
        self.gameObject = gameObject
        self.components = components

class File:
    def __init__(self, path, type, uuid=None):
        self.path = path
        self.type = type
        if uuid is None:
            self.uuid = str(uuid4())
        else:
            self.uuid = uuid
        self.obj = None

class Project:
    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.firstScene = 0
        self.files = {}
        self.file_paths = {}
    
    def import_file(self, localPath, type, uuid=None):
        file = File(localPath, type, uuid)
        self.files[file.uuid] = (file, localPath)
        self.file_paths[localPath] = file
        return file
    
    def get_file_obj(self, uuid):
        return self.files[uuid][0].obj
    
    def write_project(self):
        with open(os.path.join(self.path, self.name + ".pyunity"), "w+") as f:
            f.write("Project\n")
            f.write("    name: " + self.name + "\n")
            f.write("    firstScene: " + str(self.firstScene) + "\n")
            f.write("Files\n")
            for uuid, file in self.files.items():
                f.write("    " + uuid + ": " + file[1] + "\n")
    
    @staticmethod
    def from_folder(filePath):
        if not os.path.isdir(filePath):
            raise ValueError("The specified folder does not exist")
        
        files = glob.glob(os.path.join(filePath, "*.pyunity"))
        if len(files) == 0:
            raise ValueError("The specified folder is not a PyUnity project")
        elif len(files) > 1:
            raise ValueError("Ambiguity in specified folder: " + str(len(files)) + " project files found")
        file = files[0]

        with open(file) as f:
            lines = f.read().rstrip().splitlines()
        
        data = {}
        lines.pop(0)
        for line in lines:
            if not line.startswith("    "):
                break
            name, value = line[4:].split(": ")
            data[name] = value
        
        data["files"] = {}
        lines = lines[lines.index("Files") + 1:]
        for line in lines:
            name, value = line[4:].split(": ")
            data["files"][name] = value
        
        project = Project(filePath, data["name"])
        for uuid, path in data["files"].items():
            type_ = os.path.splitext(path)[1][1:].capitalize()
            if type_ == "Py":
                type_ = "Behaviour"
            elif type_ == "Mat":
                type_ = "Material"
            project.import_file(path, type_, uuid)
        
        return project
    
    def save_mat(self, mat, name):
        directory = os.path.join(self.path, "Materials")
        os.makedirs(directory, exist_ok=True)

        if mat.texture is not None:
            if os.path.join("Textures", name + ".png") in self.file_paths:
                uuid = self.file_paths[os.path.join("Textures", name + ".png")].uuid
            else:
                path = os.path.join(self.path, "Textures", name + ".png")
                os.makedirs(os.path.dirname(path), exist_ok=True)
                mat.texture.img.save(path)
                uuid = self.import_file(path, "Texture2D").uuid
        else:
            uuid = "None"

        with open(os.path.join(directory, name + ".mat"), "w+") as f:
            f.write("Material\n")
            f.write("    albedoColor: " + mat.color.to_string() + "\n")
            f.write("    albedoTexture: " + uuid + "\n")
    
    def load_mat(self, file):
        with open(os.path.join(self.path, file.path)) as f:
            lines = f.read().rstrip().splitlines()
        
        lines.pop(0)
        
        data = {}
        for line in lines:
            name, value = line[4:].split(": ")
            data[name] = value
        
        color = Color.from_string(data["albedoColor"])
        material = Material(color)
        if "albedoTexture" in data and data["albedoTexture"] != "None":
            uuid = data["albedoTexture"]
            if self.files[uuid].obj != "None":
                self.files[uuid].obj = Texture2D(os.path.join(self.path, self.files[uuid].path))
            material.texture = self.files[uuid].obj
        return material
