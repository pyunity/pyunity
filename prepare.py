## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""
A script that contains commands to manage the PyUnity project.

Run this script with ``python prepare.py cmd1 cmd2 ...``

"""

import json
import re
import os
import glob
import shutil
import pkgutil
import sys
import signal
import multiprocessing
import importlib
import importlib.metadata
import inspect
from setuptools._vendor.packaging import version # avoid pip install
if "cython" not in os.environ:
    os.environ["cython"] = "1"

def initWorker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

with open("LICENSE") as f:
    content = f.read()
licenseHeader = "## " + content.split("\n")[2] + "\n"
licenseHeader += "## This file is licensed under the MIT License.\n"
licenseHeader += "## See https://docs.pyunity.x10.bz/en/latest/license.html\n\n"
def checkLicense():
    """
    Make sure that the PyUnity license header is present in all
    module files, stub files, test suites and helper scripts.

    Affected helper scripts are:
    - ``prepare.py``
    - ``setup.py``

    """
    files = [
        "prepare.py", "setup.py", # Root files
        *glob.glob("stubs/**/*.pyi", recursive=True),
        *glob.glob("tests/**/*.py", recursive=True),
        *glob.glob("pyunity/**/*.py", recursive=True),
    ]

    for file in files:
        with open(file) as f:
            contents = f.read()
        if contents.startswith("#"):
            continue
        if not contents.startswith(licenseHeader):
            with open(file, "w") as f:
                f.write(licenseHeader)
                f.write(contents)

def checkWhitespace():
    """
    Checks whitespace in all files in the ``pyunity``
    and ``stubs`` packages, the `docs/` folder and the
    ``tests/`` suites.

    Trailing whitespace is removed and one empty line is
    enforced at the end.

    """
    files = ["prepare.py", "setup.py"]
    for folder in ["docs", "pyunity", "stubs", "tests"]:
        files.extend(glob.glob(folder + "**/*.py", recursive=True))
        files.extend(glob.glob(folder + "**/*.pyi", recursive=True))

    for file in files:
        with open(file, encoding="utf8") as f:
            contents = f.read().rstrip()

        lines = contents.split("\n")
        for i in range(len(lines)):
            lines[i] = lines[i].rstrip()
            if lines[i].isspace():
                lines[i] = ""
        lines.append("")

        content = "\n".join(lines)
        while "\n\n\n" in lines:
            content.replace("\n\n\n", "\n\n")
        with open(file, "w", encoding="utf8") as f:
            f.write(content)

def parseSingleFile(path):
    current = multiprocessing.current_process()
    print(f"Worker-{current.pid}: correcting", path)

    import autopep8
    autopep8.main(["autopep8", "-i", "--ignore",
                   "E26,E301,E302,E305,E401,E402,E501",
                   path])

def parseCode(nthreads=None):
    """
    Uses autopep8 to parse all files in the ``pyunity``
    and ``stubs`` packages, the `docs/` folder and the
    ``tests/`` suites.

    Parameters
    ----------
    nthreads : int, optional
        Number of threads to use, by default None

    Raises
    ------
    Exception
        Propagated from the worker threads.

    """
    if pkgutil.find_loader("autopep8") is None:
        raise Exception("autopep8 is needed to parse the source code.\n" +
                        "Install using \"pip install autopep8\".")

    if nthreads is None:
        nthreads = os.cpu_count()
    pool = multiprocessing.Pool(nthreads, initWorker)
    paths = ["prepare.py", "setup.py"]
    for folder in ["docs", "pyunity", "stubs", "tests"]:
        paths.extend(glob.glob(folder + "**/*.py", recursive=True))
        paths.extend(glob.glob(folder + "**/*.pyi", recursive=True))

    result = pool.map_async(parseSingleFile, paths)
    try:
        result.get(0xFFF)
    except Exception:
        pool.terminate()
        pool.join()
        raise

moduleVars = {}
def getPackages(parentModule="pyunity"):
    """
    Check the ``__all__`` attribute of all submodules and subpackages
    using subclasses of :class:`ModuleExportControlMixin`.

    Parameters
    ----------
    parentModule : str, optional
        The package to check, by default "pyunity"

    """
    # Keep original __module__ attributes and expose Mathf functions
    os.environ["PYUNITY_SPHINX_CHECK"] = "1"
    from pyunity.values import IgnoredMixin, IncludeInstanceMixin, IncludeMixin
    if isinstance(parentModule, str):
        parentModule = importlib.import_module(parentModule)

    for _, name, ispkg in pkgutil.iter_modules(parentModule.__path__):
        if "example" in name:
            # Includes pyunity.examples and all of its subpackages
            continue
        module = importlib.import_module(parentModule.__name__ + "." + name)
        if ispkg:
            # how pyunity.window.providers is dealt with is to be decided
            if name != "providers":
                # Recursive descent into subpackage
                getPackages(module)

        original = set(getattr(module, "__all__", set()))
        new = set()

        for variable in dir(module):
            value = getattr(module, variable)
            if inspect.isclass(value) or inspect.isfunction(value):
                if value.__module__ == module.__name__ or (
                        ispkg and value.__module__.startswith(module.__name__)):
                    # value was not imported from a submodule
                    if inspect.isclass(value):
                        if issubclass(value, IncludeMixin):
                            new.add(variable)
                        elif not issubclass(value, IgnoredMixin) and variable[0].isupper():
                            new.add(variable)
                        elif value is IgnoredMixin:
                            new.add(variable)
                    else:
                        # value is a function
                        if variable[0].isupper():
                            new.add(variable)
            elif inspect.ismodule(value):
                if value.__package__ == module.__name__ and variable[0].isupper():
                    # value is a submodule of this module, imported with a capital letter
                    new.add(variable)
            elif isinstance(value, (int, float, str, bool, list, dict)) and variable[0].isupper():
                # Constants
                new.add(variable)
            elif variable.isupper() and not variable.startswith("_"):
                # Forced constants (IncludeInstanceMixin not needed)
                new.add(variable)
            elif isinstance(value, IncludeInstanceMixin):
                # value was defined in this module
                if getattr(value, "__module__", "") == module.__name__:
                    new.add(variable)

        moduleVars[module.__name__] = {
            "__all__": sorted(list(new)),
            "__doc__": module.__doc__
        }
        if original != new:
            added = json.dumps(sorted(list(new - original)))
            removed = json.dumps(sorted(list(original - new)))
            moduleFile = module.__name__.replace(".", os.path.sep) + ".py"
            if ispkg:
                moduleFile = moduleFile[:-3] + os.path.sep + "__init__.py"
            print(moduleFile, "Add", added, "Remove", removed)

def formatAll(list, width=79):
    """
    Formats the ``__all__`` attribute of a module
    with line wrapping.

    Parameters
    ----------
    list : list
        List of variable names exported
    width : int, optional
        Maximum width of a line, defaults to 79

    Returns
    -------
    string
        The formatted list

    """
    text = "__all__ = ["
    indent = len(text)
    limit = width - indent
    length = 0
    for item in list:
        length += len(item) + 4
        if length > limit:
            # Line wrap
            text += "\n" + " " * indent
            # 4 includes ("", )
            length = len(item) + 4
        text += "\"" + item + "\", "
    if len(list):
        # Remove comma if non-empty
        text = text[:-2]
    text += "]"
    return text

def checkMissing():
    """
    Runs :func:`getPackages` to gather module information
    then checks stub files for three things:

    1. if they have the correct license header
    2. if they have the correct module docstring
    3. if they have the correct ``__all__``

    """
    global moduleVars
    moduleVars = {}
    getPackages("pyunity")
    for file in glob.glob("stubs/pyunity/*.pyi", recursive=True):
        moduleName = file[6:-4].replace(os.path.sep, ".")
        if moduleName.endswith(".__init__"):
            # Needs special handling, better to do manually
            continue
        # if "example" in moduleName:
        #     continue

        with open(file) as f:
            contents = f.read()
        fileHeader = licenseHeader
        if moduleVars[moduleName]["__doc__"] is not None:
            fileHeader += '"""' + moduleVars[moduleName]["__doc__"] + '"""\n\n'
        if not contents.startswith(fileHeader):
            print(file, "has wrong header and docstring, see", file[6:-1])

        if moduleVars[moduleName]["__all__"] == []:
            continue
        allVars = re.search(r"__all__ = \[(.*?)\]", contents, re.DOTALL)
        if allVars is None:
            print(file, "does not have __all__, expected:")
            allVars = ""
        else:
            # Replace all newlines and indents
            allVars = re.sub(r"\s+", " ", allVars.group(1))

        allSet = set(allVars[1:-1].split("\", \""))
        if allSet == set(moduleVars[moduleName]["__all__"]):
            continue
        elif allVars != "":
            print(file, "does not have correct __all__, expected:")
        expectedAllText = formatAll(moduleVars[moduleName]["__all__"])
        print(expectedAllText)

# items = []

# for name in dir(pyunity):
#     if not (isinstance(getattr(pyunity, name), ModuleType) and
#             name.islower() or name.startswith("__")):
#         items.append(name)

# with open(os.path.join("pyunity", "__init__.py"), "r") as f:
#     content = f.read()

# index = content.index("# __all__ starts here")
# end = content.index("# __all__ ends here") + 19
# before = content[:index]
# after = content[end:]
# text = "# __all__ starts here\n__all__ = ["
# line = ""
# for item in items:
#     if len(line) < 50:
#         line += "\"" + item + "\", "
#     else:
#         text += line[:-1] + "\n           "
#         line = "\"" + item + "\", "

# text += line[:-2] + "]\n# __all__ ends here"

# with open(os.path.join("pyunity", "__init__.py"), "w") as f:
#     f.write(before + text + after)

# desc = pyunity.__doc__.split("\n")
# descNew = [
#     "# PyUnity", "",
#     "".join([
#         "[![Documentation Status](https://readthedocs.org/projects/pyunity/badge/?version=latest)]",
#         "(https://pyunity.readthedocs.io/en/latest/?badge=latest)\n",
#         "[![License](https://img.shields.io/pypi/l/pyunity.svg?logo=python&logoColor=FBE072)]",
#         "(https://github.com/pyunity/pyunity/blob/develop/LICENSE)\n",
#         "[![PyPI version](https://img.shields.io/pypi/v/pyunity.svg?logo=python&logoColor=FBE072)]",
#         "(https://pypi.python.org/pypi/pyunity)\n",
#         "[![Python version](https://img.shields.io/pypi/pyversions/pyunity.svg?logo=python&logoColor=FBE072)]",
#         "(https://pypi.python.org/pypi/pyunity)\n",
#         "[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/pyunity/pyunity.svg?logo=lgtm)]",
#         "(https://lgtm.com/projects/g/pyunity/pyunity/context:python)\n",
#         "[![Total alerts](https://img.shields.io/lgtm/alerts/g/pyunity/pyunity.svg?logo=lgtm&logoWidth=18)]",
#         "(https://lgtm.com/projects/g/pyunity/pyunity/alerts/)\n",
#         "[![Build status](https://ci.appveyor.com/api/projects/status/ucpcthqu63llcgot?svg=true)]",
#         "(https://ci.appveyor.com/project/pyunity/pyunity)\n",
#         "[![Discord](https://img.shields.io/discord/835911328693616680?logo=discord&label=discord)]",
#         "(https://discord.gg/zTn48BEbF9)\n",
#         "[![Gitter](https://badges.gitter.im/pyunity/community.svg)]",
#         "(https://gitter.im/pyunity/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)\n",
#         "[![GitHub Repo stars](https://img.shields.io/github/stars/pyunity/pyunity?logo=github)]",
#         "(https://github.com/pyunity/pyunity/stargazers)",
#     ])
# ]
# skip = 0
# for i in range(len(desc)):
#     if skip:
#         skip = 0
#         continue
#     if i != len(desc) - 1 and len(set(desc[i + 1])) == 1:
#         if desc[i + 1][0] == "-":
#             descNew.append("### " + desc[i])
#             skip = 1
#         elif desc[i + 1][0] == "=":
#             descNew.append("## " + desc[i])
#             skip = 1
#     else:
#         if "create a new pull request" in desc[i]:
#             desc[i] = desc[i].replace(
#                 "create a new pull request",
#                 "[create a new pull request](https://github.com/pyunity/pyunity/pulls)"
#             )
#         if desc[i] == "`here <https://github.com/pyunity/pyunity>`_":
#             continue
#         descNew.append(desc[i].replace("::", ":"))

# with open("README.md", "w") as f:
#     for line in descNew:
#         f.write(line + "\n")

def getFiles():
    """
    Gets a list of all files to be included in generated
    packages.

    Returns
    -------
    tuple
        A tuple of two lists. The first list contains all
        of the cython output C files, and the second list
        contains all other files, including resources and
        files that are not cythonized.

    """
    cythonized = []
    copied = []

    for path in glob.glob("pyunity/**/*.*", recursive=True):
        _, file = os.path.split(path)
        if (file.endswith(".py") and not file.startswith("__") and
                file != "_version.py" and
                not path.startswith(os.path.join(
                    "pyunity", "window", "providers"))):
            destPath = os.path.join("src", path[8:-2] + "c")
            cythonized.append(destPath)
        else:
            destPath = os.path.join("src", path[8:])
            copied.append(destPath)

    return cythonized, copied

def packageSingleFile(path):
    """
    Cythonize or copy a package file.

    Parameters
    ----------
    path : str
        Path to package file

    Raises
    ------
    Exception
        If a file failed to cythonize

    """
    from Cython.Build import cythonize
    directives = {"language_level": "3"}

    if path.endswith(".pyc") or path.endswith(".pyo"):
        return

    current = multiprocessing.current_process()
    print(f"Worker-{current.pid}: cythonizing", path)
    dirpath, file = os.path.split(path)
    if (file.endswith(".py") and not file.startswith("__") and
            file != "_version.py" and
            not path.startswith(os.path.join(
                "pyunity", "window", "providers"))):
        srcPath = path[:-2] + "c"
        try:
            cythonize(path, quiet=True, compiler_directives=directives,
                      show_all_warnings=True)
        except:
            os.remove(srcPath)
            raise Exception(f"Cythonization of `{path}` failed.") from None
        op = shutil.move
    else:
        # _version.py should go here
        srcPath = os.path.join(dirpath, file)
        op = shutil.copy
    destPath = os.path.join("src", os.path.dirname(srcPath[8:]))
    os.makedirs(destPath, exist_ok=True)
    op(srcPath, destPath)

minimumCythonVersion = "3.0.0a8"
def cythonize(nthreads=None):
    """
    Loop through all files in the package and prepares them
    for distribution, cythonizing them if necessary.

    Parameters
    ----------
    nthreads : int, optional
        Number of threads to use. If ``None`` is passed (the
        default) then the number of cpu threads is used.

    Raises
    ------
    Exception
        If Cython is not installed or has the wrong version

    """
    if os.environ["cython"] != "1":
        return
    if pkgutil.find_loader("cython") is None:
        raise Exception("Cython is needed to create CPython extensions.")
    cythonVer = version.parse(importlib.metadata.version("cython"))
    if cythonVer < version.parse(minimumCythonVersion):
        raise Exception(" - ".join([
            "Cython version must be at least " + minimumCythonVersion,
            f"install using `pip install \"cython>={minimumCythonVersion}\"`"]))
    if os.path.exists("src"):
        shutil.rmtree("src")

    if nthreads is None:
        nthreads = os.cpu_count()
    pool = multiprocessing.Pool(nthreads, initWorker)
    paths = glob.glob("pyunity/**/*.*", recursive=True)

    result = pool.map_async(packageSingleFile, paths)
    try:
        result.get(0xFFF)
    except Exception:
        pool.terminate()
        pool.join()
        raise

def main():
    """
    Runs the specified commands from command line arguments
    or runs all of them if none given.

    """
    if len(sys.argv) == 1:
        checkLicense()
        checkWhitespace()
        parseCode()
        checkMissing()
        cythonize()
    else:
        for item in sys.argv[1:]:
            func = globals().get(item)
            if callable(func):
                func()
            else:
                print("Unrecognised command: " + item)

if __name__ == "__main__":
    main()
