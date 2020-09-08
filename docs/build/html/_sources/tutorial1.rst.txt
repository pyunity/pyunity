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
GameObject. A GameObject is an object that
has lots of different things on it that will
affect the GameObject and other GameObjects.
Each GameObject has its own Components, which
are like the hardware in a computer. These
Components can do all sorts of things.

Each GameObject has a special component called
a Transform. A Transform holds information about
the GameObject's position, rotation and scale.
A Transform can also have other Transforms as
children, and the children Transforms will have
their position, rotation and scale affected by
the parent.