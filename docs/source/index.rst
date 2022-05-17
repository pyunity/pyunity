===================================
Welcome to PyUnity's documentation!
===================================

Version 0.9.0 (in development)
##############################
PyUnity is a pure Python 3D Game Engine that
was inspired by the structure of the Unity
Game Engine. This does not mean that PyUnity
are bindings for the UnityEngine. However,
this project has been made to facilitate
any programmer, beginner or advanced, novice
or veteran.

Disclaimer
----------
As we have said above, this is not a set of
bindings for the UnityEngine, but a pure
Python library to aid in making 3D games in
Python.

Installing
----------
To install PyUnity for Linux distributions
based on Ubuntu or Debian, use::

    > pip3 install pyunity

To install PyUnity for other operating systems,
use pip::

    > pip install pyunity

Alternatively, you can clone the repository
to build the package from source. The latest
version is on the master branch and you can
build as follows::

    > git clone https://github.com/pyunity/pyunity
    > git checkout master
    > pip install .

The latest builds are on the ``develop`` branch
which is the default branch. These builds are
sometimes broken, so use at your own risk. ::

    > git clone https://github.com/pyunity/pyunity
    > pip install .

Its only dependencies are PyOpenGL, PySDL2,
Pillow and PyGLM. Microsoft Visual
C++ Build Tools are required on Windows
for building yourself. GLFW can be optionally
installed if you would like to use the GLFW
window provider.

Links
-----
For more information check out :doc:`the API documentation <api>`.

If you would like to contribute, please
first see the `contributing guidelines <https://github.com/pyunity/pyunity/blob/develop/docs/contributing.md>`_,
check out the latest `issues <https://github.com/pyunity/pyunity/issues>`_
and then make a `pull request <https://github.com/pyunity/pyunity/pulls>`_.

.. toctree::
    :maxdepth: 1
    :caption: Contents:

    releases
    tutorials/tutorials
    links
    license
    api

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
