======================
Scripts and Behaviours
======================

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

With a Behaviour, never define the ``__init__``
function, but you can use the ``Start`` function.
That will be called on the start of the scene:

   >>> class MyBehaviour(Behaviour):
   ...     def Start(self):
   ...         self.a = 0
   ...     def Update(self, dt):
   ...         print(self.a)
   ...         self.a += dt