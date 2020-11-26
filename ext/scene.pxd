from core cimport *

cdef class Scene:
    cdef public str name
    cdef public Camera mainCamera
    cdef public list gameObjects, rootGameObjects
    cpdef public void Add(Scene self, GameObject gameObject)
    cpdef public void Remove(Scene self, GameObject gameObject)
    cpdef public void List(Scene self)
    cpdef public list FindGameObjectsByName(Scene self, str name)
    cpdef public list FindGameObjectsByTagName(Scene self, str name)
    cpdef public list FindGameObjectsByTagNumber(Scene self, int num)
    cpdef public bint inside_frustrum(Scene self, MeshRenderer renderer)
    # cpdef public void start_scripts(Scene self)
    cpdef public void Start(Scene self)
    cpdef public void transform(Scene self, Transform transform)
    cpdef public void update_scripts(Scene self)
    cpdef public void render(Scene self)
    cpdef public void no_interactive(Scene self)
    cpdef public void update(Scene self)