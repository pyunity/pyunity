===============================
Tutorial 2: Rendering in Scenes
===============================

Last tutorial we covered some basic concepts
on GameObjects and Transforms, and this time
we'll be looking at how to render things in
a window.

Scenes
======
A Scene is like a page to draw on: you can
add things, remove things and change things.
To create a scene, you can call
``SceneManager.AddScene``:

   >>> scene = SceneManager.AddScene("Scene")

In your newly created scene, you have 2 GameObjects:
a Main Camera, and a Light. These two things can be
moved around like normal GameObjects.

Next, let's move the camera back 10 units:

   >>> scene.mainCamera.transform.localPosition = Vector3(0, 0, -10)

``scene.mainCamera`` references the Camera component
on the Main Camera.