## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""
Class to load, render and manage GameObjects
and their various components.

You should never use the :class:`Scene`
class directly, instead, only use
the :class:`SceneManager` submodule.

"""

__all__ = ["Scene"]

from .. import Logger, config
from ..audio import AudioListener, AudioSource
from ..core import Component, GameObject, Tag
from ..errors import ComponentException, GameObjectException, PyUnityException
from ..events import EventLoop
from ..files import Asset, Behaviour
from ..meshes import MeshRenderer
from ..physics.core import CollManager
from ..render import Camera, Light, Screen
from ..values import Mathf, Vector3
from pathlib import Path
import os
import sys
import time
import inspect

if os.environ["PYUNITY_INTERACTIVE"] == "1":
    import OpenGL.GL as gl

disallowedChars = set(":*/\"\\?<>|")

def createTask(loop, coro, *args):
    if inspect.iscoroutinefunction(coro):
        loop.create_task(coro(*args))
    else:
        coro(*args)

class Scene(Asset):
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
        self.mainCamera = GameObject("Main Camera").AddComponent(Camera)
        self.mainCamera.AddComponent(AudioListener)
        self.mainCamera.gameObject.scene = self
        light = GameObject("Light")
        light.transform.localPosition = Vector3(10, 10, -10)
        light.transform.LookAtPoint(Vector3.zero())
        light.AddComponent(Light)
        light.scene = self
        self.gameObjects = [self.mainCamera.gameObject, light]

    def GetAssetFile(self, gameObject):
        return Path("Scenes") / (self.name + ".scene")

    def SaveAsset(self, ctx):
        ctx.savers[Scene](self, ctx.project, ctx.filename)

    @staticmethod
    def Bare(name):
        """
        Create a bare scene.

        Parameters
        ----------
        name : str
            Name of the scene

        Returns
        -------
        Scene
            A bare scene with no GameObjects

        """
        cls = Scene.__new__(Scene)
        cls.name = name
        cls.gameObjects = []
        cls.mainCamera = None
        return cls

    @property
    def rootGameObjects(self):
        """All GameObjects which have no parent"""
        return [x for x in self.gameObjects if x.transform.parent is None]

    def Add(self, gameObject):
        """
        Add a GameObject to the scene.

        Parameters
        ----------
        gameObject : GameObject
            The GameObject to add.

        """
        if gameObject.scene is not None:
            raise PyUnityException("GameObject \"%s\" is already in Scene \"%s\"" %
                                   (gameObject.name, gameObject.scene.name))
        gameObject.scene = self
        self.gameObjects.append(gameObject)

    def AddMultiple(self, *args):
        """
        Add GameObjects to the scene.

        Parameters
        ----------
        *args : list
            A list of GameObjects to add.

        """
        for gameObject in args:
            self.Add(gameObject)

    def Destroy(self, gameObject):
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
        if gameObject not in self.gameObjects:
            raise PyUnityException(
                "The provided GameObject is not part of the Scene")

        pending = [a.gameObject for a in gameObject.transform.GetDescendants()]
        for gameObject in pending:
            for component in gameObject.GetComponents(Behaviour):
                component.OnDestroy()

        for gameObject in pending:
            if gameObject in self.gameObjects:
                gameObject.scene = None
                self.gameObjects.remove(gameObject)
                if self.mainCamera is not None and gameObject is self.mainCamera.gameObject:
                    Logger.LogLine(Logger.WARN,
                                   f"Removing Main Camera from scene {self.name!r}")
                    self.mainCamera = None

        for gameObject in self.gameObjects:
            for component in gameObject.components:
                for saved in component._saved:
                    attr = getattr(component, saved)
                    if isinstance(attr, GameObject):
                        if attr in pending:
                            setattr(component, saved, None)
                    elif isinstance(attr, Component):
                        if attr.gameObject in pending:
                            setattr(component, saved, None)

    def Has(self, gameObject):
        """
        Check if a GameObject is in the scene.

        Parameters
        ----------
        gameObject : GameObject
            Query GameObject

        Returns
        -------
        bool
            If the GameObject exists in the scene

        """
        return gameObject in self.gameObjects

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
            When there is no tag named ``name``

        """
        if name in Tag.tags:
            return [gameObject for gameObject in self.gameObjects if gameObject.tag.tagName == name]
        else:
            raise GameObjectException(
                f"No tag named {name}; create a new tag with Tag.AddTag")

    def FindGameObjectsByTagNumber(self, num):
        """
        Gets all GameObjects with a tag of tag ``num``.

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
        if len(Tag.tags) > num >= 0:
            return [gameObject for gameObject in self.gameObjects if gameObject.tag.tag == num]
        else:
            raise GameObjectException(
                f"No tag at index {num}; create a new tag with Tag.AddTag")

    def FindComponent(self, component):
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
                f"Cannot find component {component.__name__} in scene")
        return query

    def FindComponents(self, component):
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

    def insideFrustum(self, renderer):
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
        if mesh is None:
            return False
        pos = self.mainCamera.transform.position * Vector3(1, 1, -1)
        directionX = self.mainCamera.transform.right * Vector3(1, 1, -1)
        directionY = self.mainCamera.transform.up * Vector3(1, 1, -1)
        directionZ = self.mainCamera.transform.forward * Vector3(1, 1, -1)
        if renderer.transform.parent is not None:
            parent = renderer.transform.parent.position
        else:
            parent = Vector3.zero()
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
            Mathf.Tan(self.mainCamera.fov / Screen.size.x *
                      Screen.size.y / 2 * Mathf.DEG_TO_RAD)
        hmax = maxZ * 2 * \
            Mathf.Tan(self.mainCamera.fov / Screen.size.x *
                      Screen.size.y / 2 * Mathf.DEG_TO_RAD)
        if minY > -hmin / 2 or maxY < hmax / 2:
            return True

        minX = rpmin.dot(directionX)
        maxX = rpmax.dot(directionX)
        wmin, wmax = hmin * \
            Screen.size.x / Screen.size.y, hmax * \
            Screen.size.x / Screen.size.y
        return minX > -wmin / 2 or maxX < wmax / 2

    def startOpenGL(self):
        self.mainCamera.Resize(*config.size)

        gl.glEnable(gl.GL_DEPTH_TEST)
        if config.faceCulling:
            gl.glEnable(gl.GL_CULL_FACE)
        else:
            gl.glDisable(gl.GL_CULL_FACE)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA,
                       gl.GL_ONE_MINUS_SRC_ALPHA)

        for gameObject in self.gameObjects:
            for component in gameObject.components:
                if isinstance(component, MeshRenderer) and component.mesh is not None:
                    component.mesh.compile()

        self.mainCamera.setupBuffers()

    def startScripts(self):
        loop = EventLoop()
        if config.audio:
            audioListeners = self.FindComponents(AudioListener)
            audioListeners = [c for c in audioListeners if c.enabled]
            if len(audioListeners) == 0:
                Logger.LogLine(
                    Logger.WARN, "No enabled AudioListeners found, audio is disabled")
                self.audioListener = None
            elif len(audioListeners) > 1:
                Logger.LogLine(Logger.WARN, "Ambiguity in AudioListeners, " +
                               str(len(audioListeners)) + " enabled")
                self.audioListener = None
            else:
                self.audioListener = audioListeners[0]
                self.audioListener.Init()
        else:
            self.audioListener = None

        for gameObject in self.gameObjects:
            if not gameObject.enabled:
                continue
            for component in gameObject.components:
                if not component.enabled:
                    continue
                if isinstance(component, Behaviour):
                    component.Awake()
                    createTask(loop, component.Start)
                elif isinstance(component, AudioSource):
                    if component.playOnStart:
                        component.Play()

        # self.physics = any(
        #     isinstance(
        #         component, Rigidbody
        #     ) for gameObject in self.gameObjects for component in gameObject.components
        # )
        self.physics = True # Check is too expensive
        if self.physics:
            self.collManager = CollManager()
            self.collManager.AddPhysicsInfo(self)

        return loop

    def startLoop(self):
        Logger.LogLine(Logger.DEBUG, "Physics is",
                       "on" if self.physics else "off")
        Logger.LogLine(Logger.DEBUG, "Scene " +
                       repr(self.name) + " has started")

        self.lastFrame = time.perf_counter()
        self.lastFixedFrame = time.perf_counter()

    def Start(self):
        """
        Start the internal parts of the
        Scene. Deprecated in 0.9.0.

        """
        self.startScripts()
        self.startOpenGL()

    def updateScripts(self, loop):
        """Updates all scripts in the scene."""
        from ..input import Input
        dt = max(time.perf_counter() - self.lastFrame, sys.float_info.epsilon)
        self.lastFrame = time.perf_counter()
        if os.environ["PYUNITY_INTERACTIVE"] == "1":
            Input.UpdateAxes(dt)
            if self.mainCamera is not None and self.mainCamera.canvas is not None:
                if self.mainCamera.enabled and self.mainCamera.canvas.enabled:
                    self.mainCamera.canvas.Update(loop)

        for gameObject in self.gameObjects:
            if not gameObject.enabled:
                continue
            for component in gameObject.components:
                if not component.enabled:
                    continue
                if isinstance(component, Behaviour):
                    createTask(loop, component.Update, dt)
                elif isinstance(component, AudioSource):
                    if component.loop and component.playOnStart:
                        if component.channel and not component.channel.get_busy():
                            component.Play()

        for gameObject in self.gameObjects:
            if not gameObject.enabled:
                continue
            for component in gameObject.GetComponents(Behaviour):
                if component.enabled:
                    createTask(loop, component.LateUpdate, dt)

    def updateFixed(self, loop):
        dt = max(time.perf_counter() - self.lastFixedFrame, sys.float_info.epsilon)
        self.lastFixedFrame = time.perf_counter()
        if self.physics:
            self.collManager.Step(dt)
            for gameObject in self.gameObjects:
                if not gameObject.enabled:
                    continue
                for component in gameObject.GetComponents(Behaviour):
                    if component.enabled:
                        createTask(loop, component.FixedUpdate, dt)

    def Render(self, loop=None):
        """
        Call the appropriate rendering functions
        of the Main Camera.

        Parameters
        ----------
        loop : EventLoop
            Event loop to run :meth:`Behaviour.OnPreRender`
            and :meth:`Behaviour.OnPostRender` in. If None,
            the above methods will not be called.

        """
        if self.mainCamera is None or not self.mainCamera.enabled:
            gl.glClearColor(0, 0, 0, 1)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)
            return

        if loop is not None:
            behaviours = self.FindComponents(Behaviour)
            for component in behaviours:
                createTask(loop, component.OnPreRender)

        renderers = self.FindComponents(MeshRenderer)
        lights = self.FindComponents(Light)
        self.mainCamera.renderPass = True
        self.mainCamera.Render(renderers, lights)
        self.mainCamera.renderPass = False

        if loop is not None:
            for component in behaviours:
                createTask(loop, component.OnPostRender)

    def cleanUp(self):
        """
        Called when the scene finishes running,
        or stops running.

        """
        if self.audioListener is not None:
            self.audioListener.DeInit()

        for gameObject in self.gameObjects:
            for component in gameObject.GetComponents(Behaviour):
                component.OnDestroy()
