from . import window

windowProvider = None
size = (800, 500)
fps = 60
faceCulling = True

windowProviders = [glutWindow, glfwWindow, pygameWindow]