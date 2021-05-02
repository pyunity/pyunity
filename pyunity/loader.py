"""
Utility functions related to loading
and saving PyUnity meshes and scenes.

"""

from .vector3 import Vector3
from .meshes import Mesh
from .core import *
from .scenes import SceneManager
from . import logger as Logger
import pickle
import os
# import random

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

    normals = []
    for face in faces:
        a = vertices[face[2]] - vertices[face[1]]
        b = vertices[face[0]] - vertices[face[1]]
        normal = a.cross(b).normalized()
        normals.append(normal)

    return Mesh(vertices, faces, normals)

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
        directory = os.path.dirname(os.path.realpath(filePath))
    else:
        directory = os.getcwd()

    with open(os.path.join(directory, name + ".mesh"), "w+") as f:
        i = 0
        for vertex in mesh.verts:
            i += 1
            f.write(str(vertex.x) + "/")
            f.write(str(vertex.y) + "/")
            f.write(str(vertex.z))
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

# def randomHex(length):
#     """
#     Returns a random hexadecimal string of length `length`.

#     Parameters
#     ----------
#     length : int
#         Length of string

#     Returns
#     -------
#     str
#         A random hexadecimal string

#     """
#     return ("%0" + str(length) + "x") % random.randrange(16 ** length)

# def AddHex(l, length):
#     x = randomHex(length)
#     while x in l: x = randomHex(length)
#     l.append(x)
#     return x

def SaveScene(scene, filePath=None):
    """
    Save a scene to a file. Uses pickle.

    Parameters
    ----------
    scene : Scene
        Scene to save
    filePath : str, optional
        Pass in `__file__` to save in
        directory of script, otherwise
        pass in a directory. If not
        specified, then the scene is saved
        in the cwd.

    """
    # hexes = []
    # with open(scene.name + ".scene", "w+") as f:
    #     for gameObject in scene.gameObjects:
    #         f.write("GameObject (" + gameObject.name + ") " + AddHex(hexes, 24) + ":\n")
    #         for component in gameObject.components:
    #             f.write("  Component " + type(component).__name__ + " " + AddHex(hexes, 24) + ":\n")

    if filePath:
        directory = os.path.dirname(os.path.realpath(filePath))
    else:
        directory = os.getcwd()

    with open(os.path.join(directory, scene.name + ".scene"), "wb+") as f:
        pickle.dump(scene, f)

def LoadScene(sceneName, filePath=None):
    """
    Load a scene from a file. Uses pickle.

    Parameters
    ----------
    sceneName : str
        Name of the scene, without
        the .scene extension

    Returns
    -------
    Scene
        Loaded scene

    Notes
    -----
    If there already is a scene called
    `sceneName`, then no scene will be added.

    """
    if sceneName in SceneManager.scenesByName:
        Logger.LogLine(Logger.WARNING, "Already has scene called", sceneName)
        return

    if filePath:
        directory = os.path.dirname(os.path.realpath(filePath))
    else:
        directory = os.getcwd()

    with open(os.path.join(directory, sceneName + ".scene"), "rb") as f:
        scene = pickle.load(f)

    SceneManager.scenesByIndex.append(scene)
    SceneManager.scenesByName[sceneName] = scene
    return scene

class Primitives:
    __path = os.path.dirname(os.path.realpath(__file__))
    cube = LoadMesh(os.path.join(__path, "primitives/cube.mesh"))
    quad = LoadMesh(os.path.join(__path, "primitives/quad.mesh"))
    double_quad = LoadMesh(os.path.join(__path, "primitives/double_quad.mesh"))
    sphere = LoadMesh(os.path.join(__path, "primitives/sphere.mesh"))
    capsule = LoadMesh(os.path.join(__path, "primitives/capsule.mesh"))
    cylinder = LoadMesh(os.path.join(__path, "primitives/cylinder.mesh"))
