"""
Core classes for the PyUnity library.

This module has some key classes used throughout PyUnity, and
have to be in the same file due to references both ways. Usually
when you create a scene, you should never create Components
directly, instead add them with AddComponent.

Example
-------
To create a GameObject with 2 children, one of which has its own child,
and all have MeshRenderers:

    >>> from pyunity import * # Import
    Loaded config
    Trying GLFW as a window provider
    GLFW doesn't work, trying Pygame
    Trying Pygame as a window provider
    Using window provider Pygame
    Loaded PyUnity version 0.0.5
    >>> mat = Material((255, 0, 0)) # Create a default material
    >>> root = GameObject("Root") # Create a root GameObjects
    >>> child1 = GameObject("Child1", root) # Create a child
    >>> child1.transform.position = Vector3(-2, 0, 0) # Move the child
    >>> renderer = child1.AddComponent(MeshRenderer) # Add a renderer
    >>> renderer.mat = mat # Add a material
    >>> renderer.mesh = Mesh.cube(2) # Add a mesh
    >>> child2 = GameObject("Child2", root) # Create another child
    >>> renderer = child2.AddComponent(MeshRenderer) # Add a renderer
    >>> renderer.mat = mat # Add a material
    >>> renderer.mesh = Mesh.quad(1) # Add a mesh
    >>> grandchild = GameObject("Grandchild", child2) # Add a grandchild
    >>> grandchild.transform.position = Vector3(0, 5, 0) # Move the grandchild
    >>> renderer = grandchild.AddComponent(MeshRenderer) # Add a renderer
    >>> renderer.mat = mat # Add a material
    >>> renderer.mesh = Mesh.cube(3) # Add a mesh
    >>> root.transform.List() # List all GameObjects
    /Root
    /Root/Child1
    /Root/Child2
    /Root/Child2/Grandchild
    >>> child1.components # List child1's components
    [<Transform position=Vector3(0, -2, 0) rotation=Quaternion(1, 0, 0, 0) scale=Vector3(2, 2, 2) path="/Root/Child1">, <pyunity.core.MeshRenderer object at 0x0AE3F688>]
    >>> child2.transform.children # List child2's children
    [<Transform position=Vector3(0, 0, 5) rotation=Quaternion(1, 0, 0, 0) scale=Vector3(3, 3, 3) path="/Root/Child2/Grandchild">]

"""

from .vector3 import Vector3
from .quaternion import Quaternion
from .errors import *
from .meshes import *
from OpenGL import GL as gl

tags = ["Default"]
"""List of current tags"""

class Tag:
    """
    Class to group GameObjects together without referencing the tags.
        
    Parameters
    ----------
    tagNumOrName : str or int
        Name or index of the tag
    
    Raises
    ------
    ValueError
        If there is no tag name
    IndexError
        If there is no tag at the provided index
    TypeError
        If the argument is not a str or int

    Attributes
    ----------
    tagName : str
        Tag name
    tag : int
        Tag index of the list of tags
    
    """

    @staticmethod
    def AddTag(self, name):
        """
        Add a new tag to the tag list.
        
        Parameters
        ----------
        name : str
            Name of the tag
        
        Returns
        -------
        int
            The tag index
        
        """
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
    """
    Class to create a GameObject, which is an object with components.
        
    Parameters
    ----------
    name : str, optional
        Name of GameObject
    parent : GameObject or None
        Parent of GameObject

    Attributes
    ----------
    name : str
        Name of the GameObject
    components : list
        List of components
    parent : GameObject or None
        Parent GameObject, if GameObject has one
    tag : Tag
        Tag that the GameObject has (defaults to tag 0 or Default)
    transform : Transform
        Transform that belongs to the GameObject
    
    """

    def __init__(self, name = "GameObject", parent = None):
        self.name = name
        self.components = []
        self.AddComponent(Transform)
        if parent: self.transform.ReparentTo(parent.transform)
        self.tag = Tag(0)
    
    def AddComponent(self, componentClass):
        """
        Adds a component to the GameObject.
        If it is a transform, set
        GameObject's transform to it.
        
        Parameters
        ----------
        componentClass : Component
            Component to add. Must inherit from `Component`
        
        """
        if not issubclass(componentClass, Component):
            raise ComponentError(
                "Cannot add " + repr(componentClass.__name__) + " to the GameObject; it is not a component"
            )
        if not (
                componentClass in (Transform, Camera, Light, MeshRenderer) and 
                any(isinstance(component, componentClass) for component in self.components)):
            component = componentClass()
            self.components.append(component)
            if componentClass is Transform:
                self.transform = component
            
            component.gameObject = self
            component.transform = self.transform
            return component
        else:
            raise ComponentError(
                "Cannot add " + repr(componentClass.__name__) + " to the GameObject; it already has one"
            )
    
    def GetComponent(self, componentClass):
        """
        Gets a component from the GameObject.
        Will return first match.
        For all matches, do a manual loop.
        
        Parameters
        ----------
        componentClass : Component
            Component to get. Must inherit from `Component`
        
        """
        for component in self.components:
            if isinstance(component, componentClass):
                return component
        
        return None

class Component:
    """
    Base class for built-in components.

    Attributes
    ----------
    gameObject : GameObject
        GameObject that the component belongs to.
    transform : Transform
        Transform that the component belongs to.
    
    """

    def __init__(self):
        self.gameObject = None
        self.transform = None
    
    def GetComponent(self, component):
        """
        Calls `GetComponent` on the component's GameObject.
        
        Parameters
        ----------
        componentClass : Component
            Component to get. Must inherit from `Component`
        
        """
        return self.gameObject.GetComponent(component)
    
    def AddComponent(self, component):
        """
        Calls `AddComponent` on the component's GameObject.
        
        Parameters
        ----------
        component : Component
            Component to add. Must inherit from `Component`
        
        """
        return self.gameObject.AddComponent(component)

class Behaviour(Component):
    """
    Base class for behaviours that can be scripted.

    Attributes
    ----------
    gameObject : GameObject
        GameObject that the component belongs to.
    transform : Transform
        Transform that the component belongs to.
    
    """

    def Start(self):
        """
        Called every time a scene is loaded up.
        
        """
        pass

    def Update(self, dt):
        """
        Called every frame.

        Parameters
        ----------
        dt : float
            Time since last frame, sent by the scene 
            that the Behaviour is in.
        
        """
        pass

class Transform(Component):
    """
    Class to hold data about a GameObject's transformation.

    Attributes
    ----------
    gameObject : GameObject
        GameObject that the component belongs to.
    position : Vector3
        Position of the Transform in world space.
    eulerAngles : Vector3
        Rotation of the Transform in world space.
        It is measured in degrees around x, y, and z.
    rotation : Quaternion
        Rotation of the Transform in world space.
    scale : Vector3
        Scale of the Transform in world space.
    localPosition : Vector3
        Position of the Transform in local space.
    localEulerAngles : Quaternion
        Rotation of the Transform in local space.
        It is measured in degrees around x, y, and z.
    localRotation : Quaternion
        Rotation of the Transform in local space.
    localScale : Vector3
        Scale of the Transform in local space.
    parent : Transform or None
        Parent of the Transform. The hierarchical tree is 
        actually formed by the Transform, not the GameObject.
    children : list
        List of children
    
    """

    def __init__(self):
        super(Transform, self).__init__()
        self.localPosition = Vector3.zero()
        self.localRotation = Quaternion.identity()
        self.localScale = Vector3.one()
        self.parent = None
        self.children = []
    
    @property
    def position(self):
        if self.parent is None: return self.localPosition
        else: return self.parent.position + self.localRotation.RotateVector(self.localPosition)
    
    @position.setter
    def position(self, value):
        if not isinstance(value, Vector3):
            raise PyUnityException("Cannot set position to object of type \"" + type(value).__name__)
        
        self.localPosition = value if self.parent is None else value - self.parent.position
    
    @property
    def rotation(self):
        if self.parent is None: return self.localRotation
        else: return self.localRotation * self.parent.rotation
    
    @rotation.setter
    def rotation(self, value):
        if not isinstance(value, Quaternion):
            raise PyUnityException("Cannot set rotation to object of type \"" + type(value).__name__)
        
        self.localRotation = value if self.parent is None else value * self.parent.rotation.conjugate
    
    @property
    def localEulerAngles(self):
        return self.localRotation.eulerAngles
    
    @localEulerAngles.setter
    def localEulerAngles(self, value):
        self.localRotation.eulerAngles = value
    
    @property
    def eulerAngles(self):
        return self.rotation.eulerAngles
    
    @eulerAngles.setter
    def eulerAngles(self, value):
        self.rotation.eulerAngles = value
    
    @property
    def scale(self):
        if self.parent is None: return self.localScale
        else: return self.parent.scale + self.localScale
    
    @scale.setter
    def scale(self, value):
        if not isinstance(value, Vector3):
            raise PyUnityException("Cannot set scale to object of type \"" + type(value).__name__)
        
        self.localScale = value if self.parent is None else value - self.parent.scale
    
    def ReparentTo(self, parent):
        """
        Reparent a Transform.

        Parameters
        ----------
        parent : Transform
            The parent to reparent to.
        
        """
        if parent: parent.children.append(self); self.parent = parent
    
    def List(self):
        """
        Prints the Transform's full path from the root, then
        lists the children in alphabetical order. This results in a
        nice list of all GameObjects.
        
        """
        print(self.FullPath())
        for child in sorted(self.children, key = lambda x: x.gameObject.name):
            child.List()
    
    def FullPath(self):
        """
        Gets the full path of the Transform.

        Returns
        -------
        str
            The full path of the Transform.
        
        """
        path = "/" + self.gameObject.name
        flag = self.parent is None
        parent = self.parent
        while parent is not None:
            path = "/" + parent.gameObject.name + path
            parent = parent.parent
        return path
    
    def __repr__(self):
        """
        Returns a string interpretation of the Transform.

        Returns
        -------
        str
            A string interpretation of the Transform. For example, the Main Camera would have
            a string interpretation of <Transform position=<Vector3 x=0 y=0 z=0>
            rotation=<Vector3 x=0 y=0 z=0> scale=<Vector3 x=1 y=1 z=1> path="/Main Camera">
        
        """
        return "<Transform position=" + str(self.position) + " rotation=" + str(self.rotation) + \
                " scale=" + str(self.scale) + " path=\"" + self.FullPath() + "\">"
    
    __str__ = __repr__

class Camera(Component):
    """
    Component to hold data about the camera in a scene.

    Attributes
    ----------
    fov : int
        Fov in degrees measured horizontally. Defaults to 90.
    near : float
        Distance of the near plane in the camera frustrum. Defaults to 0.05.
    far : float
        Distance of the far plane in the camera frustrum. Defaults to 100.
    clearColor : tuple
        Tuple of 4 floats of the clear color of the camera. Defaults to (.1, .1, .1, 1).
        Color mode is RGBA.
    
    """

    def __init__(self):
        super(Camera, self).__init__()
        self.fov = 90
        self.near = 0.05
        self.far = 100
        self.clearColor = (0, 0, 0, 1)

class Light(Component):
    """
    Component to hold data about the light in a scene.
    
    """

    def __init__(self):
        super(Light, self).__init__()
        self.intensity = 50
        self.type = 1

class MeshRenderer(Component):
    """
    Component to render a mesh at the position of a transform.

    Attributes
    ----------
    mesh : Mesh
        Mesh that the MeshRenderer will render.
    mat : Material
        Material to use for the mesh

    """

    def __init__(self):
        super(MeshRenderer, self).__init__()
        self.mesh = None
        self.mat = None

    def render(self):
        """
        Render the mesh that the MeshRenderer has.

        """
        gl.glBegin(gl.GL_TRIANGLES)
        gl.glColor3f(*self.mat.color)
        for index, triangle in enumerate(self.mesh.triangles):
            gl.glNormal3fv(list(self.mesh.normals[index]))
            for vertex in triangle:
                gl.glVertex3f(*self.mesh.verts[vertex])
        gl.glEnd()

class Material:
    """
    Class to hold data on a material.

    Attributes
    ----------
    color : list or tuple
        A list or tuple of 4 floats that make up a RGBA color.

    """

    def __init__(self, color):
        self.color = color