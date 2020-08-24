from .vector3 import Vector3
from .meshes import Mesh

def LoadObj(filename):
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