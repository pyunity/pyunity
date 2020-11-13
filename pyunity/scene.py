"""
Module to create and load Scenes.

You should never use the ``Scene``
class directly, instead, only use
the SceneManager class.

"""

from .audio import *
from .core import *
from .vector3 import Vector3
from .quaternion import Quaternion
from . import config, window, physics
from .errors import *
from time import time
import os
import math
import copy
import pygame

if os.environ["PYUNITY_INTERACTIVE"] == "1":
    import OpenGL.GL as gl
    import OpenGL.GLU as glu

class SceneManager:
    """
    Class to manage scenes.

    Attributes
    ----------
    scenesByIndex : list
        List of scenes
    scenesByName : dict
        Dictionary of scenes, with the scene
        names as the keys.

    """

    def __init__(self):
        self.scenesByIndex = []
        self.scenesByName = {}
        self.window = None

    def AddScene(self, sceneName):
        """
        Add a scene to the SceneManager. Pass
        in a scene name to create a scene.

        Parameters
        ----------
        sceneName : str
            Name of the scene

        Returns
        -------
        Scene
            Newly created scene

        Raises
        ------
        PyUnityException
            If there already exists a scene called `sceneName`

        """
        if sceneName in self.scenesByName:
            raise PyUnityException("SceneManager already contains scene \"" +
                                   sceneName + "\"")
        scene = Scene(sceneName)
        self.scenesByIndex.append(scene)
        self.scenesByName[sceneName] = scene
        return scene

    def GetSceneByIndex(self, index):
        """
        Get a scene by its index.

        Parameters
        ----------
        index : int
            Index of the scene

        Returns
        -------
        Scene
            Specified scene at index `index`

        Raises
        ------
        IndexError
            If there is no scene at the specified index

        """
        if len(self.scenesByIndex) <= index:
            raise IndexError("There is no scene at index " + str(index))
        return self.scenesByIndex[index]

    def GetSceneByName(self, name):
        """
        Get a scene by its name.

        Parameters
        ----------
        name : str
            Name of the scene

        Returns
        -------
        Scene
            Specified scene with name of `name`

        Raises
        ------
        KeyError
            If there is no scene called `name`

        """
        if name not in self.scenesByName:
            raise KeyError("There is no scene called " + name)
        return self.scenesByName[name]

    def RemoveScene(self, scene):
        """
        Removes a scene from the SceneManager.

        Parameters
        ----------
        scene : Scene
            Scene to remove

        Raises
        ------
        TypeError
            If the provided scene is not type Scene
        PyUnityException
            If the scene is not part of the SceneManager

        """
        if not isinstance(scene, Scene):
            raise TypeError("The provided scene is not of type Scene")
        if scene not in self.scenesByIndex:
            raise PyUnityException(
                "Scene \"%s\" is not part of the SceneManager" % scene.name)
        self.scenesByIndex.remove(scene)
        self.scenesByName.pop(scene.name)

    def LoadSceneByName(self, name):
        """
        Loads a scene by its name.

        Parameters
        ----------
        name : str
            Name of the scene

        Raises
        ------
        TypeError
            When the provided name is not a string
        PyUnityException
            When there is no scene named ``name``

        """
        if not isinstance(name, str):
            raise TypeError("\"%r\" is not a string" % name)
        if name not in self.scenesByName:
            raise PyUnityException("There is no scene named \"%s\"" % name)
        self.__loadScene(copy.deepcopy(self.scenesByName[name]))

    def LoadSceneByIndex(self, index):
        """
        Loads a scene by its index of when it was added
        to the SceneManager.

        Parameters
        ----------
        index : int
            Index of the scene

        Raises
        ------
        TypeError
            When the provided index is not an integer
        PyUnityException
            When there is no scene at index ``index``

        """
        if not isinstance(index, int):
            raise TypeError("\"%r\" is not an integer" % index)
        if index >= len(self.scenesByIndex):
            raise PyUnityException("There is no scene at index \"%d\"" % index)
        self.__loadScene(copy.deepcopy(self.scenesByIndex[index]))

    def LoadScene(self, scene):
        """
        Load a scene by a reference.

        Parameters
        ----------
        scene : Scene
            Scene to be loaded

        Raises
        ------
        TypeError
            When the scene is not of type `Scene`
        PyUnityException
            When the scene is not part of the SceneManager.
            This is checked because the SceneManager
            has to make some checks before the scene
            can be run.

        """
        if not isinstance(scene, Scene):
            raise TypeError(
                "The provided Scene \"%s\" is not an integer" % scene.name)
        if scene not in self.scenesByIndex:
            raise PyUnityException(
                "The provided scene is not part of the SceneManager")
        self.__loadScene(copy.deepcopy(scene))

    def __loadScene(self, scene):
        self.__running_scene = scene
        if not self.window and os.environ["PYUNITY_INTERACTIVE"] == "1":
            self.window = window.window_providers[config.windowProvider](
                config, scene.name)
            scene.Start()
            self.window.start(scene.update)
            self.window = None
        else:
            scene.Start()
            if os.environ["PYUNITY_INTERACTIVE"] == "1":
                self.window.update_func = scene.update
            else:
                scene.no_interactive()

    @property
    def CurrentScene(self):
        """Gets the current scene being run"""
        return self.__running_scene


SceneManager = SceneManager()
"""Manages all scene additions and changes"""

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
        self.mainCamera = GameObject("Main Camera").AddComponent(Camera)
        light = GameObject("Light")
        light.AddComponent(Light)
        light.transform.localPosition = Vector3(10, 10, -10)
        self.gameObjects = [self.mainCamera.gameObject, light]
        self.rootGameObjects = [self.mainCamera.gameObject, light]

    def Add(self, gameObject):
        """
        Add a GameObject to the scene.

        Parameters
        ----------
        gameObject : GameObejct
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
            If the specified GameObject is the Main Camera.

        """
        if gameObject not in [self.mainCamera]:
            flag = False
            for go in self.gameObjects:
                if go == gameObject:
                    flag = True
                    break
            if flag:
                self.gameObjects.remove(gameObject)
        else:
            raise PyUnityException(
                "Cannot remove the Main Camera from the scene")

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
        if name in tags:
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
        if len(tags) > num:
            return [gameObject for gameObject in self.gameObjects if gameObject.tag.tag == num]
        else:
            raise GameObjectException(
                "No tag at index " + str(num) + "; create a new tag with Tag.AddTag")

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

        for gameObject in self.gameObjects:
            for component in gameObject.components:
                if isinstance(component, Behaviour):
                    component.Start()
                elif isinstance(component, AudioSource):
                    component.channel = pygame.mixer.Channel(0)
                    if component.clip:
                        component.clip.sound = pygame.mixer.Sound(
                            component.clip.file)
                    if component.PlayOnStart:
                        component.Play()

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
        if os.environ["PYUNITY_INTERACTIVE"] == "1":
            self.lights = [
                gl.GL_LIGHT0,
                gl.GL_LIGHT1,
                gl.GL_LIGHT2,
                gl.GL_LIGHT3,
                gl.GL_LIGHT4,
                gl.GL_LIGHT5,
                gl.GL_LIGHT6,
                gl.GL_LIGHT7
            ]

        self.mainCamera.lastPos = Vector3.zero()
        self.mainCamera.lastRot = Quaternion.identity()

        if os.environ["PYUNITY_INTERACTIVE"] == "1":
            gl.glMatrixMode(gl.GL_PROJECTION)
            gl.glLoadIdentity()
            glu.gluPerspective(
                self.mainCamera.fov / config.size[0] * config.size[1],
                config.size[0] / config.size[1],
                self.mainCamera.near,
                self.mainCamera.far)
            gl.glMatrixMode(gl.GL_MODELVIEW)

            light_num = 0
            for gameObject in self.gameObjects:
                light = gameObject.GetComponent(Light)
                if light:
                    color = (light.intensity / 100, light.intensity /
                             100, light.intensity / 100, 1)
                    gl.glLightfv(self.lights[light_num],
                                 gl.GL_AMBIENT, (0, 0, 0, 1))
                    gl.glLightfv(self.lights[light_num], gl.GL_DIFFUSE, color)
                    # gl.glLightfv(self.lights[light_num], gl.GL_SPECULAR, (1, 1, 1, 1))
                    light_num += 1

            gl.glClearColor(*self.mainCamera.clearColor)

            gl.glEnable(gl.GL_DEPTH_TEST)
            if config.faceCulling:
                gl.glEnable(gl.GL_CULL_FACE)

        self.start_scripts()

        if os.environ["PYUNITY_DEBUG_MODE"] == "1":
            print("Physics is", "on" if self.physics else "off")
            print("Scene \"" + self.name + "\" has started")

    def transform(self, transform):
        """
        Transform the matrix by a specified transform.

        Parameters
        ----------
        transform : Transform
            Transform to move

        """
        gl.glRotatef(*transform.rotation.angleAxisPair)
        gl.glScalef(*transform.scale)
        gl.glTranslatef(*(transform.position * Vector3(1, 1, -1)))

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

    def render(self):
        """Renders all GameObjects with MeshRenderers."""
        for gameObject in self.gameObjects:
            renderer = gameObject.GetComponent(MeshRenderer)
            if renderer and self.inside_frustrum(renderer):
                gl.glPushMatrix()
                self.transform(gameObject.transform)
                renderer.render()
                gl.glPopMatrix()

    def no_interactive(self):
        done = False
        clock = pygame.time.Clock()
        while not done:
            try:
                self.update_scripts()
                clock.tick(config.fps)
            except KeyboardInterrupt:
                print("Exiting")
                done = True

    def update(self):
        """Updating function to pass to the window provider."""
        self.update_scripts()

        if os.environ["PYUNITY_INTERACTIVE"] == "1":
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

            gl.glLoadIdentity()

            gl.glEnable(gl.GL_LIGHTING)
            gl.glEnable(gl.GL_COLOR_MATERIAL)
            gl.glColorMaterial(gl.GL_FRONT, gl.GL_AMBIENT_AND_DIFFUSE)

            light_num = 0
            for gameObject in self.gameObjects:
                light = gameObject.GetComponent(Light)
                if light:
                    gl.glEnable(self.lights[light_num])
                    pos = (*(gameObject.transform.position *
                             Vector3(1, 1, -1)), int(light.type))
                    gl.glLight(self.lights[light_num], gl.GL_POSITION, pos)
                    light_num += 1

            if (self.mainCamera.lastPos != self.mainCamera.transform.position or
                    self.mainCamera.lastRot != self.mainCamera.transform.rotation):
                pos = self.mainCamera.transform.position * Vector3(1, 1, -1)
                look = pos + \
                    self.mainCamera.transform.rotation.RotateVector(
                        Vector3.forward()) * Vector3(1, 1, -1)
                up = self.mainCamera.transform.rotation.RotateVector(
                    Vector3.up()) * Vector3(1, 1, -1)
                glu.gluLookAt(*pos, *look, *up)
                self.mainCamera.lastPos = self.mainCamera.transform.position
                self.mainCamera.lastRot = self.mainCamera.transform.rotation

            self.render()

            light_num = 0
            for gameObject in self.gameObjects:
                light = gameObject.GetComponent(Light)
                if light:
                    gl.glDisable(self.lights[light_num])
                    light_num += 1

            gl.glDisable(gl.GL_LIGHTING)
            gl.glDisable(gl.GL_COLOR_MATERIAL)
