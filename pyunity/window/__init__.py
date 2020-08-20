import os
from .pygameWindow import Window as pygameWindow
from .glutWindow import Window as glutWindow
from .glfwWindow import Window as glfwWindow

if os.environ["PYUNITY_DEBUG_MODE"] == "1":
    print("Loaded window providers")