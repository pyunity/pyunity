from vector3 cimport Vector3

cdef class Mesh:
    cdef public tuple verts, triangles, normals
    cdef public Vector3 min, max