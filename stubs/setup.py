from setuptools import setup

setup(
    name="pyunity-stubs",
    version="0.8.0",
    author="Ray Chen",
    author_email="tankimarshal2@gmail.com",
    description="Stub files for the PyUnity package",
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
    packages=["pyunity==0.8.0"],
    package_data={"pyunity": ["*.pyi", "*/*.pyi"]},
    zip_safe=False,
)
