import os
from .glfwWindow import Window as glfwWindow
from .glutWindow import Window as glutWindow
from .pygameWindow import Window as pygameWindow

if os.environ["PYUNITY_DEBUG_MODE"] == "1":
    print("Loaded window providers")