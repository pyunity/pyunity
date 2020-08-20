from setuptools import setup, find_packages
import os, pyunity

pyopengl_link = "pyopengl @ git+https://raw.githubusercontent.com/rayzchen/PyUnity/master/PyOpenGL-3.1.5-cp38-cp38-win32.whl"
pyopengl_accelerate_link = "pyopengl-accelerate @ git+https://raw.githubusercontent.com/rayzchen/PyUnity/master/PyOpenGL_accelerate-3.1.5-cp38-cp38-win32.whl"
if os.name == "nt":
    links = [pyopengl_link, pyopengl_accelerate_link]
else:
    links = []

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "pyunity",
    version = pyunity.__version__,
    author = "Ray Chen",
    author_email = "tankimarshal2@gmail.com",
    description = "A Python implementation of the Unity Engine",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github/rayzchen/PyUnity",
    packages = find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
    dependency_links = links,
    install_requires = [
        "glfw",
        "pygame",
        # *links,
        "pyopengl",
    ],
    python_requires = '>=3.7',
)