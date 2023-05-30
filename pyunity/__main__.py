## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

from pathlib import Path
import re
import os
import sys
import json
import subprocess
import platform
import pkgutil
import argparse
from ._version import versionInfo
from . import Loader, SceneManager, examples

def printVersion():
    TITLE_WIDTH = 30
    print("#" * TITLE_WIDTH)
    print("VERSION INFO".center(TITLE_WIDTH))
    print("#" * TITLE_WIDTH)

    vstr = "v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}"
    print("PyUnity version: " + vstr.format(versionInfo))
    print("Python version:", vstr.format(sys.version_info))
    print("Operating system:", platform.system(), platform.release())
    print("Machine:", platform.machine())
    print("Python architecture:", platform.architecture()[0])

    if sys.version_info >= (3, 8):
        from importlib.metadata import distribution, version, PackageNotFoundError
    elif pkgutil.find_loader("importlib_metadata") is not None:
        from importlib_metadata import distribution, version, PackageNotFoundError
    else:
        distribution = None
        print("Warning: Python version less than 3.8 but no importlib_metadata found")

    if distribution is not None:
        gitrepo = False
        try:
            dist = distribution("pyunity")

            path = Path(__file__)
            if path.exists() and (path.parent.parent / ".git").is_dir():
                gitrepo = True
                raise PackageNotFoundError
        except PackageNotFoundError:
            print("Warning: PyUnity not ran as an installed package")
            requirements = []

            orig = os.getcwd()
            if gitrepo:
                os.chdir(path.parent.parent)
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

                print("Git commit hash:", rev)
                print("Local commit:", local)

                p = subprocess.Popen(["git", "branch", "-r", "--contains", rev],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
                stdout, _ = p.communicate()
                out = stdout.decode().rstrip()
                print("Working tree modified:", len(out) == 0)

                if os.path.isfile("requirements.txt"):
                    with open("requirements.txt") as f:
                        requirements = f.read().rstrip().split("\n")
                else:
                    print("Warning: No requirements.txt file found")

                os.chdir(orig)
        else:
            requirements = dist.requires
            path = dist._path / "version.json"
            if path.is_file():
                with open(path) as f:
                    data = json.load(f)
                print("Git commit hash:", data["revision"])
                print("Local commit:", data["local"])

        print("Dependencies:")
        for item in requirements:
            name = re.split(" |;", item)[0]
            try:
                print("-", name, "version:", version(name))
            except PackageNotFoundError:
                # python_version or sys.platform used
                print("-", name, "version:", None)

parser = argparse.ArgumentParser(description="Load PyUnity examples, PyUnity projects or display information about the PyUnity installation")
parser.add_argument("-v", "--version", action="store_true",
                    help="Display information about the PyUnity installation")
parser.add_argument("project", nargs="?", default="0",
                    help="Project or example number to load")

def main():
    args = parser.parse_args()
    if args.version:
        printVersion()
        return

    if args.project.isdecimal():
        examples.show()
    elif os.path.isdir(args.project):
        project = Loader.LoadProject(args.project)
        SceneManager.LoadSceneByIndex(project.firstScene)
    else:
        raise Exception(f"invalid project: {args.project}")

if __name__ == "__main__":
    main()
