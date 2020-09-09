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

With a Behaviour, never define the ``__init__``
function, but you can use the ``Start`` function.
That will be called on the start of the scene:

   >>> class MyBehaviour(Behaviour):
   ...     def Start(self):
   ...         self.a = 0
   ...     def Update(self, dt):
   ...         print(self.a)
   ...         self.a += dt

The example above will print in seconds how long
it had been since the start of the Scene.

With this, you can create all sorts of Components,
and because Behaviour is subclassed from
Component, you can add a Behaviour to a GameObject
with ``AddComponent``. This creates a spinning
cube:

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

In the next tutorial we'll be looking at physics.