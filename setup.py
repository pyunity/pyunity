# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

from setuptools import setup, find_packages, Extension
from setuptools.command.egg_info import egg_info, manifest_maker
from pathlib import Path
import os
import re
import sys
import glob
import json
import subprocess

if "cython" not in os.environ:
    os.environ["cython"] = "1"

class SaveMeta(egg_info):
    def writeVersion(self):
        if not os.path.isdir(".git"):
            return

        p = subprocess.Popen(["git", "rev-parse", "HEAD"],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        stdout, _ = p.communicate()
        rev = stdout.decode().rstrip()
        if p.returncode != 0:
            rev = "unknown"
            local = True
        else:
            p = subprocess.Popen(["git", "branch", "-r", "--contains", rev],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            stdout, _ = p.communicate()
            out = stdout.decode().rstrip()
            if p.returncode != 0:
                local = True
            else:
                local = len(out) == 0

        data = {"revision": rev, "local": local}
        self.write_or_delete_file(
            "version", Path(self.egg_info) / "version.json", json.dumps(data))

    def find_sources(self):
        """Generate SOURCES.txt manifest file"""
        self.writeVersion()
        sources = Path(self.egg_info) / "SOURCES.txt"
        mm = ManifestMaker(self.distribution)
        mm.manifest = str(sources)
        mm.run()
        self.filelist = mm.filelist

class ManifestMaker(manifest_maker):
    def add_defaults(self):
        super(ManifestMaker, self).add_defaults()
        self.filelist.append("prepare.py")

class Cythonize(SaveMeta):
    def run(self):
        if os.environ["cython"] == "1":
            self.announce("Cython enabled", level=2)
            if not os.path.isdir("src"):
                self.announce(
                    "src/ directory not found", level=2)
                cmd = [sys.executable, "prepare.py", "cythonize"]
                self.announce(
                    f"Running command: {cmd}",
                    level=2)
                subprocess.check_call(cmd)
            else:
                self.announce(
                    "src/ directory found", level=2)
        else:
            self.announce(
                "Cython disabled", level=2)

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
        dataFiles = [a for a in glob.glob("src/**/*.*", recursive=True) if ".c" not in a]
        versionfile = "src/_version.py"

    config = {
        "cmdclass": {"egg_info": Cythonize},
        "package_dir": {"pyunity": "src"},
        "packages": ["pyunity"] + ["src." + package for package in find_packages(where="pyunity")],
        "ext_package": "pyunity",
        "ext_modules": [Extension(file[4:-2].replace(os.path.sep, "."), [file]) for file in cFiles],
        "package_data": {"pyunity": [file[4:] for file in dataFiles]},
        "zip_safe": False
    }
else:
    dataFiles = [a for a in glob.glob("pyunity/**/*.*", recursive=True) if ".py" not in a]
    config = {
        "cmdclass": {"egg_info": SaveMeta},
        "packages": ["pyunity"] + ["pyunity." + package for package in find_packages(where="pyunity")],
        "package_data": {"pyunity": [file[8:] for file in dataFiles]},
        "zip_safe": True
    }
    versionfile = "pyunity/_version.py"

verstrline = open(versionfile, "r").read()
versionexp = r"^versionInfo = VersionInfo\((\d+), (\d+), (\d+)"
match = re.search(versionexp, verstrline, re.M)
if match:
    version = f"{match.group(1)}.{match.group(2)}.{match.group(3)}"
else:
    raise RuntimeError(f"Unable to find version string in {versionfile}")

setup(
    version=version,
    **config,
)
