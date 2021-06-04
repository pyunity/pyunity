Welcome to PyUnity's documentation!
===================================
PyUnity is a Python implementation of the
Unity Engine, written in C++. This is just
a fun project and many features have been
taken out to make it as easy as possible
to create a scene and run it.

Installing
----------
To install PyUnity for Linux distributions
based on Ubuntu or Debian, use::

   > pip3 install pyunity

To install PyUnity for other operating systems,
use pip::

   > pip install pyunity

Alternatively, you can clone the repository
`here <https://github.com/rayzchen/pyunity>`_
to build the package from source. Then use
`setup.py` to build. Note that it will install
Cython to compile.

   > python setup.py install

Its only dependencies are PyOpenGL, Pygame,
GLFW, Pillow and PyGLM.

To install PyGame on Linux, use:

   > pip3 install pygame

After installation, run an example using this
command:

   > python -m pyunity 3

.. toctree::
   :maxdepth: 4
   :caption: Contents:

   releases
   tutorials
   links
   license
   pyunity


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
