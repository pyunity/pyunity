========
Releases
========

v0.9.0
======
In development.

API
###
New features:

Module
------

- `RenderTarget` component which renders a Camera output to a texture
- `Mathf` module
- Coroutines and async functions
- Advanced component attribute settings
- Prefabs
- STL loading
- Mesh generation
- Customizable scene runner
- Shadow mapping
- Revamped project format
- Version and dependency info when running `python -m pyunity -v`
- Linux wheels audited with `auditwheel` on three different archs
- Environment variable documentation

Internal
########
New features:

Module
------

- Window provider organization

  - New window providers can be added with
    a respective Python package
  - Current window providers: GLFW, SDL2, GLUT (not fully supported), GLContext

- Rotation bugs fixed
- Separate EventLoops for rendering, physics and update
- PyUnity resource management
- Standardized code style and variable name case
- Import reorganization
- `pathlib.Path` usage
- Internal star imports removed
- Splash screen
- Better logging output

Repository
----------
- GitHub Actions integration
- Migration from unittest to PyTest
- Mypy integration
- Switch to using `pypa/build` instead of running `setup.py`
- Migration to a `pyproject.toml`-based project
- Automatic running of `prepare.py` when installing if needed
- GitHub issue forms
- New badges displayed on README

v0.8.4
======
An internal change-heavy update, but most of the API is untouched.

Changes:

- Python 3.10 support
- Orthographic camera projection
- Ortho camera example
- Fixed scaling and position issues
- A 2D tutorial
- Better documentation formatting
- Directional light type
- Skybox toggle

Download source code at
https://github.com/pyunity/pyunity/releases/tag/0.8.4

v0.8.3
======
Bugfix regarding Quaternion.eulerAngles.

To set the rotation of the camera using Euler angles,
use ``scene.mainCamera.localRotation.SetBackward(Vector3(...))``.

Download source code at
https://github.com/pyunity/pyunity/releases/tag/0.8.3

v0.8.2
======
Bugfix regarding ``Quaternion.FromDir``, ``Quaternion.Euler``,
``abstractmethod`` and 2D depth buffers.

Download source code at
https://github.com/pyunity/pyunity/releases/tag/0.8.2

v0.8.1
======
Bugfix regarding camera position updating and input axes.

Download source code at
https://github.com/pyunity/pyunity/releases/tag/0.8.1

v0.8.0
======
New features:

- Rewrote documentation and docstrings
- Reformatted code
- F string integration
- ``ImmutableStruct`` and ``ABCMeta`` metaclasses
   - The ``ABCMeta`` class has more features than the default Python ``abc`` module.
- Rewrote examples
- Combined many functions common to both Vector2 and Vector3 into a single Vector class.
   - If you want to implement your own Vector classes, subclass from Vector and implement
     the required abstract methods.
- Fixed quaternion and rotation maths
- Input axes and mouse input
- Multiple lights
- Different light types
- Window provider caching and checking
- Gui components
   - This includes buttons, checkboxes, images and text boxes
   - Rect transforms can be very flexible
   - Platform-specific font loading
- Stub package
   - This will work with editors such as VSCode and PyCharm, just install ``pyunity-stubs`` from pip

Stub package: https://pypi.org/project/pyunity-stubs

Download source code at
https://github.com/pyunity/pyunity/releases/tag/0.8.0

v0.7.1
======
Extra features used in the PyUnity Editor.

Changes:

- Code of Conduct and Contributing guides
- Rewrote most of the README to clear confusion about what PyUnity really is
- RGB and HSV
- Better GameObject deleting
- ShowInInspector and HideInInspector
- Dynamic lighting

Download source code at
https://github.com/pyunity/pyunity/releases/tag/0.7.1

v0.7.0
======
New features:

- Customizable skybox
- Editor integration
- Rewrote scene saving and loading
- PYUNITY_WINDOW_PROVIDER environment variable
- Fixed example 8

Editor GitHub:
https://github.com/pyunity/pyunity-gui

Download source code at
https://github.com/pyunity/pyunity/releases/tag/0.7.0

v0.6.0
======
Project structure update.

New features:

- Replaced Pygame with PySDL2
- Revamped audio module
- Fixed input bugs
- Added scene saving
- Added project saving
- Added project structure
- Automated win32 builds on Appveyor
- Removed redundant code from fixed function pipeline

Download source code at
https://github.com/pyunity/pyunity/releases/tag/0.6.0

v0.5.2
======
Small minor fix of shader inclusion in binary distributions.

Download source code at
https://github.com/pyunity/pyunity/releases/tag/0.5.2

v0.5.1
======
Bugfix that fixes the shaders and dependency management.

Download source code at
https://github.com/pyunity/pyunity/releases/tag/0.5.1

v0.5.0
======
Big rendering update that completely rewrites rendering code and optimizes it.

New features:

- Script loading
- Shaders
- Vertex buffer objects and vertex array objects
- Optimized rendering
- Colours
- Textures
- New lighting system
- New meshes and mesh loading

Download source code at
https://github.com/pyunity/pyunity/releases/tag/0.5.0

v0.4.0
======
Small release that has large internal changes.

New features:

- Added logger
- Moved around files and classes to make it more pythonic
- Rewrote docs
- Fixed huge bug that broke all versions from 0.2.0-0.3.1
- Clarified README.md

Download source code at
https://github.com/pyunity/pyunity/releases/tag/0.4.0

v0.3.1
======
Bugfix on basically everything because 0.3.0 was messed up.

Download source code at
https://github.com/pyunity/pyunity/releases/tag/0.3.1

v0.3.0
======
After a long break, 0.3.0 is finally here!

New features:

- Added key input (not fully implemented)
- Fixed namespace pollution
- Fixed minor bugs
- Window resizing implemented
- New Scene loading interface
- Python 3.9 support
- Finished pxd files
- LGTM Integration
- AppVeyor is now the main builder
- Code is now PEP8-friendly
- Added tests.py
- Cleaned up working directory

Download source code at
https://github.com/pyunity/pyunity/releases/tag/0.3.0

v0.2.1
======
Small bugfix around the AudioClip loading and inclusion of the OGG file in example 8.

Download source code at
https://github.com/pyunity/pyunity/releases/tag/0.2.1

v0.2.0
======
A CI integration update, with automated building from Appveyor and Travis CI.

Features:

- Shaded faces with crisp colours
- PXD files to optimize Cython further (not yet implemented fully)
- Scene changing
- FPS changes
- Better error handling
- Travis CI and AppVeyor integration
- Simple audio handling
- Changelogs in the dist folder of master
- Releases branch for builds from Travis
- Python 3.6 support
- 1 more example, bringing the total to 8

Download source code at
https://github.com/pyunity/pyunity/releases/tag/0.2.0

v0.1.0
======
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
- Frustum culling
- Overall optimization

Notes:

- The FPS config will not have a change due to
  the inability of cyclic imports in Cython.
- You can see the c code used in Cython in the
  src folder.
- When installing with ``setup.py``, you can set
  the environment variable ``a`` to anything but
  an empty string, this will disable recreating
  the c files. For example::

      > set a=1
      > pip install .

Download source code at
https://github.com/pyunity/pyunity/releases/tag/0.1.0


v0.0.5
======
Transform updates, with new features extending
GameObject positioning.

Features:

- Local transform
- Quaternion
- Better example loader
- Primitive objects in files
- Fixed jittering when colliding from an angle
- Enabled friction (I don't know when it was turned off)
- Remove scenes from SceneManager
- Vector division

Download source code at
https://github.com/pyunity/pyunity/releases/tag/0.0.5

v0.0.4
======
Physics update.

New features:

- Rigidbodies
- Gravity
- Forces
- Optimized collision
- Better documentation
- Primitive meshes
- PyUnity mesh files that are optimized for fast loading
- Pushed GLUT to the end of the list so that it has the least priority
- Fixed window loading
- Auto README.md updater

Download source code at
https://github.com/pyunity/pyunity/releases/tag/0.0.4

v0.0.3
======
More basic things added.

Features:

- Examples (5 of them!)
- Basic physics components
- Lighting
- Better window selection
- More debug options
- File loader for .obj files

Download source code at
https://github.com/pyunity/pyunity/releases/tag/0.0.3

v0.0.2
======
First proper release (v0.0.1 was
lost).

Features:

- Documentation
- Meshes

Download source code at
https://github.com/pyunity/pyunity/releases/tag/0.0.2
