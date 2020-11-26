from vector3 cimport Vector3
from vector3 import Vector3
from meshes cimport Mesh
from scene cimport Scene
from core cimport *
import cython

@cython.locals(vertices=list, normals=list, faces=list, values=list, a=Vector3, b=Vector3, normal=Vector3)
cpdef Mesh LoadObj(str filename)

@cython.locals(lines=list, vertices=list, normals=list, faces=list, a=Vector3, b=Vector3, normal=Vector3)
cpdef Mesh LoadMesh(str filename)

@cython.locals(directory=str, vertex=Vector3, i=cython.int, triangle=list, j=cython.int, item=cython.int)
cpdef void SaveMesh(Mesh mesh, str name, str filePath=*)

@cython.locals(directory=str)
cpdef void SaveScene(Scene scene, str filePath=*)

@cython.locals(directory=str)
cpdef Scene LoadScene(Scene scene, str filePath=*)

cdef class Primitives:
    cdef public Mesh cube, quad, double_quad, sphere, capsule, cylinder