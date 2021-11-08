==============
Tutorial 4: 2D
==============

.. contents:: Table of Contents
   :depth: 1
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
and ``pivot``.