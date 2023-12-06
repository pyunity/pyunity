## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""
Functions to get information about the PyUnity's installation,
distribution or build. The main function is :func:`printInfo`.

"""

from ._version import versionInfo
from pathlib import Path
import os
import re
import sys
import json
import pkgutil
import platform
import subprocess

def getRepoInfo():
    """
    Print information about the git repository that PyUnity
    is running in.

    Note
    ----
    This function only applies to editable installations
    (``pip install -e .``) or local imports (cloned git
    repositories).

    """
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
    """
    Get toml loading function and format to open
    file with

    Returns
    -------
    function, str
        Tuple of toml loading function and format
        to create a file handle with (either "r"
        or "rb")
    """
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
        format = ""
    return tomlLoad, format

def formatName(item):
    """
    Format a requirements item to package name

    Parameters
    ----------
    item : str
        Name of requirement specified in pyproject.toml
        or requirements.txt

    Returns
    -------
    str
        Package name

    Notes
    -----
    The package name is normalized to only have lowercase
    letters a-z, numbers and hyphens.

    """
    return re.split("[^a-zA-Z0-9_-]", item)[0].lower().replace("_", "-")

def getReqsFromToml(version):
    """
    Get all requirements of the PyUnity package from the
    pyproject.toml file found in the repository.

    Parameters
    ----------
    version : function
        Function to get package version. Should be
        imported from ``importlib.metadata`` or
        ``importlib_metadata``.

    Returns
    -------
    dict
        See format of return type of :func:`getReqs`

    """
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

def pruneReqs(reqs):
    """
    Prune the requirements dict retrieved by ``getReqsFrom*``
    functions. Removes the ``dev`` section if found and
    removes sections with no requirements found. This helps
    reduce the output of ``getInfo``, since ``[dev]`` is a
    list of requirements which include most other sections.

    Parameters
    ----------
    reqs : dict
        Requirements dictionary.
        See format of return type of :func:`getReqs`

    """
    removed = set()
    for section in reqs:
        if all(x[1] is None for x in reqs[section]):
            removed.add(section)

    if "dev" in reqs:
        removed.add("dev")

    for section in removed:
        reqs.pop(section)

    return reqs

def getReqsFromRepo(path, version):
    """
    Get all requirements of the PyUnity package from
    either the pyproject.toml file or the requirements.txt
    file found in the repository.

    Parameters
    ----------
    path : pathlib.Path
        Path of the repository
    version : function
        Function to get package version. Should be
        imported from ``importlib.metadata`` or
        ``importlib_metadata``.

    Returns
    -------
    dict
        See format of return type of :func:`getReqs`

    """
    print("Warning: PyUnity not ran as an installed package")
    orig = os.getcwd()
    os.chdir(path.parent.parent)
    getRepoInfo()
    reqs = getReqsFromToml(version)
    if reqs is not None:
        reqs = pruneReqs(reqs)
        if len(reqs) == 0:
            print("Warning: no reqs found in pyproject.toml")
            reqs = None
    if reqs is None:
        if os.path.isfile("requirements.txt"):
            reqs = {"": []}
            with open("requirements.txt") as f:
                for item in f.read().rstrip().split("\n"):
                    name = formatName(item)
                    reqs[""].append((name, version(name)))
        else:
            print("Warning: No requirements.txt file found")

    os.chdir(orig)
    return reqs

def getReqsFromDistribution(dist, version, gitInfo=True):
    """
    Get all requirements of the PyUnity package from
    either the pyproject.toml file or the requirements.txt
    file found in the repository.

    Parameters
    ----------
    dist : importlib.metadata.Distribution
        Distribution object of PyUnity
    version : function
        Function to get package version. Should be
        imported from ``importlib.metadata`` or
        ``importlib_metadata``.
    gitInfo : bool
        If True, print git repository info

    Returns
    -------
    dict
        See format of return type of :func:`getReqs`

    """
    if gitInfo:
        data = json.loads(dist.read_text("version.json"))
        if data is not None:
            print("Git commit hash:", data["revision"])
            print("Local commit:", data["local"])
        else:
            print("Warning: version.json not found")

    discriminant = " ; extra == '"
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
    """
    Print system info and versions of Python and PyUnity,
    to be used in bug reports.

    """
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
    """
    Get requirements for PyUnity from multiple sources.

    Returns
    -------
    dict
        Dictionary of requirements, with keys for
        optional dependencies. The ``""`` key is
        for install_requires requirements.

    """
    if sys.version_info >= (3, 8):
        from importlib.metadata import (PackageNotFoundError, version,
                                        distribution)
    elif pkgutil.find_loader("importlib_metadata") is not None:
        from importlib_metadata import (PackageNotFoundError, distribution,
                                        version)
    else:
        print("Warning: Python version less than 3.8 but no importlib_metadata found")
        return None

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
            dist = distribution("pyunity")
        except PackageNotFoundError:
            print("Warning: could not find pyunity distribution info")
            reqs = None
        else:
            reqs = getReqsFromDistribution(dist, getVersion, not repoChecked)
            if reqs is not None:
                reqs = pruneReqs(reqs)

    return reqs

def printReqs(reqs):
    """
    Print requirements found from :func:`getReqs`.

    Parameters
    ----------
    reqs : dict
        See format of return type of :func:`getReqs`
    """
    print("Dependencies:")
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

def printInfo():
    """
    Print system info, get requirements and print them. Used
    by the PyUnity command ``python -m pyunity -v``.

    """
    printSystemInfo()
    print()
    reqs = getReqs()
    if reqs is not None:
        print()
        printReqs(reqs)
