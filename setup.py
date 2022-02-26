from setuptools import setup, find_packages, Extension
import os
import glob
if "cython" not in os.environ:
    os.environ["cython"] = "1"

with open("README.md", "r") as fh:
    long_description = fh.read()

if os.environ["cython"] == "1":
    if not os.path.isdir("src"):
        if not os.path.isfile("prepare.py"):
            raise Exception("\n".join([
                "Source directory `src` not found but `prepare.py` does not exist.",
                "If this is not a local clone of the repository, please report",
                "this as a bug at https://github.com/pyunity/pyunity/issues."
            ]))
        import prepare
        prepare.cythonize()
    c_files = glob.glob("src/**/*.c", recursive=True)
    data_files = list(filter(lambda a: ".c" not in a,
                      glob.glob("src/**/*.*", recursive=True)))
    config = {
        "package_dir": {"pyunity": "src"},
        "packages": ["pyunity"] + ["pyunity." + package for package in find_packages(where="pyunity")],
        "ext_package": "pyunity",
        "ext_modules": [Extension(file[4:-2].replace(os.path.sep, "."), [file]) for file in c_files],
        "package_data": {"pyunity": [file[4:] for file in data_files]},
    }
else:
    data_files = glob.glob("pyunity/**/*.mesh", recursive=True) + \
        glob.glob("pyunity/**/*.ogg", recursive=True)
    config = {
        "packages": ["pyunity"] + ["pyunity." + package for package in find_packages(where="pyunity")],
        "package_data": {"pyunity": [file[8:] for file in data_files]},
    }

setup(
    name="pyunity",
    version="0.8.3",
    author="Ray Chen",
    author_email="tankimarshal2@gmail.com",
    description="A Python implementation of the Unity Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pyunity/pyunity",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=[
        "pyopengl",
        "pillow",
        "pysdl2",
        "pysdl2-dll",
        "pyglm",
        "glfw",
    ],
    python_requires='>=3.6',
    **config,
)
