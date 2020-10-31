import cython

cdef class Vector3:
    cdef public float x, y, z
    cpdef Vector3 _o2(self, Vector3 other, f)
    cpdef Vector3 _r_o2(self, Vector3 other, f)
    cpdef Vector3 _io(self, Vector3 other, f)
    cpdef Vector3 copy(self)
    cpdef float get_length_sqrd(self)
    @cython.locals(length=cython.float)
    cpdef Vector3 normalized(self)
    @cython.locals(length=cython.float)
    cpdef float normalize_return_length(self)
    cpdef float get_distance(self, Vector3 other)
    cpdef float get_dist_sqrd(self, Vector3 other)
    cpdef float dot(self, Vector3 other)
    @cython.locals(x=cython.float, y=cython.float, z=cython.float)
    cpdef Vector3 cross(self, Vector3 other)