import os
import glob
import shutil
import pkgutil
import sys
import importlib
import inspect
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
# os.environ["PYUNITY_TESTING"] = "1"
if "cython" not in os.environ:
    os.environ["cython"] = "1"

# import pyunity

def check_endings():
    if len(sys.argv) > 1:
        for file in glob.glob("**/*.py", recursive=True) + \
                glob.glob("**/*.pyi", recursive=True):
            with open(file) as f:
                contents = f.read()
            
            print(repr(contents[-1]))
            if not contents.endswith("\n"):
                contents += "\n"
            
            with open(file, "w") as f:
                f.write(contents)

def parse_code():
    if pkgutil.find_loader("autopep8") is None:
        raise Exception("autopep8 is needed to parse the source code.\n" +
                        "Install using \"pip install autopep8\".")
    import autopep8
    autopep8.main(["autopep8", "-i", "-r", "--ignore", "E301,E302,E305,E401,E402",
                "pyunity", "setup.py", "cli.py"])

def get_packages(module):
    for _, name, ispkg in pkgutil.iter_modules(module.__path__):
        if "__" in name or "Window" in name or name == "config" or "example" in name:
            continue
        mod = importlib.import_module(module.__name__ + "." + name)
        if ispkg:
            get_packages(mod)
        if hasattr(mod, "__all__"):
            original = set(mod.__all__)
        else:
            original = set()
        new = set([x for x in dir(mod) if ((inspect.isclass(getattr(mod, x)) or
                                        inspect.isfunction(getattr(mod, x))) and 
                                       x[0].isupper() and 
                                       getattr(mod, x).__module__ == mod.__name__)])
        if original != new:
            print(mod.__name__, "Add", list(new - original),
                  "Remove", list(original - new))

def check_missing():
    if len(sys.argv) > 1:
        import pyunity
        get_packages(pyunity)

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
# desc_new = [
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
#             desc_new.append("### " + desc[i])
#             skip = 1
#         elif desc[i + 1][0] == "=":
#             desc_new.append("## " + desc[i])
#             skip = 1
#     else:
#         if "create a new pull request" in desc[i]:
#             desc[i] = desc[i].replace(
#                 "create a new pull request",
#                 "[create a new pull request](https://github.com/pyunity/pyunity/pulls)"
#             )
#         if desc[i] == "`here <https://github.com/pyunity/pyunity>`_":
#             continue
#         desc_new.append(desc[i].replace("::", ":"))

# with open("README.md", "w") as f:
#     for line in desc_new:
#         f.write(line + "\n")

def cythonize(error=False):
    if os.environ["cython"] == "1":
        if pkgutil.find_loader("cython") is None:
            raise Exception("Cython is needed to create CPython extensions.")
        if os.path.exists("src"):
            shutil.rmtree("src")
        for path in glob.glob("pyunity/**/*.*", recursive=True):
            if path.endswith(".pyc"):
                continue
            dirpath, file = os.path.split(path)
            print(file)
            if file.endswith(".py") and not file.startswith("__"):
                code = os.system("cythonize -3 -q " + path)
                srcPath = path[:-2] + "c"
                if code != 0:
                    os.remove(srcPath)
                    if error:
                        raise Exception(f"Cythonization of `{path}` failed.")
                    break
                op = shutil.move
            else:
                srcPath = os.path.join(dirpath, file)
                op = shutil.copy
            destPath = os.path.join("src", os.path.dirname(srcPath[8:]))
            os.makedirs(destPath, exist_ok=True)
            op(srcPath, destPath)

def main():
    check_endings()
    parse_code()
    check_missing()
    cythonize()

if __name__ == "__main__":
    main()
