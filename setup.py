from setuptools import setup
import pyunity

setup(
    name = "pyunity",
    version = pyunity.__version__,
    description = "",
    url = "",
    install_requires = [
        "glfw",
        "pygame",
        "pyopengl",
    ],
)