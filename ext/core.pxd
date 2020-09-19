cdef class Tag:
    cdef public str tagName
    cdef public int tag

cdef class GameObject:
    cdef public str name
    cdef public list components
    cdef public Transform transform
    cdef public Tag tag