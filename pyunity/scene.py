from .core import *
from . import config
from .errors import *

from OpenGL.GL import *
from OpenGL.GLU import *

from time import time

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

class Scene:
    def __init__(self, name):
        self.name = name
        self.mainCamera = GameObject("Main Camera").AddComponent(Camera)
        light = GameObject("Light")
        light.AddComponent(Light)
        self.gameObjects = [self.mainCamera.gameObject, light]
        self.rootGameObjects = [self.mainCamera.gameObject, light]
    
    def Add(self, gameObject):
        self.gameObjects.append(gameObject)
        if gameObject.transform.parent is None:
            self.rootGameObjects.append(gameObject)
    
    def Remove(self, gameObject):
        if gameObject.name not in ["Main Camera"]:
            flag = False
            for go in self.gameObjects:
                if go == gameObject:
                    flag = True
                    break
            if flag: self.gameObjects.remove(gameObject)
    
    def List(self):
        for gameObject in sorted(self.rootGameObjects, key = lambda x: x.name):
            gameObject.transform.List()
    
    def FindGameObjectsByName(self, name):
        return [gameObject for gameObject in self.gameObjects if gameObject.name == name]
        
    def FindGameObjectsByTagName(self, name):
        if name in tags:
            return [gameObject for gameObject in self.gameObjects if gameObject.tag.tagName == name]
        else:
            raise GameObjectException("No tag named " + name + "; create a new tag with Tag.AddTag")
        
    def FindGameObjectsByTagNumber(self, num):
        if len(tags) > num:
            return [gameObject for gameObject in self.gameObjects if gameObject.tag.tag == num]
        else:
            raise GameObjectException("No tag at index " + str(num) + "; create a new tag with Tag.AddTag")
    
    def Run(self):
        self.lastFrame = time()

        for gameObject in self.gameObjects:
            for component in gameObject.components:
                if isinstance(component, Behaviour):
                    component.Start()
        
        self.windowProvider = config.windowProviders[config.windowProvider]
        self.window = self.windowProvider(config.size, self.name)

        glEnable(GL_DEPTH_TEST)
        if config.faceCulling:
            glEnable(GL_CULL_FACE)

        glLightfv(GL_LIGHT0, GL_POSITION, (1, 1, 0, 1))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
        glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))

        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (1, 1, 1, 1))
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, (0, 0, 0, 1))
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (.2, .2, .2, 1))
        
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_COLOR_MATERIAL)
        
        glClearColor(*self.mainCamera.clearColor)

        glMatrixMode(GL_PROJECTION)
        gluPerspective(
            self.mainCamera.fov / config.size[0] * config.size[1],
            config.size[0] / config.size[1],
            self.mainCamera.near,
            self.mainCamera.far)
        glMatrixMode(GL_MODELVIEW)

        self.window.start(self.update)
    
    def transform(self, transform):
        glRotatef(transform.rotation[0], 1, 0, 0)
        glRotatef(transform.rotation[1], 0, 1, 0)
        glRotatef(transform.rotation[2], 0, 0, 1)
        glTranslatef(transform.position[0],
                    transform.position[1],
                    transform.position[2])

    def update(self):
        for gameObject in self.gameObjects:
            for component in gameObject.components:
                if isinstance(component, Behaviour):
                    component.Update(max(time() - self.lastFrame, 0.001))

        self.lastFrame = time()
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()
        gluLookAt(0, 0, 0, 0, 0, -1, 0, 1, 0)

        glRotatef(self.mainCamera.transform.rotation[0], 1, 0, 0)
        glRotatef(self.mainCamera.transform.rotation[1], 0, 1, 0)
        glRotatef(self.mainCamera.transform.rotation[2], 0, 0, 1)
        glTranslatef(-self.mainCamera.transform.position[0],
                    -self.mainCamera.transform.position[1],
                    self.mainCamera.transform.position[2])

        for gameObject in self.rootGameObjects:
            renderer = gameObject.GetComponent(MeshRenderer)
            if renderer:
                glPushMatrix()
                self.transform(gameObject.transform)
                renderer.render()
                glPopMatrix()