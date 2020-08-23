from .vector3 import Vector3
from .meshes import Mesh

def LoadObj(filename):
    vertices = []
    norm_index = []
    norm_vectors = []
    face_norms = []
    faces = []

    material = None
    for line in open(filename, "r"):
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue
        if values[0] == 'v':
            v = Vector3(*map(float, values[1:4]))
            vertices.append(v)
        elif values[0] == 'vn':
            v = list(map(float, values[1:4]))
            norm_vectors.append(v)
        elif values[0] == 'f':
            face = []
            normals = []
            for v in values[1:]:
                w = v.split('/')
                face.append(int(w[0]) - 1)
                if len(w) >= 3 and len(w[2]) > 0:
                    normals.append(int(w[2]) - 1)
                else:
                    normals.append(0)
            faces.append(Vector3(*face[::-1]))
            norm_index.append(normals[::-1])
    
    if not norm_vectors: norm_vectors.append(Vector3.zero())
    
    for normal in norm_index:
        face_norms.append(norm_vectors[normal[0]])
    
    return Mesh(vertices, faces, face_norms)