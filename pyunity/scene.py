from .core import *
from . import config
from .errors import *
from . import physics
from time import time
import os

from OpenGL.GL import *
from OpenGL.GLU import *

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
        """
        Create a scene manager.

        """
        self.scenesByIndex = []
        self.scenesByName = {}
    
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
            raise PyUnityException("SceneManager already contains scene \"" + \
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
        if not isinstance(scene, Scene):
            raise PyUnityException("The provided scene is not of type Scene")
        if scene not in self.scenesByIndex:
            raise PyUnityException("Scene \"" + scene.name + "\" is not part of the SceneManager")
        self.scenesByIndex.remove(scene)
        self.scenesByName.pop(scene.name)

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
        light.transform.position = Vector3(10, 5, -5)
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
            if flag: self.gameObjects.remove(gameObject)
        else:
            raise PyUnityException("Cannot remove the Main Camera from the scene")
    
    def List(self):
        """
        Lists all the GameObjects currently in the scene.

        """
        for gameObject in sorted(self.rootGameObjects, key = lambda x: x.name):
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
            raise GameObjectException("No tag named " + name + "; create a new tag with Tag.AddTag")
        
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
            raise GameObjectException("No tag at index " + str(num) + "; create a new tag with Tag.AddTag")

    def start_scripts(self):
        """
        Start the scripts in the Scene.

        """
        self.lastFrame = time()

        for gameObject in self.gameObjects:
            for component in gameObject.components:
                if isinstance(component, Behaviour):
                    component.Start()

        self.physics = any(
            isinstance(
                component, physics.Collider
            ) for component in gameObject.components for gameObject in self.gameObjects
        )
        if self.physics:
            self.collManager = physics.CollManager()
            self.collManager.AddPhysicsInfo(self)
    
    def Start(self):
        """
        Start the internal parts of the
        Scene.

        """
        self.lights = [
            GL_LIGHT0,
            GL_LIGHT1,
            GL_LIGHT2,
            GL_LIGHT3,
            GL_LIGHT4,
            GL_LIGHT5,
            GL_LIGHT6,
            GL_LIGHT7
        ]

        glEnable(GL_DEPTH_TEST)
        if config.faceCulling:
            glEnable(GL_CULL_FACE)

        glEnable(GL_LIGHTING)

        light_num = 0
        for gameObject in self.gameObjects:
            light = gameObject.GetComponent(Light)
            if light:
                color = (light.intensity / 100, light.intensity / 100, light.intensity / 100, 1)
                glLightfv(self.lights[light_num], GL_DIFFUSE, color)
                glLightfv(self.lights[light_num], GL_SPECULAR, (1, 1, 1, 1))
                glEnable(self.lights[light_num])
                light_num += 1
        
        glColorMaterial(GL_FRONT, GL_EMISSION)
        glEnable(GL_COLOR_MATERIAL)
        
        glClearColor(*self.mainCamera.clearColor)

        glMatrixMode(GL_PROJECTION)
        gluPerspective(
            self.mainCamera.fov / config.size[0] * config.size[1],
            config.size[0] / config.size[1],
            self.mainCamera.near,
            self.mainCamera.far)
        glMatrixMode(GL_MODELVIEW)

        self.start_scripts()
        
        if os.environ["PYUNITY_DEBUG_MODE"] == "1":
            print("Physics is", "on" if self.physics else "off")
            print("Scene \"" + self.name + "\" has started")
    
    def Run(self):
        """
        Run the scene and create a window for it.

        """
        self.windowProvider = config.windowProvider
        self.window = self.windowProvider(config.size, self.name)
        self.Start()
        self.window.start(self.update)
    
    def transform(self, transform):
        """
        Transform the matrix by a specified transform.

        Parameters
        ----------
        transform : Transform
            Transform to move
        
        """
        glRotatef(*transform.rotation.angleAxisPair)
        glTranslatef(transform.position[0],
                    transform.position[1],
                    -transform.position[2])

    def update_scripts(self):
        for gameObject in self.gameObjects:
            for component in gameObject.components:
                if isinstance(component, Behaviour):
                    component.Update(max(time() - self.lastFrame, 0.001))

        if self.physics:
            self.collManager.Step(max(time() - self.lastFrame, 0.001))

        self.lastFrame = time()

    def update(self):
        """
        Updating function to pass to the window provider.

        """
        self.update_scripts()
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()
        gluLookAt(
            *(list(self.mainCamera.transform.position * Vector3(0, 0, -1))),
            *(list(self.mainCamera.transform.position * Vector3(0, 0, -1) - Vector3.forward())),
            0, 1, 0)

        glRotatef(*self.mainCamera.transform.rotation.angleAxisPair)

        light_num = 0
        for gameObject in self.gameObjects:
            light = gameObject.GetComponent(Light)
            if light:
                pos = (*(gameObject.transform.position * Vector3(0, 0, -1)), int(light.type))
                glLightfv(self.lights[light_num], GL_POSITION, pos)
                light_num += 1
        
        for gameObject in self.gameObjects:
            renderer = gameObject.GetComponent(MeshRenderer)
            if renderer:
                glPushMatrix()
                self.transform(gameObject.transform)
                renderer.render()
                glPopMatrix()