======================
Tutorial 1: The Basics
======================

In this tutorial you will be learning
the basics to using PyUnity, and
understanding some key concepts.

What is PyUnity?
================
PyUnity is a Python implementation of the
UnityEngine_, which was originally written
in C++. PyUnity has been modified to be
easy to use in Python, which means that
some features have been removed.

.. _UnityEngine: https://unity.com/

Basic concepts
==============
In PyUnity, everything belongs to a
GameObject. A GameObject is a named object that
has lots of Components on it that will
affect the GameObject and other GameObjects.
Components are Python objects that do specific
things each frame, like rendering an object or
deleting other GameObjects.

Transforms
==========

Each GameObject has a special component called
a Transform. A Transform holds information about
the GameObject's position, rotation and scale.

A Transform also manages the hierarchy system in PyUnity.
Each transforms can have multiple children, which are all
Transforms attached to the children GameObjects.
All transforms will have a ``localPosition``, ``localRotation``
and ``localScale``, which are all relative to their parent.
In addition, all Transforms will have a ``position``,
``rotation`` and ``scale`` property which is measured
in global space.

For example, if there is a Transform at 1 unit up from
the origin, and its child had a ``localPosition`` of
1 unit right, then the child would have a ``position`` of
1 unit up and 1 unit to the right.

Code
====
All of that has now been established, so let's start to
program it all! To start, we need to import PyUnity.

   >>> from pyunity import *
   Loaded config
   Trying GLFW as a window provider
   GLFW doesn't work, trying PySDL2
   Trying PySDL2 as a window provider
   Using window provider PySDL2
   Loaded PyUnity version 0.4.0

The output beneath the import is just for debug, you
can turn it off with the environment variable
``PYUNITY_DEBUG_INFO`` set to ``"0"``.

For example:

   >>> import os
   >>> os.environ["PYUNITY_DEBUG_INFO"] = "0"
   >>> from pyunity import *
   >>> # No output

Now we have loaded the module, we can start creating our
GameObjects. To create a GameObject, use the ``GameObject``
class:

   >>> root = GameObject("Root")

Then we can change its position by accessing its transform.
All GameObjects have references to their transform by the
``transform`` attribute, and all components have a reference
to the GameObject and the Transform that they belong to, by
the ``gameObject`` and ``transform`` attributes. Here's
how to make the GameObject positioned 1 unit up, 2 units to
the right and 3 units forward:

   >>> root.transform.localPosition = Vector3(2, 1, 3)

A Vector3 is just a way to represent a 3D vector. In PyUnity
the coordinate system is a left-hand Y-axis up system, which
is essentially what OpenGL uses, but with the Z-axis flipped.

Then to add a child to the GameObject, specify the parent
GameObject as the second argument:

   >>> child1 = GameObject("Child1", root)
   >>> child2 = GameObject("Child2", root)


**Note**: Accessing the ``localPosition``, ``localRotation`` and
``localScale`` attributes are faster than using the ``position``,
``rotation`` and ``scale`` properties. Use the local attributes
whenever you can.

Rotation
========
Rotation is measured in Quaternions. Do not worry about these,
because they use some very complex maths. All you need to know
are these methods:

#. To make a Quaternion that represents no rotation, use
   ``Quaternion.identity()``. This just means no rotation.
#. To make a Quaternion from an axis and angle, use the
   ``Quaternion.FromAxis()`` method. What this does is it
   creates a Quaternion that represents a rotation around
   an axis clockwise, by ``angle`` degrees. The axis
   does not need to be normalized.
#. To make a Quaternion from Euler angles, use
   ``Quaternion.Euler``. This creates a Quaternion from
   Euler angles, where it is rotated on the Z-axis first,
   then the X-axis, and finally the Y-axis.

Transforms also have ``localEulerAngles`` and ``eulerAngles``
properties, which just represent the Euler angles of the
rotation Quaternions. If you don't know what to do, only use
the ``eulerAngles`` property.

In the next tutorial, we'll be covering how to render things
and use a Scene.