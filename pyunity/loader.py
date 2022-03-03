"""
Utility functions related to loading
and saving PyUnity meshes and scenes.

This will be imported as ``pyunity.Loader``.

"""

__all__ = ["Primitives", "GetImports", "SaveScene",
           "LoadMesh", "SaveMesh", "LoadObj", "SaveObj"]

from .meshes import Mesh
from .errors import *
from .core import *
from .values import *
from .scenes import SceneManager
from .files import Behaviour, Scripts, Project, File, Texture2D
from .render import Camera
from .audio import AudioSource, AudioListener, AudioClip
from .physics import BoxCollider, SphereCollider, Rigidbody  # , PhysicMaterial
from .scenes import Scene
from uuid import uuid4
import inspect
import json
import enum
import os
import shutil

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

def SaveObj(mesh, name, filePath=None):
    if filePath:
        directory = os.path.dirname(os.path.abspath(filePath))
    else:
        directory = os.getcwd()
    os.makedirs(directory, exist_ok=True)

    with open(os.path.join(directory, name + ".obj"), "w+") as f:
        for vertex in mesh.verts:
            f.write(f"v {' '.join(map(str, round(vertex, 8)))}\n")
        for normal in mesh.normals:
            f.write(f"vn {' '.join(map(str, round(normal, 8)))}\n")
        for face in mesh.triangles:
            face = " ".join([f"{x + 1}//{x + 1}" for x in face])
            f.write(f"f {face}\n")

def LoadMesh(filename):
    """
    Loads a .mesh file generated by
    `SaveMesh`. It is optimized for faster
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
    texcoords = list(map(float, lines[3].split("/")))
    texcoords = [
        [texcoords[i], texcoords[i + 1]] for i in range(0, len(texcoords), 2)
    ]
    return Mesh(vertices, faces, normals, texcoords)

def SaveMesh(mesh, name, filePath=None):
    """
    Saves a mesh to a .mesh file
    for faster loading.

    Parameters
    ----------
    mesh : Mesh
        Mesh to save
    name : str
        Name of the mesh
    filePath : str, optional
        Pass in `__file__` to save in
        directory of script, otherwise
        pass in the path of where you
        want to save the file. For example, if you
        want to save in C:\Downloads, then give
        "C:\Downloads\mesh.mesh". If not
        specified, then the mesh is saved
        in the cwd.

    """
    if filePath:
        directory = os.path.dirname(os.path.abspath(filePath))
    else:
        directory = os.getcwd()
    os.makedirs(directory, exist_ok=True)

    with open(os.path.join(directory, name + ".mesh"), "w+") as f:
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
    _names = ["cube", "quad", "double_quad", "sphere", "capsule", "cylinder"]
    _path = os.path.dirname(os.path.abspath(__file__))
    cube = LoadMesh(os.path.join(_path, "primitives/cube.mesh"))
    quad = LoadMesh(os.path.join(_path, "primitives/quad.mesh"))
    double_quad = LoadMesh(os.path.join(_path, "primitives/double_quad.mesh"))
    sphere = LoadMesh(os.path.join(_path, "primitives/sphere.mesh"))
    capsule = LoadMesh(os.path.join(_path, "primitives/capsule.mesh"))
    cylinder = LoadMesh(os.path.join(_path, "primitives/cylinder.mesh"))

def GetImports(file):
    with open(file) as f:
        lines = f.read().rstrip().splitlines()
    imports = []
    for line in lines:
        line = line.lstrip()
        if line.startswith("import") or (line.startswith("from") and " import " in line):
            imports.append(line)
    return "\n".join(imports) + "\n\n"

componentMap = {
    "Transform": Transform,
    "Camera": Camera,
    "Light": Light,
    "MeshRenderer": MeshRenderer,
    "BoxCollider": BoxCollider,
    "SphereCollider": SphereCollider,
    "Rigidbody": Rigidbody,
    "AudioSource": AudioSource,
    "AudioListener": AudioListener
}
"""List of all components by name"""

def parseString(string):
    if string.startswith("Vector3("):
        return True, Vector3(*list(map(float, string[8:-1].split(", "))))
    if string.startswith("Quaternion("):
        return True, Quaternion(*list(map(float, string[11:-1].split(", "))))
    if string.startswith("RGB("):
        return True, RGB(*list(map(float, string[4:-1].split(", "))))
    if string.startswith("HSV("):
        return True, HSV(*list(map(float, string[4:-1].split(", "))))
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
        return True, json.loads(string)
    except json.decoder.JSONDecodeError:
        pass
    if string.startswith("(") and string.endswith(")"):
        check, items = zip(*list(map(parseString, string.split(", "))))
        if all(check):
            return True, tuple(items)
    if string.startswith("[") and string.endswith("]"):
        check, items = zip(*list(map(parseString, string[1:-1].split(", "))))
        if all(check):
            return True, list(items)
    return False, None

class ObjectInfo:
    def __init__(self, name, uuid, attrs):
        self.name = name
        self.uuid = uuid
        self.attrs = attrs
    
    def __str__(self):
        s = f"{self.name} : {self.uuid}"
        for k, v in self.attrs.items():
            s += f"\n    {k}: {v}"
        return s

def gen_uuid():
    return str(uuid4())

def SaveMat(material, project, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    if material.texture is None:
        texID = "None"
    else:
        if material.texture not in project._ids:
            texID = str(uuid4())
            project._ids[material.texture] = texID
            project._idMap[texID] = material.texture

            name = os.path.splitext(os.path.basename(filename))[0]
            path = os.path.join(project.path, "Textures", name + ".png")
            file = File(path, texID)
            project.ImportFile(file, write=False)
            material.texture.img.save(path)
        else:
            texID = project._ids[material.texture]
    
    colStr = str(material.color)

    with open(filename, "w+") as f:
        f.write(f"Material\n    texture: {texID}\n    color: {colStr}")

def LoadMat(path, project):
    if not os.path.isfile(path):
        raise PyUnityException(f"The specified file does not exist: {path}")
    
    with open(path) as f:
        contents = f.read().rstrip().splitlines()
    
    if contents.pop(0) != "Material":
        raise ProjectParseException("Expected \"Material\" as line 1")
    
    parts = {split[0][4:]: split[1] for split in map(lambda x: x.split(": "), contents)}

    if not (parts["color"].startswith("RGB") or parts["color"].startswith("HSV")):
        raise ProjectParseException("Color value does not start with RGB or HSV")
    
    color = Color.from_string(parts["color"])

    if parts["texture"] not in project._idMap and parts["texture"] != "None":
        raise ProjectParseException(f"Project file UUID not found: {parts['texture']}")
    
    if parts["texture"] == "None":
        texture = None
    else:
        texture = project._idMap[parts["texture"]]

    return Material(color, texture)

def SaveScene(scene, project, path):
    def get_uuid(obj):
        if obj is None:
            return None
        if obj in project._ids:
            return project._ids[obj]
        uuid = str(uuid4())
        project._ids[obj] = uuid
        project._idMap[uuid] = obj
        return project._ids[obj]
    
    location = os.path.join(project.path, path, scene.name + ".scene")
    data = [ObjectInfo("Scene", get_uuid(scene), {"name": json.dumps(scene.name), "mainCamera": get_uuid(scene.mainCamera)})]

    for gameObject in scene.gameObjects:
        attrs = {"name": json.dumps(gameObject.name),
                 "tag": gameObject.tag.tag,
                 "transform": get_uuid(gameObject.transform)}
        data.append(ObjectInfo("GameObject", get_uuid(gameObject), attrs))
    
    for gameObject in scene.gameObjects:
        gameObjectID = get_uuid(gameObject)
        for component in gameObject.components:
            attrs = {"gameObject": gameObjectID}
            for k in component.saved.keys():
                v = getattr(component, k)
                if isinstance(v, (GameObject, Component, Scene)):
                    v = get_uuid(v)
                elif isinstance(v, Mesh):
                    filename = os.path.join("Meshes", gameObject.name + ".mesh")
                    SaveMesh(v, gameObject.name, os.path.join(project.path, filename))
                    v = get_uuid(v)
                    file = File(filename, v)
                    project.ImportFile(file, write=False)
                elif isinstance(v, Material):
                    filename = os.path.join("Materials", gameObject.name + ".mat")
                    SaveMat(v, project, os.path.join(project.path, filename))
                    v = get_uuid(v)
                    file = File(filename, v)
                    project.ImportFile(file, write=False)
                elif isinstance(v, Texture2D):
                    filename = os.path.join("Textures", gameObject.name + ".png")
                    os.makedirs(os.path.join(project.path, "Textures"), exist_ok=True)
                    v.img.save(os.path.join(project.path, filename))
                    v = get_uuid(v)
                    file = File(filename, v)
                    project.ImportFile(file, write=False)
                attrs[k] = v
            if isinstance(component, Behaviour):
                behaviour = component.__class__
                uuid = get_uuid(behaviour)
                attrs["_script"] = uuid
                name = behaviour.__name__ + "(Behaviour)"

                filename = os.path.join("Scripts", behaviour.__name__ + ".py")
                os.makedirs(os.path.join(project.path, "Scripts"), exist_ok=True)
                with open(os.path.join(project.path, filename), "w+") as f:
                    f.write(GetImports(inspect.getsourcefile(behaviour)) + \
                            inspect.getsource(behaviour))

                file = File(filename, uuid)
                project.ImportFile(file, write=False)
            else:
                name = component.__class__.__name__ + "(Component)"
            data.append(ObjectInfo(name, get_uuid(component), attrs))

    os.makedirs(os.path.dirname(location), exist_ok=True)
    with open(location, "w+") as f:
        f.write("\n".join(map(str, data)))
    project.ImportFile(File(os.path.join(path, scene.name + ".scene"), get_uuid(scene)))
    project.Write()

def ResaveScene(scene, project):
    if scene not in project._ids:
        raise PyUnityException(f"Scene is not part of project: {scene.name!r}")
    
    path = project.fileIDs[project._ids[scene]]
    SaveScene(scene, project, path)

def GenerateProject(name):
    project = Project(name)
    SaveProject(project)
    return project

def SaveProject(project):
    for scene in SceneManager.scenesByIndex:
        SaveScene(scene, project, "Scenes")

def LoadProject(folder):
    project = Project.FromFolder(folder)

    # Scripts
    for file in project.filePaths:
        if file.endswith(".py") and not file.startswith("__"):
            Scripts.LoadScript(os.path.join(project.path, os.path.normpath(file)))
    
    # Meshes
    for file in project.filePaths:
        if file.endswith(".mesh"):
            mesh = LoadMesh(os.path.join(project.path, os.path.normpath(file)))
            uuid = project.filePaths[file].uuid
            project._idMap[uuid] = mesh

    # Textures
    for file in project.filePaths:
        if file.endswith(".png") or file.endswith(".jpg"):
            texture = Texture2D(os.path.join(project.path, os.path.normpath(file)))
            uuid = project.filePaths[file].uuid
            project._idMap[uuid] = texture
    
    # Materials
    for file in project.filePaths:
        if file.endswith(".mat"):
            material = LoadMat(os.path.join(project.path, os.path.normpath(file)), project)
            uuid = project.filePaths[file].uuid
            project._idMap[uuid] = material

    # Scenes
    for file in project.filePaths:
        if file.endswith(".scene"):
            LoadScene(os.path.join(project.path, os.path.normpath(file)), project)
    
    return project

def LoadScene(sceneFile, project):
    try:
        import PyUnityScripts
    except ImportError:
        raise PyUnityException("Please run Scripts.LoadScript before this function")

    def add_uuid(obj, uuid):
        if obj in project._ids:
            return
        project._ids[obj] = uuid
        project._idMap[uuid] = obj
    
    if not os.path.isfile(sceneFile):
        raise PyUnityException(f"The specified file does not exist: {sceneFile}")

    with open(sceneFile) as f:
        contents = f.read().rstrip().splitlines()
    
    data = []
    attrs = {}
    name, uuid = contents.pop(0).split(" : ")
    for line in contents:
        if line.startswith("    "):
            key, value = line[4:].split(": ")
            attrs[key] = value
        elif name == "" or uuid == "":
            raise ProjectParseException(f"Section header before data")
        else:
            data.append(ObjectInfo(name, uuid, attrs))
            name, uuid = line.split(" : ")
            attrs = {}
    
    # Final objectinfo
    data.append(ObjectInfo(name, uuid, attrs))
    
    sceneInfo = data.pop(0)
    if sceneInfo.name != "Scene":
        raise ProjectParseException(f"Expected \"Scene\" as first section")
    
    gameObjectInfo = [x for x in data if x.name == "GameObject"]
    componentInfo = [x for x in data if x.name.endswith("(Component)")]
    behaviourInfo = [x for x in data if x.name.endswith("(Behaviour)")]

    gameObjects = []
    scene = SceneManager.AddBareScene(json.loads(sceneInfo.attrs["name"]))
    add_uuid(scene, sceneInfo.uuid)
    for part in gameObjectInfo:
        gameObject = GameObject.BareObject(json.loads(part.attrs["name"]))
        add_uuid(gameObject, part.uuid)
        gameObjects.append(gameObject)
    
    # first pass, adding components
    for part in componentInfo + behaviourInfo:
        gameObjectID = part.attrs.pop("gameObject")
        gameObject = project._idMap[gameObjectID]

        if part.name.endswith("(Component)"):
            component = gameObject.AddComponent(componentMap[part.name[:-11]])
        else:
            file = project.fileIDs[part.attrs.pop("_script")]
            fullpath = os.path.join(os.path.abspath(project.path), file.path)
            behaviourType = PyUnityScripts._lookup[fullpath]
            component = gameObject.AddComponent(behaviourType)
            if part.name[:-11] != behaviourType.__name__:
                raise PyUnityException(f"{behaviourType.__name__} does not match {part.name[:-11]}")
        
        add_uuid(component, part.uuid)
    
    # second part, assigning attrs
    for part in componentInfo + behaviourInfo:
        component = project._idMap[part.uuid]
        for k, v in part.attrs.items():
            if v in project._idMap:
                value = project._idMap[v]
            else:
                success, value = parseString(v)
                if not success:
                    continue
            if value is not None:
                type_ = type(component).saved[k].type
                if type_ is float:
                    type_ = (float, int)
                elif issubclass(type_, enum.Enum):
                    if value in list(type_.__members__.values()):
                        value = type_(value)
                    else:
                        raise ProjectParseException(f"{value} not in enum {type_}")
                if not isinstance(value, type_):
                    raise ProjectParseException(f"Value does not match type: {(value, type_)!r}")
            setattr(component, k, value)
    
    scene.mainCamera = project._idMap[sceneInfo.attrs["mainCamera"]]
    for gameObject in gameObjects:
        scene.Add(gameObject)
    return scene


