Cython update, where everything is cythonized.
First big update.

Features:

- Much more optimized rendering with Cython
- A new example
- Primitives
- Scaling
- Tutorials
- New color theme for documentation
- Timer decorator
- Non-interactive mode
- Frustrum culling
- Overall optimization

Notes:

- The FPS config will not have a change due to
  the inability of cyclic imports in Cython.
- You can see the c code used in Cython in the
  src folder.
- When installing with ``setup.py``, you can set
  the environment variable ``a`` to anything but
  an empty string, this will disable recreating
  the c files. For example:

        > set a=1
        > python setup.py install