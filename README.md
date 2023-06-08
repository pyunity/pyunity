# PyUnity

[![Documentation Status](https://readthedocs.org/projects/pyunity/badge/?version=latest)](https://docs.pyunity.x10.bz/)
[![Documentation Website](https://img.shields.io/website?url=https%3A%2F%2Fdocs.pyunity.x10.bz)](https://docs.pyunity.x10.bz/)
[![License](https://img.shields.io/pypi/l/pyunity.svg?logo=python&logoColor=FBE072)](https://docs.pyunity.x10.bz/en/latest/license.html)
[![PyPI version](https://img.shields.io/pypi/v/pyunity.svg?logo=python&logoColor=FBE072)](https://pypi.python.org/pypi/pyunity)
[![Semantic versioning](https://img.shields.io/badge/semver-2.0.0-blue)](https://semver.org/)
[![Python version](https://img.shields.io/pypi/pyversions/pyunity.svg?logo=python&logoColor=FBE072)](https://pypi.python.org/pypi/pyunity)
[![Downloads](https://pepy.tech/badge/pyunity)](https://pepy.tech/project/pyunity)
[![Build status](https://ci.appveyor.com/api/projects/status/ucpcthqu63llcgot?svg=true)](https://ci.appveyor.com/project/pyunity/pyunity)
[![Testing](https://github.com/pyunity/pyunity/actions/workflows/coverage.yml/badge.svg)](https://github.com/pyunity/pyunity/actions/workflows/coverage.yml)
[![Languages](https://shields.io/github/languages/top/pyunity/pyunity)](https://github.com/pyunity/pyunity)
[![Languages](https://shields.io/github/issues/pyunity/pyunity)](https://github.com/pyunity/pyunity/issues)
[![Codecov](https://codecov.io/gh/pyunity/pyunity/branch/develop/graph/badge.svg)](https://codecov.io/gh/pyunity/pyunity)
[![Discord](https://img.shields.io/discord/835911328693616680?logo=discord&label=discord)](https://discord.gg/zTn48BEbF9)
[![Gitter](https://badges.gitter.im/pyunity/community.svg)](https://gitter.im/pyunity/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![GitHub Repo stars](https://img.shields.io/github/stars/pyunity/pyunity?logo=github)](https://github.com/pyunity/pyunity/stargazers)
[![GitHub commits](https://img.shields.io/github/commit-activity/m/pyunity/pyunity)](https://github.com/pyunity/pyunity/commits)
<!-- [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/pyunity/pyunity.svg?logo=lgtm)](https://lgtm.com/projects/g/pyunity/pyunity/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/pyunity/pyunity.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/pyunity/pyunity/alerts/) -->

## Version 0.9.0 (in development)
PyUnity is a pure Python 3D Game Engine that
was inspired by the structure of the Unity
Game Engine. It aims to be as close as possible
to Unity itself. This does not mean that PyUnity
are bindings for the UnityEngine. However,
this project has been made to facilitate
any programmer, beginner or advanced, novice
or veteran.

### Disclaimer
As we have said above, this is not a set of
bindings for the UnityEngine, but a pure
Python library to aid in making 3D games in
Python.

### Installing
To install PyUnity for Linux distributions
based on Ubuntu or Debian, use:

    > pip3 install pyunity

To install PyUnity for other operating systems,
use:

    > pip install pyunity

Alternatively, you can clone the repository
to build the package from source. The latest
stable version is on the master branch and
you can build as follows:

    > git clone https://github.com/pyunity/pyunity
    > git checkout master
    > pip install .

The latest unstable version is on the ``develop``
branch which is the default branch. These builds are
sometimes broken, so use at your own risk.

    > git clone https://github.com/pyunity/pyunity
    > pip install .

Its only dependencies are PyOpenGL, PySDL2,
Pillow and PyGLM. Microsoft Visual
C++ Build Tools are required on Windows
for building yourself, but it can be disabled by
setting the `cython` environment variable to
`0`, at the cost of being less optimized.
GLFW can be optionally installed if you would
like to use the GLFW window provider.

### Links

For more information check out
[the API documentation](https://pyunity.readthedocs.io/en/latest/).
There we offer some tutorials on the basics of
PyUnity, as well as all modules and utility functions
that come with it. Examples are located at subfolders in
[pyunity/examples](https://github.com/pyunity/pyunity/tree/develop/pyunity/examples)
so do be sure to check them out as a starting point.

If you would like to contribute, please
first see the [contributing guidelines](https://github.com/pyunity/pyunity/blob/develop/docs/contributing.md),
check out the latest [issues](https://github.com/pyunity/pyunity/issues)
and then make a [pull request](https://github.com/pyunity/pyunity/pulls).
