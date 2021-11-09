==============
Tutorial 4: 2D
==============

.. contents:: Table of Contents
   :depth: 2
   :local:

This tutorial we will be introducing many
new components, namely the ``RectTransform``
and the ``Image2D``. There is more to
2D than this, but most of the tutorial is quite
dense in new ideas.

Data types
==========
To facilitate positioning objects, we are
going to use ``RectAnchors`` and
``RectOffset``. They both subclass
``RectData``, which means they have two
properties: ``min`` and ``max``. They are both of
type ``Vector2``. For now, let's ignore the
``RectAnchors``.

RectOffset
----------
By ignoring ``RectAnchors`` we can simplify
our offset to a literal rectangle. The ``min`` value
specifies the top left corner of the rectangle, and
the ``max`` value specifies the bottom right corner.
In PyUnity, the X axis goes left to right and the Y
axis goes top to bottom.

For example, a rect that is 100 pixels by 150 pixels,
with a top left corner of (50, 75) would be like this:

   >>> offset = RectOffset(
   ...     Vector2(50, 75),
   ...     Vector2(150, 225) # 100 + 50 and 150 + 75
   ... )

RectTransform
-------------
A ``RectTransform`` has 5 notable properties:
``parent``, ``anchors``, ``offset``, ``rotation``
and ``pivot``. ``parent`` is a read-only property,
which gets the ``RectTransform`` of its parent,
if it has one. ``rotation`` is a
float measured in degrees, and ``pivot`` is
a point between (0.0, 0.0) and (1.0, 1.0) which
defines the rotation point.

Image2D
-------
A ``RectTransform`` can't really do much on its own,
so we'll look at the ``Image2D`` component. This
renders a texture in the rect that is defined from
the ``RectTransform``. If you read tutorial 2, you
may have used the ``Texture2D`` class. Here we can
do the exact same:

   >>> gameObject = GameObject("Image")
   >>> transform = gameObject.AddComponent(RectTransform)
   >>> transform.offset = RectOffset.Rectangle(
   ...     Vector2(100, 100), center=Vector2(125, 75))
   >>> img = gameObject.AddComponent(Image2D)
   >>> img.texture = Texture2D("python.png")

Canvas
------
All 2D renderers must be a descendant of a ``Canvas``
element, which can customize the rendering of 2D
components. We don't need to worry about that too much,
except that if we were to create an ``Image2D`` we must
make it as a child or descendant of our canvas.

.. code-block:: python

   canvas = GameObject("Canvas")
   canvas.AddComponent(Canvas)
   img = GameObject("Image", canvas)
   # And so on...

Here the second argument to the ``GameObject`` constructor
specifies its parent, which must be a ``GameObject``.

Code
====

.. code-block:: python

   from pyunity import *

   scene = SceneManager.AddScene("Scene")
   canvas = GameObject("Canvas")
   canvas.AddComponent(Canvas)
   scene.Add(canvas)

   gameObject = GameObject("Image", canvas)
   transform = gameObject.AddComponent(RectTransform)
   transform.offset = RectOffset.Rectangle(
       Vector2(100, 100), center=Vector2(125, 75))
   img = gameObject.AddComponent(Image2D)
   img.texture = Texture2D("pyunity.png")
   scene.Add(gameObject)

   SceneManager.LoadScene(scene)

PyUnity image:

.. image:: ../static/pyunity.png

This is the result:

.. image:: ../static/2d.png

We can use ``Behaviour``s to interact with these 2D
objects.
