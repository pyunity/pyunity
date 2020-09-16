from setuptools import setup, find_packages, Extension
import os, sys, subprocess, pyunity, glob, shutil

def _run_command(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=sys.stderr)
    process.communicate()
    return process.wait()

desc = pyunity.__doc__.split("\n")
desc_new = [
    "# PyUnity", "",
    "".join([
        "[![Documentation Status](https://readthedocs.org/projects/pyunity/badge/?version=latest)]",
        "(https://pyunity.readthedocs.io/en/latest/?badge=latest) ",
        "[![License](https://img.shields.io/pypi/l/pyunity.svg?v=1)]",
        "(https://pypi.python.org/pypi/pyunity)",
        "[![PyPI version](https://img.shields.io/pypi/v/pyunity.svg?v=1)]",
        "(https://pypi.python.org/pypi/pyunity) ",
        "[![Python version](https://img.shields.io/badge/python-3-blue.svg?v=1)]",
        "(https://img.shields.io/badge/python-3-blue.svg?v=1) ",
        "[![Commits since last release](https://img.shields.io/github/commits-since/rayzchen/pyunity/0.0.5.svg",
        ")](https://github.com/rayzchen/pyunity/compare/0.0.5...master)",
    ])
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

if "a" not in os.environ:
    if os.path.exists("src"): shutil.rmtree("src")
    for dirpath, dirs, files in os.walk("pyunity"):
        for file in files:
            if file.lower().endswith(".py") or file.endswith(".mesh"):
                print(file)
                if file.startswith("__") or file.endswith(".mesh"):
                    srcPath = os.path.join(dirpath, file)
                    op = shutil.copy
                else:
                    os.system("cythonize -3 -q " + os.path.join(dirpath, file))
                    srcPath = os.path.join(dirpath, file)[:-2] + "c"
                    op = shutil.move
                destPath = os.path.join("src", os.path.dirname(srcPath[8:]))
                try: os.makedirs(destPath)
                except: pass
                op(srcPath, destPath)

c_files = glob.glob("src/**/*.c", recursive = True)
mesh_files = glob.glob("src/**/*.mesh", recursive = True)

setup(
    name = "pyunity",
    version = pyunity.__version__,
    author = "Ray Chen",
    author_email = "tankimarshal2@gmail.com",
    description = "A Python implementation of the Unity Engine",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github/rayzchen/PyUnity",
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
    package_dir = {"pyunity": "src"},
    packages = ["pyunity"] + ["pyunity." + package for package in find_packages(where = "src")],
    ext_package = "pyunity",
    ext_modules = [Extension(file[4:-2].replace(os.path.sep, "."), [file]) for file in c_files],
    package_data = {"pyunity": [file[4:] for file in mesh_files]},
)
