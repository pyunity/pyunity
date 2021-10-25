from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="pyunity-stubs",
    version="0.8.3",
    author="Ray Chen",
    author_email="tankimarshal2@gmail.com",
    description="Stub files for the PyUnity package",
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
    python_requires='>=3.6',
    packages=["pyunity"],
    install_requires=["pyunity==0.8.3"],
    package_data={"pyunity": ["*.pyi", "*/*.pyi"]},
    zip_safe=False,
)
