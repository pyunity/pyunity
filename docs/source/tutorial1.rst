======================
Tutorial 1: The Basics
======================

In this tutorial you will be learning
the basics to using PyUnity, and
understanding some key concepts.

What is PyUnity?
================
PyUnity is a Python port of the
UnityEngine_, which was originally written
in C++. PyUnity has been modified to be
easy to use in Python, which means that
some features have been removed.

.. _UnityEngine: https://unity.com/

Basic concepts
==============
In PyUnity, everything will belong to a
GameObject. A GameObject is a named object that
has lots of different things on it that will
affect the GameObject and other GameObjects.
Each GameObject has its own Components, which
are like the hardware in a computer. These
Components can do all sorts of things.

Transforms
==========

Each GameObject has a special component called
a Transform. A Transform holds information about
the GameObject's position, rotation and scale.

A Transform can also have a child. This child is
also a GameObject's component. All transforms will
have a localPosition, localRotation and localScale,
which are all relative to their parent. In addition,
all Transforms will have a ``position``, ``rotation`` and
``scale`` property which is measured in global space.

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
   GLFW doesn't work, trying Pygame
   Trying Pygame as a window provider
   Using window provider Pygame
   Loaded PyUnity version 0.0.6

The output beneath the import is just debug statement, you
can turn it off with the environment variable
``PYUNITY_DEBUG_INFO`` set to ``0``.