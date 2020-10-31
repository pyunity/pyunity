from vector3 cimport Vector3
from quaternion cimport Quaternion

cdef class Tag:
    cdef public str tagName
    cdef public int tag

cdef class GameObject:
    cdef public str name
    cdef public list components
    cdef public Tag tag
    cdef public Transform transform

cdef class Component:
    cdef public GameObject gameObject
    cdef public Transform transform

cdef class Behaviour(Component):
    cdef void Start(Behaviour self)
    cdef void Update(Behaviour self, float dt)

cdef class Transform(Component):
    cdef public Vector3 localPosition
    cdef public Quaternion localRotation
    cdef public Vector3 localScale
    cdef public Transform parent
    cdef public list children
    cdef void ReparentTo(Transform self, Transform parent)