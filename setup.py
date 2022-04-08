# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

from setuptools import setup, find_packages, Extension
import os
import re
import glob

if "cython" not in os.environ:
    os.environ["cython"] = "1"

with open("README.md", "r") as fh:
    longDesc = fh.read()

if os.environ["cython"] == "1":
    if not os.path.isdir("src"):
        if not os.path.isfile("prepare.py"):
            raise Exception("\n".join([
                "Source directory `src` not found but `prepare.py` does not exist.",
                "If this is not a local clone of the repository, please report",
                "this as a bug at https://github.com/pyunity/pyunity/issues."
            ]))
        import prepare
        prepare.cythonize()
    cFiles = glob.glob("src/**/*.c", recursive=True)
    dataFiles = list(filter(lambda a: ".c" not in a,
                            glob.glob("src/**/*.*", recursive=True)))
    config = {
        "package_dir": {"pyunity": "src"},
        "packages": ["pyunity"] + ["pyunity." + package for package in find_packages(where="pyunity")],
        "ext_package": "pyunity",
        "ext_modules": [Extension(file[4:-2].replace(os.path.sep, "."), [file]) for file in cFiles],
        "package_data": {"pyunity": [file[4:] for file in dataFiles]},
    }
    versionfile = "src/_version.py"
else:
    dataFiles = list(filter(lambda a: ".py" not in a,
                            glob.glob("pyunity/**/*.*", recursive=True)))
    config = {
        "packages": ["pyunity"] + ["pyunity." + package for package in find_packages(where="pyunity")],
        "package_data": {"pyunity": [file[8:] for file in dataFiles]},
    }
    versionfile = "pyunity/_version.py"

verstrline = open(versionfile, "r").read()
versionexp = r"^__version__ = ['\"]([^'\"]*)['\"]"
match = re.search(versionexp, verstrline, re.M)
if match:
    version = match.group(1)
else:
    raise RuntimeError(f"Unable to find version string in {versionfile}")

setup(
    name="pyunity",
    version=version,
    author="Ray Chen",
    author_email="tankimarshal2@gmail.com",
    description="A Python implementation of the Unity Engine",
    long_description=longDesc,
    long_description_content_type="text/markdown",
    license="MIT",
    project_urls={
        "Documentation": "https://docs.pyunity.x10.bz/",
        "Source": "https://github.com/pyunity/pyunity",
        "Tracker": "https://github.com/pyunity/pyunity/issues"
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=[
        "pyopengl",
        "pillow",
        "pysdl2",
        "pysdl2-dll",
        "pyglm",
    ],
    python_requires=">=3.6",
    zip_safe=False,
    **config,
)
