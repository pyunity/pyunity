# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

import json
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
# from types import ModuleType
# from unittest.mock import Mock
# sys.modules["sdl2"] = Mock()
# sys.modules["sdl2.sdlmixer"] = Mock()
# sys.modules["sdl2.ext"] = Mock()
# sys.modules["sdl2.video"] = Mock()
# sys.modules["glfw"] = Mock()
# sys.modules["OpenGL"] = Mock()
# sys.modules["OpenGL.GL"] = Mock()
# sys.modules["OpenGL.GLU"] = Mock()
# sys.modules["OpenGL.GLUT"] = Mock()
# os.environ["PYUNITY_INTERACTIVE"] = "0"
if "cython" not in os.environ:
    os.environ["cython"] = "1"

# import pyunity

def checkLicense():
    files = [
        "prepare.py", "setup.py", # Root files
        os.path.join("stubs", "setup.py"), # Stub setup
        *glob.glob("stubs/**/*.pyi", recursive=True),
        *glob.glob("tests/**/*.py", recursive=True),
        *glob.glob("pyunity/**/*.py", recursive=True),
    ]

    with open("LICENSE") as f:
        content = f.read()
    header = "# " + content.split("\n")[2] + "\n"
    header += "# This file is licensed under the MIT License.\n"
    header += "# See https://docs.pyunity.x10.bz/en/latest/license.html\n\n"
    for file in files:
        with open(file) as f:
            contents = f.read()
        if contents.startswith("#"):
            continue
        if not contents.startswith(header):
            with open(file, "w") as f:
                f.write(header)
                f.write(contents)

def checkWhitespace():
    for file in glob.glob("**/*.py", recursive=True) + \
            glob.glob("**/*.pyi", recursive=True):
        with open(file, encoding="utf8") as f:
            contents = f.read().rstrip()

        lines = contents.split("\n")
        for i in range(len(lines)):
            if lines[i].isspace():
                lines[i] = ""
        lines.append("")

        with open(file, "w", encoding="utf8") as f:
            f.write("\n".join(lines))

def parseSingleFile(path):
    current = multiprocessing.current_process()
    print(f"Worker-{current.pid}: correcting", path)

    import autopep8
    autopep8.main(["autopep8", "-i", "--ignore",
                "E26,E301,E302,E305,E401,E402,E501",
                path])

def parseCode(nthreads=None):
    if pkgutil.find_loader("autopep8") is None:
        raise Exception("autopep8 is needed to parse the source code.\n" +
                        "Install using \"pip install autopep8\".")

    if nthreads is None:
        nthreads = os.cpu_count()
    pool = multiprocessing.Pool(nthreads, initWorker)
    paths = glob.glob("pyunity/**/*.py", recursive=True)
    paths.append("setup.py")
    paths.append("cli.py")

    result = pool.map_async(parseSingleFile, paths)
    try:
        result.get(0xFFF)
    except Exception:
        pool.terminate()
        pool.join()
        raise

def getPackages(module="pyunity"):
    os.environ["PYUNITY_CHANGE_MODULE"] = "0"
    if isinstance(module, str):
        module = importlib.import_module(module)
    for _, name, ispkg in pkgutil.iter_modules(module.__path__):
        if ispkg:
            continue
        if "__" in name or name == "providers" or name == "config" or "example" in name:
            continue
        mod = importlib.import_module(module.__name__ + "." + name)
        if ispkg:
            getPackages(mod)
        if hasattr(mod, "__all__"):
            original = set(mod.__all__)
        else:
            original = set()
        new = set()
        for x in dir(mod):
            val = getattr(mod, x)
            if inspect.isclass(val) or inspect.isfunction(val):
                if x[0].isupper() and val.__module__ == mod.__name__:
                    new.add(x)
            elif isinstance(val, (int, str, bool, list, dict)) and x[0].isupper():
                new.add(x)
        if original != new:
            added = json.dumps(list(new - original))
            removed = json.dumps(list(original - new))
            print(mod.__name__, "Add", added, "Remove", removed)

def checkMissing():
    import pyunity
    getPackages(pyunity)

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

def cythonizeSingleFile(path):
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
            cythonize(path, quiet=True, compiler_directives=directives)
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

def initWorker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def cythonize(nthreads=None):
    if os.environ["cython"] != "1":
        return
    if pkgutil.find_loader("cython") is None:
        raise Exception("Cython is needed to create CPython extensions.")
    cythonVer = version.parse(importlib.metadata.version("cython"))
    if cythonVer < version.parse("3.0.0a8"):
        raise Exception(" - ".join([
            "Cython version must be at least 3.0.0a8",
            "install using pip install \"cython>=3.0.0a8\""]))
    if os.path.exists("src"):
        shutil.rmtree("src")

    if nthreads is None:
        nthreads = os.cpu_count()
    pool = multiprocessing.Pool(nthreads, initWorker)
    paths = glob.glob("pyunity/**/*.*", recursive=True)

    result = pool.map_async(cythonizeSingleFile, paths)
    try:
        result.get(0xFFF)
    except Exception:
        pool.terminate()
        pool.join()
        raise

def main():
    if len(sys.argv) == 1:
        checkLicense()
        checkWhitespace()
        parseCode()
        cythonize()
    else:
        for item in sys.argv[1:]:
            if item in globals():
                globals()[item]()

if __name__ == "__main__":
    main()
