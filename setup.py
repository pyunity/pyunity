# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

from setuptools import setup, find_packages, Extension
from setuptools.command.egg_info import egg_info
import distutils.log
import os
import re
import sys
import glob
import subprocess

if "cython" not in os.environ:
    os.environ["cython"] = "1"

class Cythonize(egg_info):
    def run(self):
        if os.environ["cython"] == "1":
            self.announce("Cython enabled", level=distutils.log.INFO)
            if not os.path.isdir("src"):
                self.announce(
                    "src/ directory not found", level=distutils.log.INFO)
                cmd = [sys.executable, "prepare.py", "cythonize"]
                self.announce(
                    f"Running command: {cmd}",
                    level=distutils.log.INFO)
                subprocess.check_call(cmd)
            else:
                self.announce(
                    "src/ directory found", level=distutils.log.INFO)
        else:
            self.announce(
                "Cython disabled", level=distutils.log.INFO)
        super(Cythonize, self).run()

if os.environ["cython"] == "1":
    if not os.path.isdir("src"):
        if not os.path.isfile("prepare.py"):
            raise Exception("\n".join([
                "Source directory `src` not found but `prepare.py` does not exist.",
                "If this is not a local clone of the repository, please report",
                "this as a bug at https://github.com/pyunity/pyunity/issues."
            ]))
        if not os.path.isdir("pyunity"):
            raise Exception("\n".join([
                "Source directory `src` not found but `pyunity` does not exist.",
                "If this is not a local clone of the repository, please report",
                "this as a bug at https://github.com/pyunity/pyunity/issues."
            ]))
        import prepare
        cFiles, dataFiles = prepare.getFiles()
        versionfile = "pyunity/_version.py"
    else:
        cFiles = glob.glob("src/**/*.c", recursive=True)
        dataFiles = list(filter(lambda a: ".c" not in a,
                                glob.glob("src/**/*.*", recursive=True)))
        versionfile = "src/_version.py"

    config = {
        "cmdclass": {"egg_info": Cythonize},
        "package_dir": {"pyunity": "src"},
        "packages": ["pyunity"] + ["pyunity." + package for package in find_packages(where="pyunity")],
        "ext_package": "pyunity",
        "ext_modules": [Extension(file[4:-2].replace(os.path.sep, "."), [file]) for file in cFiles],
        "package_data": {"pyunity": [file[4:] for file in dataFiles]},
    }
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
    version=version,
    **config,
)
