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
from .errors import PyUnityException
from ._version import versionInfo
from . import Loader, SceneManager, examples

def getRepoInfo():
    # Get repo version info
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

    p = subprocess.Popen(["git", "diff", "--quiet", "--", "**/*.py"],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    p.communicate()
    print("Working tree modified:", p.returncode != 1)

def getTomlLoader():
    if sys.version_info >= (3, 11):
        from tomllib import load as tomlLoad
        format = "rb"
    elif pkgutil.find_loader("toml") is not None:
        from toml import load as tomlLoad
        format = "r"
    elif pkgutil.find_loader("tomli") is not None:
        from tomli import load as tomlLoad
        format = "rb"
    else:
        tomlLoad = None
    return tomlLoad, format

def formatName(item):
    return re.split("[^a-zA-Z0-9_-]", item)[0].lower().replace("_", "-")

def getReqsFromToml(version):
    if not os.path.isfile("pyproject.toml"):
        print("Warning: Could not find pyproject.toml")
        return None

    tomlLoad, format = getTomlLoader()
    if tomlLoad is None:
        print("Warning: could not load pyproject.toml")
        return None

    reqs = {"": []}
    with open("pyproject.toml", format) as f:
        data = tomlLoad(f)

    if "project" not in data or "dependencies" not in data["project"]:
        print("Warning: pyproject.toml missing dependencies section")
        return None

    for item in data["project"]["dependencies"]:
        name = formatName(item)
        reqs[""].append((name, version(name)))

    if "optional-dependencies" in data["project"]:
        optDeps = data["project"]["optional-dependencies"]
        for section in optDeps:
            if section not in reqs:
                reqs[section] = []
            for item in optDeps[section]:
                name = formatName(item)
                reqs[section].append((name, version(name)))
    return reqs

def getReqsFromRepo(path, version):
    print("Warning: PyUnity not ran as an installed package")
    orig = os.getcwd()
    os.chdir(path.parent.parent)
    getRepoInfo()
    reqs = getReqsFromToml(version)
    if reqs is not None:
        removed = []
        for section in reqs:
            if all(x[1] is None for x in reqs[section]):
                removed.append(section)

        for section in removed:
            reqs.pop(section)
        if len(reqs) == 0:
            print("Warning: no reqs found in pyproject.toml")
            reqs = None
    if reqs is None:
        if os.path.isfile("reqs.txt"):
            reqs = {"": []}
            with open("reqs.txt") as f:
                for item in f.read().rstrip().split("\n"):
                    name = formatName(item)
                    reqs[""].append((name, version(name)))
        else:
            print("Warning: No reqs.txt file found")

    os.chdir(orig)
    return reqs

def getReqsFromDistribution(dist, version, gitInfo=True):
    if gitInfo:
        data = json.loads(dist.read_text("version.json"))
        if data is not None:
            print("Git commit hash:", data["revision"])
            print("Local commit:", data["local"])
        else:
            print("Warning: version.json not found")

    discriminant = "; extra == \""
    reqs = {"": []}
    for item in dist.requires:
        name = formatName(item)
        if discriminant not in item:
            reqs[""].append((name, version(name)))
        else:
            group = item[item.index(discriminant) + len(discriminant): -1]
            if group not in reqs:
                reqs[group] = []
            reqs[group].append((name, version(name)))

    return reqs

def printSystemInfo():
    TITLE_WIDTH = 30
    print("#" * TITLE_WIDTH)
    print("VERSION INFO".center(TITLE_WIDTH))
    print("#" * TITLE_WIDTH)

    vstr = "v{0.major}.{0.minor}.{0.micro}"
    print("PyUnity version: " + vstr.format(versionInfo) + versionInfo.releaselevel)
    print("Python version:",
          vstr.format(sys.version_info) + "-" + sys.version_info.releaselevel)
    print("Operating system:", platform.system(), platform.release())
    print("Machine:", platform.machine())
    print("Python architecture:", platform.architecture()[0])

def getReqs():
    if sys.version_info >= (3, 8):
        from importlib.metadata import distribution, version, PackageNotFoundError
    elif pkgutil.find_loader("importlib_metadata") is not None:
        from importlib_metadata import distribution, version, PackageNotFoundError
    else:
        distribution = None
        print("Warning: Python version less than 3.8 but no importlib_metadata found")

    def getVersion(name):
        try:
            return version(name)
        except PackageNotFoundError:
            return None

    path = Path(__file__)
    reqs = None
    repoChecked = False
    if path.exists() and (path.parent.parent / ".git").is_dir():
        repoChecked = True
        reqs = getReqsFromRepo(path, getVersion)

    if reqs is None:
        try:
            if distribution is None:
                raise PackageNotFoundError
            dist = distribution("pyunity")
        except PackageNotFoundError:
            print("Warning: could not find pyunity distribution info")
            reqs = None
        else:
            reqs = getReqsFromDistribution(dist, getVersion, not repoChecked)

    return reqs

def printInfo():
    printSystemInfo()
    reqs = getReqs()
    if reqs is not None:
        print("\nDependencies:")
        for item, version in reqs[""]:
            print("-", item, "version:", version)

        if len(reqs) > 1:
            print("Optional dependencies:")
            sortedKeys = sorted(reqs.keys(), key=lambda x: len(reqs[x]), reverse=True)
            for section in sortedKeys:
                if section == "":
                    continue
                print("-", section + ":")
                for item, version in reqs[section]:
                    print("  -", item, "version:", version)
        else:
            print("Optional dependencies: none installed")

parser = argparse.ArgumentParser(description="Load PyUnity examples, PyUnity projects or display information about the PyUnity installation")
parser.add_argument("-v", "--version", action="store_true",
                    help="Display information about the PyUnity installation")
parser.add_argument("project", nargs="?", default="0",
                    help="Project or example number to load")

def main():
    args = parser.parse_args()
    if args.version:
        printInfo()
        return

    if args.project.isdecimal():
        examples.show()
    elif os.path.isdir(args.project):
        project = Loader.LoadProject(args.project)
        SceneManager.LoadSceneByIndex(project.firstScene)
    else:
        raise PyUnityException(f"invalid project: {args.project}")

if __name__ == "__main__":
    main()
