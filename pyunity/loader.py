# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

"""
Utility functions related to loading
and saving PyUnity meshes and scenes.

This will be imported as ``pyunity.Loader``.

"""

__all__ = ["Primitives", "GetImports", "SaveScene",
           "LoadMesh", "SaveMesh", "LoadObj", "SaveObj",
           "LoadMat", "SaveMat", "LoadProject", "ObjectInfo",
           "SaveProject", "ResaveScene", "GenerateProject",
           "LoadScene", "LoadStl", "LoadPrefab",
           "LoadObjectInfos", "LoadGameObjects",
           "SaveGameObjects", "SavePrefab"]

from . import Logger
from .meshes import Mesh, Material, Color
from .errors import PyUnityException, ProjectParseException
from .core import GameObject, Component, Tag, SavesProjectID
from .values import Vector3, Vector2, ImmutableStruct, Quaternion, SavableStruct
from .scenes import SceneManager, Scene
from .files import Behaviour, Scripts, Project, File, Texture2D, Asset, Prefab
from .resources import getPath
from pathlib import Path
from uuid import uuid4
import struct
import inspect
import json
import enum
import os

def LoadObj(filename):
    """
    Loads a .obj file to a PyUnity mesh.

    Parameters
    ----------
    filename : str
        Name of file

    Returns
    -------
    Mesh
        A mesh of the object file

    """
    vertices = []
    normals = []
    faces = []

    for line in open(filename, "r"):
        if line.startswith("#"):
            continue
        values = line.split()
        if not values:
            continue
        if values[0] == "v":
            v = Vector3(float(values[1]), float(values[3]), float(values[2]))
            vertices.append(v)
        elif values[0] == "f":
            face = []
            for v in values[1:]:
                w = v.split("/")
                face.append(int(w[0]) - 1)
            face.reverse()
            faces.append(face)

    for face in faces:
        a = vertices[face[2]] - vertices[face[1]]
        b = vertices[face[0]] - vertices[face[1]]
        normal = a.cross(b).normalized()
        normals.append(normal)

    return Mesh(vertices, faces, normals)

def SaveObj(mesh, path):
    directory = Path(path).resolve().parent
    directory.mkdir(parents=True, exist_ok=True)

    with open(path, "w+") as f:
        for vertex in mesh.verts:
            f.write(f"v {' '.join(map(str, round(vertex, 8)))}\n")
        for normal in mesh.normals:
            f.write(f"vn {' '.join(map(str, round(normal, 8)))}\n")
        for face in mesh.triangles:
            face = " ".join([f"{x + 1}//{x + 1}" for x in face])
            f.write(f"f {face}\n")

def LoadStl(filename):
    def vectorFromBytes(b):
        x, y, z = b[:4], b[4:8], b[8:]
        l = [struct.unpack("<f", a)[0] for a in [x, y, z]]
        # Flip Z and Y axes
        # Reverse Z axis
        return Vector3(l[0], l[2], -l[1])

    def vectorFromStr(s):
        l = list(map(float, s.split(" ")[-3:]))
        # Flip Z and Y axes
        # Reverse Z axis
        return Vector3(l[0], l[2], -l[1])

    faces = []
    vertices = []
    normals = []

    with open(filename, "rb") as f:
        binary = f.read()

    if binary[:5] == b"solid":
        # Ascii format
        text = "\n".join(binary.decode().rstrip().split("\n")[1:-1])
        sections = text.split("\n    endloop\nendfacet\nfacet ")
        if not sections[0].startswith("facet normal "):
            raise PyUnityException(
                "File does not start with \"facet normal\"")
        sections[0] = sections[0][:-len("facet normal ")]
        if not sections[-1].endswith("\n    endloop\nendfacet"):
            raise PyUnityException(
                "File does not end with \"endfacet\"")
        sections[-1] = sections[-1][:-len("\n    endloop\nendfacet")]

        i = 0
        for section in sections:
            lines = section.split("\n")
            normal = vectorFromStr(lines[0].split(" ")[-3:])
            a = vectorFromStr(lines[2].split(" ")[-3:])
            b = vectorFromStr(lines[3].split(" ")[-3:])
            c = vectorFromStr(lines[4].split(" ")[-3:])
            faces.append([i, i + 1, i + 2])
            vertices.extend([a, b, c])
            normals.extend([normal.copy(), normal.copy(), normal.copy()])
            i += 3
        return Mesh(vertices, faces, normals)
    else:
        # Binary format
        length = int.from_bytes(binary[80:84], byteorder="little")
        realLength = (len(binary) - 84) // 50
        if length != realLength:
            raise PyUnityException(
                f"STL length does not match real length: "
                f"expected {realLength}, got {length}")

        for i in range(length):
            section = binary[84 + i * 50: 134 + i * 50]
            normal = vectorFromBytes(section[:12])
            a = vectorFromBytes(section[12:24])
            b = vectorFromBytes(section[24:36])
            c = vectorFromBytes(section[36:48])
            faces.append([i * 3, i * 3 + 1, i * 3 + 2])
            vertices.extend([a, b, c])
            normals.extend([normal.copy(), normal.copy(), normal.copy()])
        return Mesh(vertices, faces, normals)

def LoadMesh(filename):
    """
    Loads a .mesh file generated by
    :func:`SaveMesh`. It is optimized for faster
    loading.

    Parameters
    ----------
    filename : str
        Name of file relative to the cwd

    Returns
    -------
    Mesh
        Generated mesh

    """
    with open(filename, "r") as f:
        lines = list(map(str.rstrip, f.read().rstrip().splitlines()))

    vertices = list(map(float, lines[0].split("/")))
    vertices = [
        Vector3(vertices[i], vertices[i + 1], vertices[i + 2]) for i in range(0, len(vertices), 3)
    ]
    faces = list(map(int, lines[1].split("/")))
    faces = [
        [faces[i], faces[i + 1], faces[i + 2]] for i in range(0, len(faces), 3)
    ]
    normals = list(map(float, lines[2].split("/")))
    normals = [
        Vector3(normals[i], normals[i + 1], normals[i + 2]) for i in range(0, len(normals), 3)
    ]
    if len(lines) > 3:
        texcoords = list(map(float, lines[3].split("/")))
        texcoords = [
            [texcoords[i], texcoords[i + 1]] for i in range(0, len(texcoords), 2)
        ]
    else:
        texcoords = None
    return Mesh(vertices, faces, normals, texcoords)

def SaveMesh(mesh, path):
    """
    Saves a mesh to a .mesh file
    for faster loading.

    Parameters
    ----------
    mesh : Mesh
        Mesh to save
    path : str or Path
        Path to save file

    """
    directory = Path(path).resolve().parent
    directory.mkdir(parents=True, exist_ok=True)

    with open(path, "w+") as f:
        i = 0
        for vertex in mesh.verts:
            i += 1
            f.write(str(round(vertex.x, 8)) + "/")
            f.write(str(round(vertex.y, 8)) + "/")
            f.write(str(round(vertex.z, 8)))
            if i != len(mesh.verts):
                f.write("/")
        f.write("\n")

        i = 0
        for triangle in mesh.triangles:
            i += 1
            j = 0
            for item in triangle:
                j += 1
                f.write(str(item))
                if i != len(mesh.triangles) or j != 3:
                    f.write("/")
        f.write("\n")

        i = 0
        for normal in mesh.normals:
            i += 1
            f.write(str(round(normal.x, 8)) + "/")
            f.write(str(round(normal.y, 8)) + "/")
            f.write(str(round(normal.z, 8)))
            if i != len(mesh.normals):
                f.write("/")
        f.write("\n")

        i = 0
        for texcoord in mesh.texcoords:
            i += 1
            f.write(str(texcoord[0]) + "/")
            f.write(str(texcoord[1]))
            if i != len(mesh.texcoords):
                f.write("/")
        f.write("\n")

class Primitives(metaclass=ImmutableStruct):
    """
    Primitive preloaded meshes.
    Do not instantiate this class.

    """
    _names = ["cube", "quad", "doubleQuad", "sphere", "capsule", "cylinder"]
    cube = LoadMesh(getPath("primitives/cube.mesh"))
    quad = LoadMesh(getPath("primitives/quad.mesh"))
    doubleQuad = LoadMesh(getPath("primitives/doubleQuad.mesh"))
    sphere = LoadMesh(getPath("primitives/sphere.mesh"))
    capsule = LoadMesh(getPath("primitives/capsule.mesh"))
    cylinder = LoadMesh(getPath("primitives/cylinder.mesh"))

def GetImports(file):
    with open(file) as f:
        lines = f.read().rstrip().splitlines()
    imports = []
    for line in lines:
        line = line.lstrip()
        if line.startswith("import") or (line.startswith("from") and " import " in line):
            imports.append(line)
    return "\n".join(imports) + "\n\n"

def parseString(string, project=None):
    if project is not None and string in project._idMap:
        return True, project._idMap[string]
    if string.startswith("Vector2("):
        return True, Vector2(*list(map(float, string[8:-1].split(", "))))
    if string.startswith("Vector3("):
        return True, Vector3(*list(map(float, string[8:-1].split(", "))))
    if string.startswith("Quaternion("):
        return True, Quaternion(*list(map(float, string[11:-1].split(", "))))
    if string.startswith("RGB(") or string.startswith("HSV("):
        return True, Color.fromString(string)
    if "\n" in string:
        struct = {}
        check = True
        for line in string.split("\n"):
            key, value = line.split(": ")
            valid, value = parseString(value, project)
            if not valid:
                check = False
                break
            struct[key] = value
        if check:
            return True, struct
    if string in ["True", "False"]:
        return True, string == "True"
    if string == "None":
        return True, None
    if string.isdigit():
        return True, int(string)
    try:
        return True, float(string)
    except (ValueError, OverflowError):
        pass
    try:
        # Only want strings here
        outStr = json.loads(string)
        if not isinstance(outStr, str):
            raise ValueError
        return True, outStr
    except ValueError:
        pass
    if ((string.startswith("(") and string.endswith(")")) or
            (string.startswith("[") and string.endswith("]"))):
        check = []
        items = []
        if len(string) > 2:
            for section in string[1:-1].split(", "):
                if section.isspace() or section == "":
                    continue
                valid, obj = parseString(section.rstrip().lstrip(), project)
                check.append(valid)
                items.append(obj)
        if all(check):
            if string.startswith("("):
                return True, tuple(items)
            return True, items
    return False, None

def parseStringFallback(string, project, fallback):
    success, value = parseString(string, project)
    if not success:
        return fallback
    return value

class ObjectInfo:
    class SkipConv:
        def __init__(self, value):
            self.value = value

    def __init__(self, name, uuid, attrs):
        self.name = name
        self.uuid = uuid
        self.attrs = attrs

    @staticmethod
    def convString(v):
        if isinstance(v, str):
            return json.dumps(v)
        elif isinstance(v, enum.Enum):
            return str(v.value)
        else:
            return str(v)

    def __str__(self):
        s = f"{self.name} : {self.uuid}"
        for k, v in self.attrs.items():
            if isinstance(v, ObjectInfo.SkipConv):
                string = v.value
                if string.startswith("\n"):
                    s += f"\n    {k}:{string}"
                else:
                    s += f"\n    {k}: {string}"
            else:
                string = ObjectInfo.convString(v)
                s += f"\n    {k}: {string}"
        return s

def SaveMat(material, project, filename):
    Path(filename).parent.mkdir(parents=True, exist_ok=True)

    if material.texture is None:
        texID = "None"
    else:
        texID = project._ids[material.texture]

    colStr = str(material.color)

    with open(filename, "w+") as f:
        f.write(f"Material\n    texture: {texID}\n    color: {colStr}")

def LoadMat(path, project):
    if not Path(path).is_file():
        raise PyUnityException(f"The specified file does not exist: {path}")

    with open(path) as f:
        contents = f.read().rstrip().splitlines()

    if contents.pop(0) != "Material":
        raise ProjectParseException("Expected \"Material\" as line 1")

    parts = {split[0][4:]: split[1] for split in map(lambda x: x.split(": "), contents)}

    if not (parts["color"].startswith("RGB") or parts["color"].startswith("HSV")):
        raise ProjectParseException("Color value does not start with RGB or HSV")

    color = Color.fromString(parts["color"])

    if parts["texture"] not in project._idMap and parts["texture"] != "None":
        raise ProjectParseException(f"Project file UUID not found: {parts['texture']}")

    if parts["texture"] == "None":
        texture = None
    else:
        texture = project._idMap[parts["texture"]]

    return Material(color, texture)

def SavePrefab(prefab, path, project):
    filename = Path(path)
    filename.parent.mkdir(parents=True, exist_ok=True)

    data = []
    SaveGameObjects(prefab.gameObjects, data, project)

    with open(filename, "w+") as f:
        f.write("\n".join(map(str, data)))

def LoadPrefab(path, project):
    data = LoadObjectInfos(path)
    gameObjects = LoadGameObjects(data, project)
    g = gameObjects[0]
    while g.transform.parent is not None:
        g = g.transform.parent.gameObject

    prefab = Prefab(g, prune=False)
    return prefab

savable = (
    Color, Vector3, Quaternion, # PyUnity types
    bool, int, str, float, list, tuple, # Python types
    SavesProjectID, ObjectInfo.SkipConv # Special procedures
)
"""All savable types that will not be saved as UUIDs"""

def SaveGameObjects(gameObjects, data, project):
    def getUuid(obj):
        if obj is None:
            return None
        if obj in project._ids:
            return project._ids[obj]
        uuid = str(uuid4())
        project._ids[obj] = uuid
        project._idMap[uuid] = obj
        return project._ids[obj]

    for gameObject in gameObjects:
        attrs = {
            "name": gameObject.name,
            "tag": gameObject.tag.tag,
            "enabled": gameObject.enabled,
            "transform": ObjectInfo.SkipConv(getUuid(gameObject.transform))
        }
        data.append(ObjectInfo("GameObject", getUuid(gameObject), attrs))

    for gameObject in gameObjects:
        gameObjectID = getUuid(gameObject)
        for component in gameObject.components:
            attrs = {
                "gameObject": ObjectInfo.SkipConv(gameObjectID),
                "enabled": gameObject.enabled
            }
            for k in component._saved.keys():
                v = getattr(component, k)
                if isinstance(v, SavesProjectID):
                    if v not in project._ids and isinstance(v, Asset):
                        project.ImportAsset(v, gameObject)
                    v = ObjectInfo.SkipConv(getUuid(v))
                elif hasattr(v, "_wrapper"):
                    if isinstance(getattr(v, "_wrapper"), SavableStruct):
                        wrapper = getattr(v, "_wrapper")
                        struct = {}
                        for key in wrapper.attrs:
                            if hasattr(v, key):
                                item = getattr(v, key)
                                if isinstance(item, SavesProjectID):
                                    if item not in project._ids and isinstance(item, Asset):
                                        project.ImportAsset(item, gameObject)
                                    struct[key] = getUuid(item)
                                else:
                                    struct[key] = ObjectInfo.convString(item)
                        sep = "\n        "
                        v = ObjectInfo.SkipConv(
                            sep + sep.join(": ".join(x) for x in struct.items()))
                if v is not None and not isinstance(v, savable):
                    continue
                attrs[k] = v
            if isinstance(component, Behaviour):
                behaviour = component.__class__
                if behaviour not in project._ids:
                    filename = Path("Scripts") / (behaviour.__name__ + ".py")
                    os.makedirs(project.path / "Scripts", exist_ok=True)
                    with open(project.path / filename, "w+") as f:
                        f.write(GetImports(inspect.getsourcefile(behaviour)) +
                                inspect.getsource(behaviour))

                    uuid = getUuid(behaviour)
                    file = File(filename, uuid)
                    project.ImportFile(file, write=False)

                attrs["_script"] = ObjectInfo.SkipConv(project._ids[behaviour])
                name = behaviour.__name__ + "(Behaviour)"
            else:
                name = component.__class__.__name__ + "(Component)"
            data.append(ObjectInfo(name, getUuid(component), attrs))

def LoadObjectInfos(file):
    with open(file) as f:
        contents = f.read().rstrip().splitlines()

    data = []
    attrs = {}
    struct = {}
    name, uuid = contents.pop(0).split(" : ")
    for line in contents:
        if "#" in line:
            quotes = 0
            for i, char in enumerate(line):
                if char == "\"" and line[char - 1] != "\\":
                    quotes += 1
                if char == "#":
                    if quotes % 2 == 0:
                        break
            line = line[:i]
        line = line.rstrip()
        if line == "":
            continue
        if line.startswith("        "):
            key, value = line[8:].split(": ")
            struct[key] = value
        elif line.startswith("    "):
            if line.endswith(":"):
                key = line[4:-1]
                struct = {}
                attrs[key] = struct
            else:
                key, value = line[4:].split(": ")
                attrs[key] = value
        else:
            # New section
            for key in attrs:
                if isinstance(attrs[key], dict):
                    text = "\n".join(": ".join(x) for x in attrs[key].items())
                    attrs[key] = text
            data.append(ObjectInfo(name, uuid, attrs))
            name, uuid = line.split(" : ")
            attrs = {}

    # Final objectinfo
    for key in attrs:
        if isinstance(attrs[key], dict):
            text = "\n".join(": ".join(x) for x in attrs[key].items())
            attrs[key] = text
    data.append(ObjectInfo(name, uuid, attrs))
    return data

def instanceCheck(type_, value):
    if type_ is float:
        type_ = (float, int)
    elif issubclass(type_, enum.Enum):
        if value in list(type_.__members__.values()):
            value = type_(value)
        else:
            raise ProjectParseException(f"{value} not in enum {type_}")
    return type_, value

def LoadGameObjects(data, project):
    def addUuid(obj, uuid):
        if obj in project._ids:
            return
        project._ids[obj] = uuid
        project._idMap[uuid] = obj

    try:
        import PyUnityScripts
    except ImportError:
        raise PyUnityException("Please run Scripts.LoadScript before this function")

    gameObjectInfo = [x for x in data if x.name == "GameObject"]
    componentInfo = [x for x in data if x.name.endswith("(Component)")]
    behaviourInfo = [x for x in data if x.name.endswith("(Behaviour)")]

    gameObjects = []
    for part in gameObjectInfo:
        gameObject = GameObject.BareObject(json.loads(part.attrs["name"]))
        gameObject.tag = Tag(int(part.attrs["tag"]))
        gameObject.enabled = part.attrs.get("enabled", "True") == "True"
        addUuid(gameObject, part.uuid)
        gameObjects.append(gameObject)

    import pyunity
    componentMap = {}
    for item in pyunity.__all__:
        obj = getattr(pyunity, item)
        if isinstance(obj, type) and issubclass(obj, Component):
            componentMap[item] = obj

    # first pass, adding components
    for part in componentInfo + behaviourInfo:
        gameObjectID = part.attrs.pop("gameObject")
        gameObject = project._idMap[gameObjectID]
        enabled = part.attrs.pop("enabled", "True") == "True"

        if part.name.endswith("(Component)"):
            component = gameObject.AddComponent(componentMap[part.name[:-11]])
        else:
            file = project.fileIDs[part.attrs.pop("_script")]
            fullpath = project.path.resolve() / file.path
            behaviourType = PyUnityScripts._lookup[str(fullpath)]
            addUuid(behaviourType, file.uuid)
            component = gameObject.AddComponent(behaviourType)
            if part.name[:-11] != behaviourType.__name__:
                raise PyUnityException(f"{behaviourType.__name__} does not match {part.name[:-11]}")
        component.enabled = enabled

        addUuid(component, part.uuid)

    # second part, assigning attrs
    for part in componentInfo + behaviourInfo:
        component = project._idMap[part.uuid]
        for k, v in part.attrs.items():
            success, value = parseString(v, project)
            if not success:
                continue
            if value is not None:
                type_, value = instanceCheck(component._saved[k].type, value)
                if hasattr(type_, "_wrapper"):
                    if isinstance(getattr(type_, "_wrapper"), SavableStruct):
                        value = getattr(type_, "_wrapper").fromDict(type_, value, instanceCheck)
                if not isinstance(value, type_):
                    raise ProjectParseException(
                        f"Value {value!r} does not match type {type_}: "
                        f"attribute {k!r} of {component}")
            setattr(component, k, value)

    # Transform check
    for part in gameObjectInfo:
        gameObject = project._idMap[part.uuid]
        transform = project._idMap[part.attrs["transform"]]
        if transform is not gameObject.transform:
            Logger.LogLine(Logger.WARN, f"GameObject transform does not match transform UUID: {gameObject.name!r}")
        if transform.parent is not None:
            transform.parent.children.append(transform)

    return gameObjects

def SaveScene(scene, project, path):
    def getUuid(obj):
        if obj is None:
            return None
        if obj in project._ids:
            return project._ids[obj]
        uuid = str(uuid4())
        project._ids[obj] = uuid
        project._idMap[uuid] = obj
        return project._ids[obj]

    location = project.path / path
    data = [ObjectInfo(
        "Scene",
        getUuid(scene),
        {
            "name": scene.name,
            "mainCamera": ObjectInfo.SkipConv(getUuid(scene.mainCamera))
        }
    )]

    SaveGameObjects(scene.gameObjects, data, project)

    location.parent.mkdir(parents=True, exist_ok=True)
    with open(location, "w+") as f:
        f.write("\n".join(map(str, data)))
    project.ImportFile(File(Path(path), getUuid(scene)))

savers = {
    Mesh: SaveMesh,
    Material: SaveMat,
    Scene: SaveScene,
    Prefab: SavePrefab,
}

def ResaveScene(scene, project):
    if scene not in project._ids:
        raise PyUnityException(f"Scene is not part of project: {scene.name!r}")

    path = project.fileIDs[project._ids[scene]].path
    SaveScene(scene, project, Path(path).parent)

def GenerateProject(name):
    project = Project(name)
    SaveProject(project)
    return project

def SaveProject(project):
    for scene in SceneManager.scenesByIndex:
        project.ImportAsset(scene)

def LoadProject(folder, remove=True):
    if remove:
        SceneManager.RemoveAllScenes()

    project = Project.FromFolder(folder)

    Scripts.GenerateModule()
    # Scripts
    for file in project.filePaths:
        if file.endswith(".py") and not file.startswith("__"):
            Scripts.LoadScript(project.path / os.path.normpath(file))

    # Meshes
    for file in project.filePaths:
        if file.endswith(".mesh"):
            mesh = LoadMesh(project.path / os.path.normpath(file))
            project.SetAsset(file, mesh)

    # Textures
    for file in project.filePaths:
        if file.endswith(".png") or file.endswith(".jpg"):
            texture = Texture2D(project.path / os.path.normpath(file))
            project.SetAsset(file, texture)

    # Materials
    for file in project.filePaths:
        if file.endswith(".mat"):
            material = LoadMat(project.path / os.path.normpath(file), project)
            project.SetAsset(file, material)

    # Prefabs
    for file in project.filePaths:
        if file.endswith(".prefab"):
            prefab = LoadPrefab(project.path / os.path.normpath(file), project)
            project.SetAsset(file, prefab)

    # Scenes
    for file in project.filePaths:
        if file.endswith(".scene"):
            LoadScene(project.path / os.path.normpath(file), project)

    return project

def LoadScene(sceneFile, project):
    def addUuid(obj, uuid):
        if obj in project._ids:
            return
        project._ids[obj] = uuid
        project._idMap[uuid] = obj

    if not Path(sceneFile).is_file():
        raise PyUnityException(f"The specified file does not exist: {sceneFile}")

    data = LoadObjectInfos(sceneFile)
    gameObjects = LoadGameObjects(data[1:], project)

    sceneInfo = data[0]
    if sceneInfo.name != "Scene":
        raise ProjectParseException(f"Expected \"Scene\" as first section")

    scene = SceneManager.AddBareScene(json.loads(sceneInfo.attrs["name"]))
    addUuid(scene, sceneInfo.uuid)
    scene.mainCamera = project._idMap[sceneInfo.attrs["mainCamera"]]
    for gameObject in gameObjects:
        scene.Add(gameObject)
    return scene
