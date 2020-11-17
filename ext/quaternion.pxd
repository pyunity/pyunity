from vector3 cimport Vector3
import cython

cdef class Quaternion:
    cdef public float w, x, y, z
    cpdef public Quaternion copy(Quaternion self)
    @cython.locals(length=cython.float)
    cpdef public Quaternion normalized(Quaternion self)
    cpdef public Vector3 RotateVector(Quaternion self, Vector3 vector)