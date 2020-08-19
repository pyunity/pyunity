from .core import *
from . import config
from .errors import *

from OpenGL.GL import *
from OpenGL.GLU import *

from time import time

class SceneManager:
    def __init__(self):
        self.scenesByIndex = []
        self.scenesByName = {}
    
    def AddScene(self, sceneName):
        scene = Scene(sceneName)
        self.scenesByIndex.append(scene)
        self.scenesByName[sceneName] = scene
        return scene
    
    def GetSceneByIndex(self, index):
        return self.scenesByIndex[index]
    
    def GetSceneByName(self, name):
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
        
        self.window = config.windowProviders[config.windowProvider](config.size, self.name)

        glEnable(GL_DEPTH_TEST)
        if config.faceCulling:
            glEnable(GL_CULL_FACE)
        
        glClearColor(*self.mainCamera.clearColor)

        glMatrixMode(GL_PROJECTION)
        gluPerspective(self.mainCamera.fov / config.size[0] * config.size[1], config.size[0] / config.size[1], self.mainCamera.near, self.mainCamera.far)
        glMatrixMode(GL_MODELVIEW)

        glLightfv(GL_LIGHT0, GL_POSITION,  (5, 5, 5, 1))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))

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
        
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

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
        
        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHTING)
        glDisable(GL_COLOR_MATERIAL)