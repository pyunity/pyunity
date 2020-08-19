import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from .window import *

windowProvider = None
size = (800, 500)
fps = 60
faceCulling = True

windowProviders = {"glut": glutWindow, "glfw": glfwWindow, "pygame": pygameWindow}