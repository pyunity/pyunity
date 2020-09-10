==================================
Tutorial 3: Scripts and Behaviours
==================================

Last tutorial we covered rendering meshes. In
this tutorial we will be seeing how to make 2
GameObjects interact with each other.

Behaviours
==========
A Behaviour is a Component that you can create
yourself. To create a Behaviour, subclass from
it:

   >>> class MyBehaviour(Behaviour):
   ...     pass

In this case the Behaviour does nothing. To make
it do something, use the Update function:

   >>> class Rotator(Behaviour):
   ...     def Update(self, dt):
   ...         self.transform.localEulerAngles += Vector3(0, 90, 0) * dt

What this does is it rotates the GameObject that
the Behaviour is on by 90 degrees each second
around the y-axis. The ``Update`` function takes
1 argument: ``dt`` which is how many seconds has
passed since last frame.

Behaviours vs Components
========================
Look at the code for the Component class:

.. code-block:: python

   class Component:
       def __init__(self):
           self.gameObject = None
           self.transform = None
    
       def GetComponent(self, component):
           return self.gameObject.GetComponent(component)
    
       def AddComponent(self, component):
           return self.gameObject.AddComponent(component)

A Component has 2 attributes: ``gameObject`` and ``transform``.
This is set whenever the Component is added to a GameObject.
A Behaviour is subclassed from a Component and so has the
same attributes. Each frame, the Scene will call the ``Update``
function on all Behaviours, passing the time since the last
frame in seconds.

When you want to do something at the start of the Scene, use
the ``Start`` function. That will be called right at the start
of the scene, when ``scene.Run()`` is called.

   >>> class MyBehaviour(Behaviour):
   ...     def Start(self):
   ...         self.a = 0
   ...     def Update(self, dt):
   ...         print(self.a)
   ...         self.a += dt

The example above will print in seconds how long
it had been since the start of the Scene. Note
that the order in which all Behaviours'
``Start`` functions will be the orders of the
GameObjects.

With this, you can create all sorts of Components,
and because Behaviour is subclassed from
Component, you can add a Behaviour to a GameObject
with ``AddComponent``.

Examples
========

This creates a spinning cube:

   >>> class Rotator(Behaviour):
   ...     def Update(self, dt):
   ...         self.transform.localEulerAngles += Vector3(0, 90, 135) * dt
   ...
   >>> scene = SceneManager.AddScene("Scene")
   >>> cube = GameObject("Cube")
   >>> renderer = cube.AddComponent(MeshRenderer)
   >>> renderer.mesh = Mesh.cube(2)
   >>> renderer.mat = Material((255, 0, 0))
   >>> cube.AddComponent(Rotator)
   >>> scene.Add(cube)
   >>> scene.Run()

This is a debugging Behaviour, which prints out the
change in position, rotation and scale each 10
frames:

   >>> class Debugger(Behaviour):
   ...     lastPos = Vector3.zero()
   ...     lastRot = Quaternion.identity()
   ...     lastScl = Vector3.one()
   ...     a = 0
   ...     def Update(self, dt):
   ...         self.a += 1
   ...         if self.a == 10:
   ...             print(self.transform.position - self.lastPos)
   ...             print(self.transform.rotation.conjugate * self.lastRot)
   ...             print(self.transform.scale / self.lastScl)
   ...             self.a = 0
   ...

Note that the printed output for non-moving things
would be as so:

   Vector3(0, 0, 0)
   Quaternion(1, 0, 0, 0)
   Vector3(1, 1, 1)
   Vector3(0, 0, 0)
   Quaternion(1, 0, 0, 0)
   Vector3(1, 1, 1)
   Vector3(0, 0, 0)
   Quaternion(1, 0, 0, 0)
   Vector3(1, 1, 1)
   ...

This means no rotation, position or scale change.
It will break when you set the scale to
``Vector3(0, 0, 0)``.

In the next tutorial we'll be looking at physics.