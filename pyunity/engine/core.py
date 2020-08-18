from .vector3 import Vector3
from .errors import *
from OpenGL.GL import *

tags = ["Default"]

class Tag:
    @staticmethod
    def AddTag(self, name):
        tags.append(name)
        return len(tags) - 1
    
    def __init__(self, tagNumOrName):
        if type(tagNumOrName) is str:
            self.tagName = tagNumOrName
            self.tag = tags.index(tagNumOrName)
        elif type(tagNumOrName) is int:
            self.tag = tagNumOrName
            self.tagName = tags[tagNumOrName]
        else:
            raise TypeError("Argument 1: expected str or int, got " + type(tagNumOrName).__name__)

class GameObject:
    def __init__(self, name = "GameObject", parent = None):
        self.name = name
        self.components = []
        self.AddComponent(Transform)
        if parent: self.transform.ReparentTo(parent.transform)
        self.tag = Tag(0)
    
    def AddComponent(self, componentClass):
        if not issubclass(componentClass, Component):
            raise ComponentError("Cannot add " + repr(componentClass.__name__) + " to the GameObject; it is not a component")
        if not (componentClass in (Transform, Camera) and any(isinstance(component, componentClass) for component in self.components)):
            component = componentClass()
            self.components.append(component)
            if componentClass is Transform:
                self.transform = component
            
            component.gameObject = self
            component.transform = self.transform
            return component
        else:
            raise ComponentError("Cannot add " + repr(componentClass.__name__) + " to the GameObject; it already has one")
    
    def GetComponent(self, componentClass):
        for component in self.components:
            if isinstance(component, componentClass):
                return component
        
        return None

class Component:
    def __init__(self):
        self.gameObject = None
        self.transform = None
    
    def GetComponent(self, component):
        return self.gameObject.GetComponent(component)
    
    def AddComponent(self, component):
        return self.gameObject.AddComponent(component)

class Behaviour(Component):
    def Start(self):
        pass

    def Update(self):
        pass

class Transform(Component):
    def __init__(self):
        super(Transform, self).__init__()
        self.position = Vector3(0, 0, 0)
        self.rotation = Vector3(0, 0, 0)
        self.scale = Vector3(1, 1, 1)
        self.parent = None
        self.children = []
    
    def ReparentTo(self, parent):
        if parent: parent.children.append(self); self.parent = parent
    
    def List(self):
        print(self.FullPath())
        for child in self.children:
            child.List()
    
    def FullPath(self):
        path = "/" + self.gameObject.name
        flag = self.parent is None
        parent = self.parent
        while parent is not None:
            path = "/" + parent.gameObject.name + path
            parent = parent.parent
        return path
    
    def __str__(self):
        return f"<Transform position={self.position} rotation={self.rotation} scale={self.scale} path={self.FullPath()}>"

class Camera(Component):

    fov = 90
    near = 0.5
    far = 100
    clearColor = (.1, .1, .1, 1)

    def __init__(self):
        super(Camera, self).__init__()

class Light(Component):
    def __init__(self):
        super(Light, self).__init__()

class MeshRenderer(Component):
    def __init__(self):
        super(MeshRenderer, self).__init__()
        self.mesh = None
        self.mat = None
    
    def move(self, transform):
        glRotatef(transform.rotation[0], 1, 0, 0)
        glRotatef(transform.rotation[1], 0, 1, 0)
        glRotatef(transform.rotation[2], 0, 0, 1)
        glTranslatef(transform.position[0],
                    transform.position[1],
                    transform.position[2])

    def render(self):
        for triangle in self.mesh.triangles:
            # glMaterialfv(GL_FRONT, GL_AMBIENT, [*self.mat.color, 1])
            glMaterialfv(GL_FRONT, GL_DIFFUSE, [*self.mat.color, 1])
            glBegin(GL_TRIANGLES)
            glVertex3f(*list(self.mesh.verts[triangle[0]] * -1))
            glVertex3f(*list(self.mesh.verts[triangle[1]] * -1))
            glVertex3f(*list(self.mesh.verts[triangle[2]] * -1))
            glEnd()
        
        for child in self.transform.children:
            renderer = child.GetComponent(MeshRenderer)
            if renderer:
                glPushMatrix()
                self.move(child)
                renderer.render()
                glPopMatrix()

class Mesh:
    def __init__(self, verts, triangles):
        self.verts = verts
        self.triangles = triangles

class Material:
    def __init__(self, color):
        self.color = color