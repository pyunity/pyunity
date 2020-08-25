from .vector3 import Vector3
from .meshes import Mesh
from .core import *
import random, pickle, sys, os

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

    material = None
    for line in open(filename, "r"):
        if line.startswith("#"): continue
        values = line.split()
        if not values: continue
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
    with open(filename, "r") as f:
        lines = list(map(lambda x: x.rstrip(), f.readlines()))
        if "" in lines: lines.remove("")
    
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

def SaveMesh(mesh, name, filePath = None):
    if filePath: directory = os.path.dirname(os.path.realpath(filePath))
    else: directory = os.getcwd()

    with open(os.path.join(directory, name + ".mesh"), "w+") as f:
        i = 0
        for vertex in mesh.verts:
            i += 1
            f.write(str(vertex.x) + "/")
            f.write(str(vertex.y) + "/")
            f.write(str(vertex.z))
            if i != len(mesh.verts): f.write("/")
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

def SaveScene(scene, filePath = None):
    """
    Save a scene to a file.

    Parameters
    ----------
    scene : Scene
        Scene to save
    
    """
    # hexes = []
    # with open(scene.name + ".scene", "w+") as f:
    #     for gameObject in scene.gameObjects:
    #         f.write("GameObject (" + gameObject.name + ") " + AddHex(hexes, 24) + ":\n")
    #         for component in gameObject.components:
    #             f.write("  Component " + type(component).__name__ + " " + AddHex(hexes, 24) + ":\n")

    if filePath: directory = os.path.dirname(os.path.realpath(filePath))
    else: directory = os.getcwd()
    
    with open(os.path.join(directory, scene.name + ".scene"), "wb+") as f:
        pickle.dump(scene, f)

def LoadScene(sceneName, filePath = None):
    """
    Load a scene from a file.

    Parameters
    ----------
    sceneName : str
        Name of the scene, without
        the .scene extension

    Returns
    -------
    Scene
        Loaded scene
    
    """
    if filePath: directory = os.path.dirname(os.path.realpath(filePath))
    else: directory = os.getcwd()
    
    with open(os.path.join(directory, sceneName + ".scene"), "rb") as f:
        scene = pickle.load(f)
    return scene