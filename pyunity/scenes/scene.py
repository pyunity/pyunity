"""
Class to load, render and manage GameObjects
and their various components.

You should never use the ``Scene``
class directly, instead, only use
the SceneManager class.

"""

from ..audio import *
from ..core import *
from ..files import Behaviour
from ..vector3 import Vector3
from ..quaternion import Quaternion
from .. import config, physics, logger as Logger, render
from ..errors import *
from time import time
import os
import math

if os.environ["PYUNITY_INTERACTIVE"] == "1":
    import OpenGL.GL as gl

class Scene:
    """
    Class to hold all of the GameObjects, and to run the whole
    scene.

    Parameters
    ----------
    name : str
        Name of the scene

    Notes
    -----
    Create a scene using the SceneManager, and don't create a scene
    directly using this class.

    """

    def __init__(self, name):
        self.name = name
        self.mainCamera = GameObject("Main Camera").AddComponent(render.Camera)
        self.mainCamera.AddComponent(AudioListener)
        light = GameObject("Light")
        light.AddComponent(Light)
        light.transform.localPosition = Vector3(10, 10, -10)
        self.gameObjects = [self.mainCamera.gameObject, light]
        self.rootGameObjects = [self.mainCamera.gameObject, light]

    @staticmethod
    def Bare(name):
        cls = Scene.__new__(Scene)
        cls.name = name
        cls.gameObjects = []
        cls.rootGameObjects = []
        cls.mainCamera = None
        return cls

    def Add(self, gameObject):
        """
        Add a GameObject to the scene.

        Parameters
        ----------
        gameObject : GameObject
            The GameObject to add.

        """
        self.gameObjects.append(gameObject)
        if gameObject.transform.parent is None:
            self.rootGameObjects.append(gameObject)

    def Remove(self, gameObject):
        """
        Remove a GameObject from the scene.

        Parameters
        ----------
        gameObject : GameObject
            GameObject to remove.

        Raises
        ------
        PyUnityException
            If the specified GameObject is not part
            of the Scene.

        """
        if gameObject in self.gameObjects:
            self.gameObjects.remove(gameObject)
        else:
            raise PyUnityException(
                "The provided GameObject is not part of the Scene")
        if gameObject is self.mainCamera:
            Logger.LogLine(
                Logger.WARN, "Removing Main Camera from scene \"" + self.name + "\"")

    def List(self):
        """Lists all the GameObjects currently in the scene."""
        for gameObject in sorted(self.rootGameObjects, key=lambda x: x.name):
            gameObject.transform.List()

    def FindGameObjectsByName(self, name):
        """
        Finds all GameObjects matching the specified name.

        Parameters
        ----------
        name : str
            Name of the GameObject

        Returns
        -------
        list
            List of the matching GameObjects

        """
        return [gameObject for gameObject in self.gameObjects if gameObject.name == name]

    def FindGameObjectsByTagName(self, name):
        """
        Finds all GameObjects with the specified tag name.

        Parameters
        ----------
        name : str
            Name of the tag

        Returns
        -------
        list
            List of matching GameObjects

        Raises
        ------
        GameObjectException
            When there is no tag named `name`

        """
        if name in Tag.tags:
            return [gameObject for gameObject in self.gameObjects if gameObject.tag.tagName == name]
        else:
            raise GameObjectException(
                "No tag named " + name + "; create a new tag with Tag.AddTag")

    def FindGameObjectsByTagNumber(self, num):
        """
        Gets all GameObjects with a tag of tag `num`.

        Parameters
        ----------
        num : int
            Index of the tag

        Returns
        -------
        list
            List of matching GameObjects

        Raises
        ------
        GameObjectException
            If there is no tag with specified index.

        """
        if len(Tag.tags) > num:
            return [gameObject for gameObject in self.gameObjects if gameObject.tag.tag == num]
        else:
            raise GameObjectException(
                "No tag at index " + str(num) + "; create a new tag with Tag.AddTag")

    def FindComponentByType(self, component):
        """
        Finds the first matching Component that is in the Scene.

        Parameters
        ----------
        component : type
            Component type

        Returns
        -------
        Component
            The matching Component

        Raises
        ------
        ComponentException
            If the component is not found

        """
        for gameObject in self.gameObjects:
            query = gameObject.GetComponent(component)
            if query is not None:
                break
        if query is None:
            raise ComponentException(
                "Cannot find component " + component.__name__ + " in scene")
        return query

    def FindComponentsByType(self, component):
        """
        Finds all matching Components that are in the Scene.

        Parameters
        ----------
        component : type
            Component type

        Returns
        -------
        list
            List of the matching Components

        """
        components = []
        for gameObject in self.gameObjects:
            query = gameObject.GetComponents(component)
            components.extend(query)
        return components

    def inside_frustrum(self, renderer):
        """
        Check if the renderer's mesh can be
        seen by the main camera.

        Parameters
        ----------
        renderer : MeshRenderer
            Renderer to test

        Returns
        -------
        bool
            If the mesh can be seen

        """
        mesh = renderer.mesh
        pos = self.mainCamera.transform.position * Vector3(1, 1, -1)
        directionX = self.mainCamera.transform.rotation.RotateVector(
            Vector3.right()) * Vector3(1, 1, -1)
        directionY = self.mainCamera.transform.rotation.RotateVector(
            Vector3.up()) * Vector3(1, 1, -1)
        directionZ = self.mainCamera.transform.rotation.RotateVector(
            Vector3.forward()) * Vector3(1, 1, -1)
        parent = renderer.transform.parent.position if renderer.transform.parent else Vector3.zero()
        rpmin = renderer.transform.rotation.RotateVector(
            mesh.min - renderer.transform.localPosition)
        rpmax = renderer.transform.rotation.RotateVector(
            mesh.max - renderer.transform.localPosition)
        rpmin += parent - pos
        rpmax += parent - pos

        minZ = rpmin.dot(directionZ)
        maxZ = rpmax.dot(directionZ)
        if minZ > self.mainCamera.near or maxZ < self.mainCamera.far:
            return True

        minY = rpmin.dot(directionY)
        maxY = rpmax.dot(directionY)
        hmin = minZ * 2 * \
            math.tan(math.radians(self.mainCamera.fov /
                                  config.size[0] * config.size[1] / 2))
        hmax = maxZ * 2 * \
            math.tan(math.radians(self.mainCamera.fov /
                                  config.size[0] * config.size[1] / 2))
        if minY > -hmin / 2 or maxY < hmax / 2:
            return True

        minX = rpmin.dot(directionX)
        maxX = rpmax.dot(directionX)
        wmin, wmax = hmin * \
            config.size[0] / config.size[1], hmax * \
            config.size[0] / config.size[1]
        return minX > -wmin / 2 or maxX < wmax / 2

    def start_scripts(self):
        """Start the scripts in the Scene."""
        self.lastFrame = time()

        audioListeners = self.FindComponentsByType(AudioListener)
        if len(audioListeners) == 0:
            Logger.LogLine(
                Logger.WARN, "No AudioListeners found, audio is disabled")
            self.audioListener = None
        elif len(audioListeners) > 1:
            Logger.LogLine(Logger.WARN, "Ambiguity in AudioListeners, " +
                           str(len(audioListeners)) + " found")
            self.audioListener = None
        else:
            self.audioListener = audioListeners[0]
            self.audioListener.Init()

        for gameObject in self.gameObjects:
            for component in gameObject.components:
                if isinstance(component, Behaviour):
                    component.Start()
                elif isinstance(component, AudioSource):
                    if component.PlayOnStart:
                        component.Play()
                elif isinstance(component, MeshRenderer) and component.mesh is not None:
                    mesh = component.mesh
                    mesh.vbo, mesh.ibo = render.gen_buffers(mesh)
                    mesh.vao = render.gen_array()

        self.physics = any(
            isinstance(
                component, physics.Collider
            ) for gameObject in self.gameObjects for component in gameObject.components
        )
        if self.physics:
            self.collManager = physics.CollManager()
            self.collManager.AddPhysicsInfo(self)

    def Start(self):
        """
        Start the internal parts of the
        Scene.

        """

        self.mainCamera.lastPos = Vector3.zero()
        self.mainCamera.lastRot = Quaternion.identity()

        if os.environ["PYUNITY_INTERACTIVE"] == "1":
            self.mainCamera.Resize(*config.size)

            gl.glEnable(gl.GL_DEPTH_TEST)
            if config.faceCulling:
                gl.glEnable(gl.GL_CULL_FACE)

        self.start_scripts()

        Logger.LogLine(Logger.DEBUG, "Physics is",
                       "on" if self.physics else "off")
        Logger.LogLine(Logger.DEBUG, "Scene \"" + self.name + "\" has started")

    def update_scripts(self):
        """Updates all scripts in the scene."""
        dt = max(time() - self.lastFrame, 0.001)
        for gameObject in self.gameObjects:
            for component in gameObject.components:
                if isinstance(component, Behaviour):
                    component.Update(dt)
                elif isinstance(component, AudioSource):
                    if component.Loop:
                        if component.PlayOnStart:
                            if component.channel and not component.channel.get_busy():
                                component.Play()

        if self.physics:
            self.collManager.Step(dt)

        self.lastFrame = time()

    def no_interactive(self):
        done = False
        clock = Clock()
        clock.fps = config.fps
        while not done:
            try:
                self.update_scripts()
                clock.Maintain()
            except KeyboardInterrupt:
                Logger.LogLine(Logger.DEBUG, "Exiting")
                done = True

    def update(self):
        """Updating function to pass to the window provider."""
        self.update_scripts()

        if os.environ["PYUNITY_INTERACTIVE"] == "1":
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

            if (self.mainCamera.lastPos != self.mainCamera.transform.position or
                    self.mainCamera.lastRot != self.mainCamera.transform.rotation):
                self.mainCamera.lastPos = self.mainCamera.transform.position
                self.mainCamera.lastRot = self.mainCamera.transform.rotation

            self.mainCamera.Render(self.gameObjects)

    def clean_up(self):
        if self.audioListener is not None:
            self.audioListener.DeInit()
