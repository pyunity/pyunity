from vector3 cimport Vector3
from quaternion cimport Quaternion
from meshes cimport Mesh

cdef list tags

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
    cpdef void Start(Behaviour self)
    cpdef void Update(Behaviour self, float dt)

cdef class Transform(Component):
    cdef public Vector3 localPosition
    cdef public Quaternion localRotation
    cdef public Vector3 localScale
    cdef public Transform parent
    cdef public list children
    cpdef void ReparentTo(Transform self, Transform parent)
    cpdef void List(Transform self)
    cpdef str FullPath(Transform self)

cdef class Camera(Component):
    cdef public float fov, near, far
    cdef public tuple clearColor

cdef class Light(Component):
    cdef public float intensity
    cdef public int type

cdef class MeshRenderer(Component):
    cdef public Mesh mesh
    cdef public Material mat
    cpdef void render(MeshRenderer self)

cdef class Material:
    cdef public tuple color