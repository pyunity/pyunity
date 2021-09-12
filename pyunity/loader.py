"""
Utility functions related to loading
and saving PyUnity meshes and scenes.

This will be imported as ``pyunity.Loader``.

"""

from .meshes import Mesh
from .core import *
from .values import Material, Vector3, Quaternion
from .scenes import SceneManager
from .files import Behaviour, Project, Scripts
from .render import Camera
from .audio import AudioSource, AudioListener, AudioClip
from .physics import AABBoxCollider, SphereCollider, Rigidbody  # , PhysicMaterial
from uuid import uuid4
import inspect
import json
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
            f.write("v " + " ".join(map(str, round(vertex, 8))) + "\n")
        for normal in mesh.normals:
            f.write("vn " + " ".join(map(str, round(normal, 8))) + "\n")
        for face in mesh.triangles:
            face = " ".join([
                str(face[0] + 1) + "//" + str(face[0] + 1),
                str(face[1] + 1) + "//" + str(face[1] + 1),
                str(face[2] + 1) + "//" + str(face[2] + 1),
            ])
            f.write("f " + face + "\n")

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
        lines = list(map(lambda x: x.rstrip(), f.readlines()))
        if "" in lines:
            lines.remove("")

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

def GetImports(file):
    with open(file) as f:
        lines = f.read().rstrip().splitlines()
    imports = []
    for line in lines:
        line = line.lstrip()
        if line.startswith("import") or (line.startswith("from") and " import " in line):
            imports.append(line)
    return "\n".join(imports) + "\n\n"

def SaveSceneToProject(scene, filePath=None, name=None):
    if filePath:
        directory = os.path.dirname(os.path.abspath(filePath))
    else:
        directory = os.getcwd()
    if name is None:
        directory = os.path.join(directory, scene.name)
    else:
        directory = os.path.join(directory, name)
    os.makedirs(directory, exist_ok=True)

    project = Project(directory, scene.name)

    project.import_file(os.path.join("Scenes", scene.name + ".scene"), None)
    SaveScene(scene, project)
    return project

def SaveAllScenes(name, filePath=None):
    if filePath:
        directory = os.path.dirname(os.path.abspath(filePath))
    else:
        directory = os.getcwd()
    directory = os.path.join(directory, name)
    os.makedirs(directory, exist_ok=True)

    project = Project(directory, name)

    for scene in SceneManager.scenesByIndex:
        SaveScene(scene, project)
        project.import_file(os.path.join(
            "Scenes", scene.name + ".scene"), None)
    project.write_project()
    return project

def GetId(ids, obj):
    id_ = id(obj)
    if id_ not in ids:
        ids[id_] = str(uuid4())
    return ids[id_]

def SaveScene(scene, project):
    directory = project.path
    os.makedirs(os.path.join(directory, "Scenes"), exist_ok=True)
    f = open(os.path.join(directory, "Scenes", scene.name + ".scene"), "w+")
    f.write("Scene : " + scene.id + "\n")
    f.write("    name: " + json.dumps(scene.name) + "\n")

    ids = scene.ids
    for gameObject in scene.gameObjects:
        f.write("GameObject : " + GetId(ids, gameObject) + "\n")
        f.write("    name: " + json.dumps(gameObject.name) + "\n")
        f.write("    tag: " + str(gameObject.tag.tag) + "\n")
        f.write("    transform: " + GetId(ids, gameObject.transform) + "\n")

    # 2nd pass (for components)
    for gameObject in scene.gameObjects:
        for component in gameObject.components:
            uuid = GetId(ids, component)
            if issubclass(type(component), Behaviour):
                name = type(component).__name__ + "(Behaviour)"
                file = os.path.join("Scripts", type(
                    component).__name__ + ".py")
                path = os.path.join(directory, file)
                if file not in project.file_paths:
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    with open(path, "w+") as f2:
                        f2.write(GetImports(inspect.getfile(type(component))))
                        f2.write(inspect.getsource(type(component)))
                    project.import_file(file, "Behaviour")
            else:
                name = type(component).__name__ + "(Component)"
            f.write(name + " : " + uuid + "\n")

            f.write("    gameObject: " + ids[id(gameObject)] + "\n")
            if isinstance(component, Behaviour):
                f.write("    _script: " + project.file_paths[os.path.join(
                    "Scripts", type(component).__name__ + ".py")].uuid + "\n")
            for attr in component.saved:
                value = getattr(component, attr)
                if id(value) in ids:
                    written = ids[id(value)]
                elif isinstance(value, Behaviour) and attr == "_script":
                    continue
                elif isinstance(value, Mesh):
                    if id(value) in ids:
                        written = ids[id(value)]
                    else:
                        written = str(uuid4())
                        SaveMesh(value, gameObject.name, os.path.join(
                            directory, "Meshes", gameObject.name + ".mesh"))
                        project.import_file(os.path.join(
                            "Meshes", gameObject.name + ".mesh"), "Mesh", written)
                        ids[id(value)] = written
                elif isinstance(value, Material):
                    if hasattr(component, "default"):
                        written = "default"
                    elif id(value) in ids:
                        written = ids[id(value)]
                    else:
                        written = str(uuid4())
                        project.save_mat(value, gameObject.name)
                        project.import_file(os.path.join(
                            "Materials", gameObject.name + ".mat"), "Material", written)
                        ids[id(value)] = written
                elif isinstance(value, AudioClip):
                    if id(value) in ids:
                        written = ids[id(value)]
                    else:
                        written = str(uuid4())
                        os.makedirs(os.path.join(
                            directory, "Sounds"), exist_ok=True)
                        shutil.copy(value.path, os.path.join(directory,
                                                             "Sounds", os.path.basename(value.path)))
                        project.import_file(os.path.join("Sounds",
                                                         os.path.basename(value.path)), written)
                        ids[id(value)] = written
                else:
                    written = str(value)
                f.write("    " + attr + ": " + written + "\n")

    project.write_project()

class ObjectInfo:
    def __init__(self, uuid, type, attrs):
        self.uuid = uuid
        self.type = type
        self.attrs = attrs

    def __getattr__(self, attr):
        return self.attrs[attr]

components = {
    "Transform": Transform,
    "Camera": Camera,
    "Light": Light,
    "MeshRenderer": MeshRenderer,
    "AABBoxCollider": AABBoxCollider,
    "SphereCollider": SphereCollider,
    "Rigidbody": Rigidbody,
    "AudioSource": AudioSource,
    "AudioListener": AudioListener
}
"""List of all components by name"""

def parse_string(string):
    if string.startswith("Vector3("):
        return True, Vector3(*list(map(float, string[8:-1].split(", "))))
    if string.startswith("Quaternion("):
        return True, Quaternion(*list(map(float, string[11:-1].split(", "))))
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
        check, items = zip(*list(map(parse_string, string.split(", "))))
        if all(check):
            return True, tuple(items)
    if string.startswith("[") and string.endswith("]"):
        check, items = zip(*list(map(parse_string, string[1:-1].split(", "))))
        if all(check):
            return True, list(items)
    return False, None

def LoadProject(filePath):
    project = Project.from_folder(filePath)

    scenes = [value[1]
              for value in project.files.values() if value[0].type == "Scene"]
    for path in scenes:
        with open(os.path.join(project.path, path), "r") as f:
            lines = f.read().rstrip().splitlines()

        data = []
        for line in lines:
            if not line.startswith("    "):
                data.append([line])
            else:
                data[-1].append(line)

        infos = []
        for info in data:
            type_, uuid = info[0].split(" : ")
            attrs = {attr: value for attr, value in map(
                lambda x: x[4:].split(": "), info[1:])}
            infos.append(ObjectInfo(uuid, type_, attrs))

        gameObjectInfo = list(filter(lambda x: x.type == "GameObject", infos))
        componentInfo = list(filter(lambda x: "(Component)" in x.type, infos))
        behaviourInfo = list(filter(lambda x: "(Behaviour)" in x.type, infos))

        scene_info = infos.pop(0)
        scene = SceneManager.AddBareScene(json.loads(scene_info.name))
        scene.id = scene_info.uuid

        ids = {}

        gameObjects = []
        for info in gameObjectInfo:
            gameObject = GameObject.BareObject(json.loads(info.name))
            gameObjects.append(gameObject)
            gameObject.tag = Tag(int(info.tag))
            ids[info.uuid] = gameObject

        for info in componentInfo:
            gameObject = ids[info.gameObject]
            del info.attrs["gameObject"]
            component = components[info.type[:-11]]
            component = gameObject.AddComponent(component)
            ids[info.uuid] = component
            for name, value in reversed(info.attrs.items()):
                if isinstance(component, MeshRenderer) and \
                        [name, value] == ["mat", "default"]:
                    component.mat = MeshRenderer.DefaultMaterial
                    continue
                check, obj = parse_string(value)
                if check:
                    setattr(component, name, obj)
                elif value in ids:
                    setattr(component, name, ids[value])
                elif value in project.files:
                    file = project.files[value][0]
                    if file.type == "Material":
                        obj = project.load_mat(file)
                    elif file.type == "Mesh":
                        obj = LoadMesh(os.path.join(project.path, file.path))
                    elif file.type == "Ogg":
                        obj = AudioClip(os.path.join(project.path, file.path))
                    setattr(component, name, obj)

        script = Scripts.LoadScripts(os.path.join(filePath, "Scripts"))
        for info in behaviourInfo:
            gameObject = ids[info.gameObject]
            del info.attrs["gameObject"]
            behaviour = gameObject.AddComponent(
                getattr(script, info.type[:-11]))
            for name, value in reversed(info.attrs.items()):
                check, obj = parse_string(value)
                if check:
                    setattr(behaviour, name, obj)
                elif value in ids:
                    setattr(behaviour, name, ids[value])
                elif value in project.files:
                    file = project.files[value][0]
                    if file.type == "Material":
                        obj = project.load_mat(file)
                    elif file.type == "Mesh":
                        obj = LoadMesh(os.path.join(project.path, file.path))
                    elif file.type == "Ogg":
                        obj = AudioClip(os.path.join(project.path, file.path))
                    setattr(behaviour, name, obj)

        for gameObject in gameObjects:
            scene.Add(gameObject)

        scene.mainCamera = scene.FindGameObjectsByName(
            "Main Camera")[0].GetComponent(Camera)
        scene.ids = ids

    return project

class Primitives:
    """
    Primitive preloaded meshes.
    Do not instantiate this class.

    """

    __path = os.path.dirname(os.path.abspath(__file__))
    cube = LoadMesh(os.path.join(__path, "primitives/cube.mesh"))
    quad = LoadMesh(os.path.join(__path, "primitives/quad.mesh"))
    double_quad = LoadMesh(os.path.join(__path, "primitives/double_quad.mesh"))
    sphere = LoadMesh(os.path.join(__path, "primitives/sphere.mesh"))
    capsule = LoadMesh(os.path.join(__path, "primitives/capsule.mesh"))
    cylinder = LoadMesh(os.path.join(__path, "primitives/cylinder.mesh"))
