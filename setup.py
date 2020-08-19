from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "pyunity",
    version = "0.0.1",
    author = "Ray Chen",
    author_email = "tankimarshal2@gmail.com",
    description = "A Python implementation of the Unity Engine",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github/rayzchen/PyUnity",
    packages = find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
    install_requires = [
        "glfw",
        "pygame",
        "pyopengl",
    ],
    python_requires = '>=3.7',
)