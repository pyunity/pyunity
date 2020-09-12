from setuptools import setup, find_packages
import os, sys, subprocess, pyunity

def _run_command(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=sys.stderr)
    process.communicate()
    return process.wait()

desc = pyunity.__doc__.split("\n")
desc_new = [
    "# PyUnity", "",
    "[![Documentation Status](https://readthedocs.org/projects/pyunity/badge/?version=latest)]" + \
        "(https://pyunity.readthedocs.io/en/latest/?badge=latest)"
]
skip = 0
for i in range(len(desc)):
    if skip: skip = 0; continue
    if i != len(desc) - 1 and len(set(desc[i + 1])) == 1:
        if desc[i + 1][0] == "-":
            desc_new.append("### " + desc[i])
            skip = 1
        elif desc[i + 1][0] == "=":
            desc_new.append("## " + desc[i])
            skip = 1
    else:
        if "create a new pull request" in desc[i]:
            desc[i] = desc[i].replace(
                "create a new pull request",
                "[create a new pull request](https://github.com/rayzchen/pyunity/pulls)"
            )
        desc_new.append(desc[i])

with open("README.md", "w") as f:
    for line in desc_new:
        f.write(line + "\n")

with open("README.md", "r") as fh:
    long_description = fh.read()

print("Updating cythonize packages...")
for path, subdirs, files in os.walk("pyunity"):
    for name in files:
        p = os.path.join(path, name)
        if "__" in name:
            continue
        if not name.lower().endswith(".py"):
            continue
        print("Cythonizing " + name)
        _run_command("cythonize --3str -q -i " + p)
        print("Done")
print("Cythonized packages updated")
print("Removing C files")
for path, subdirs, files in os.walk(os.getcwd()):
    for name in files:
        p = os.path.join(path, name)
        name = p[1 + len(os.getcwd()):].replace("\\", "/")
        if name.lower().endswith(".c"):
            os.remove(p)
print("Done")

setup(
    name = "pyunity",
    version = pyunity.__version__,
    author = "Ray Chen",
    author_email = "tankimarshal2@gmail.com",
    description = "A Python implementation of the Unity Engine",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github/rayzchen/PyUnity",
    packages = find_packages(),
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires = [
        "glfw",
        "pygame",
        "pyopengl",
    ],
    python_requires = '>=3.7',
)
