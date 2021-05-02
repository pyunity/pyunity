from __init__ cimport Scene

cdef Scene AddScene(str name)
cdef Scene GetSceneByIndex(int index)
cdef Scene GetSceneByName(str name)
cdef void RemoveScene(Scene name)
cdef void LoadSceneByName(str name)
cdef void LoadSceneByIndex(int index)
cdef void LoadScene(Scene scene)
cdef void __loadScene(Scene scene)