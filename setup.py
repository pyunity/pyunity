from setuptools import setup, find_packages, Extension
import os, glob, shutil, sys
if "cython" not in os.environ:
    os.environ["cython"] = "1"

with open("README.md", "r") as fh:
    long_description = fh.read()

if os.environ["cython"] == "1":
    c_files = glob.glob("src/**/*.c", recursive = True)
    mesh_files = glob.glob("src/**/*.mesh", recursive = True)
    config = {
        "package_dir": {"pyunity": "src"},
        "packages": ["pyunity"] + ["pyunity." + package for package in find_packages(where = "src")],
        "ext_package": "pyunity",
        "ext_modules": [Extension(file[4:-2].replace(os.path.sep, "."), [file]) for file in c_files],
        "package_data": {"pyunity": [file[4:] for file in mesh_files]},
    }
else:
    mesh_files = glob.glob("pyunity/**/*.mesh", recursive = True)
    config = {
        "packages": ["pyunity"] + ["pyunity." + package for package in find_packages(where = "pyunity")],
        "package_data": {"pyunity": [file[8:] for file in mesh_files]},
    }

setup(
    name = "pyunity",
    version = "0.2.0",
    author = "Ray Chen",
    author_email = "tankimarshal2@gmail.com",
    description = "A Python implementation of the Unity Engine",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github/rayzchen/PyUnity",
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    setup_requires = [
        "cython",
    ],
    install_requires = [
        "glfw",
        "pygame",
        "pyopengl",
    ],
    python_requires = '>=3.6',
    **config,
)
