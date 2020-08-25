from .vector3 import Vector3
from .meshes import Mesh
from .core import *
import random, pickle

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

def SaveScene(scene):
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
    #             for attrib in component.ListAttributes():
    #                 f.write("    " + attrib[0] + ": " + attrib[1] + "\n")

    with open(scene.name + ".scene", "wb+") as f:
        pickle.dump(scene, f)

def LoadScene(sceneName):
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
    with open(sceneName + ".scene", "rb") as f:
        scene = pickle.load(f)
    return scene