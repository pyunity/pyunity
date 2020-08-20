"""
Core classes for the PyUnity library.

This module has some key classes used throughout PyUnity, and
have to be in the same file due to references both ways. Usually
when you create a scene, you should never create Components
directly, instead add them with AddComponent.

Examples
--------
To create a GameObject with 2 children, one of which has its own child,
and all have MeshRenderers:

    >>> from pyunity import *
    GLUT doesn't work, using GLFW
    GLFW doesn't work, using Pygame
    Loaded PyUnity version 0.0.1
    Using window provider Pygame
    >>> mat = Material((1, 0, 0))
    >>> root = GameObject("Root")
    >>> child1 = GameObject("Child1", root)
    >>> child1.transform.position = Vector3(-2, 0, 0)
    >>> renderer = child1.AddComponent(MeshRenderer)
    >>> renderer.mat = mat
    >>> renderer.mesh = Mesh.cube(2)
    >>> child2 = GameObject("Child2", root)
    >>> renderer = child2.AddComponent(MeshRenderer)
    >>> renderer.mat = mat
    >>> renderer.mesh = Mesh.quad(1)
    >>> grandchild = GameObject("Grandchild", child2)
    >>> grandchild.transform.position = Vector3(0, 5, 0)
    >>> renderer = grandchild.AddComponent(MeshRenderer)
    >>> renderer.mat = mat
    >>> renderer.mesh = Mesh.cube(3)
    >>> root.transform.List()
    /Root
    /Root/Child1
    /Root/Child2
    /Root/Child2/Grandchild
    >>> child1.components
    [<Transform position=<Vector3 x=-2 y=0 z=0> rotation=<Vector3 x=0 y=0 z=0> scale=<Vector3 x=1 y=1 z=1> path="/Root/Child1">, <pyunity.core.MeshRenderer object at 0x0B5E1B68>]
    >>> child2.transform.children
    [<Transform position=<Vector3 x=0 y=5 z=0> rotation=<Vector3 x=0 y=0 z=0> scale=<Vector3 x=1 y=1 z=1> path="/Root/Child2/Grandchild">]

"""

from .vector3 import Vector3
from .errors import *
from .meshes import *
from OpenGL.GL import *

tags = ["Default"]

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
        if (
                not (componentClass in (Transform, Camera) and 
                any(isinstance(component, componentClass) for component in self.components))):
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
        Position of the Transform.
    rotation : Vector3
        Rotation of the Transform.
    scale : Vector3
        Scale of the Transform.
    parent : Transform or None
        Parent of the Transform. The hierarchical tree is 
        actually formed by the Transform, not the GameObject.
    children : list
        List of children
    
    """

    def __init__(self):
        super(Transform, self).__init__()
        self.position = Vector3(0, 0, 0)
        self.rotation = Vector3(0, 0, 0)
        self.scale = Vector3(1, 1, 1)
        self.parent = None
        self.children = []
    
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
        self.clearColor = (.1, .1, .1, 1)


class Light(Component):
    """
    (Experimental) Component to hold data about the light in a scene.

    Notes
    -----
    Lighting is not working yet, so all MeshRenderers will only display a sillhouette.
    
    """

    def __init__(self):
        super(Light, self).__init__()

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
    
    def move(self, transform):
        """
        Move the transformation matrix according to a transform.

        Parameters
        ----------
        transform : Transform
            Transform to move the transformation matrix according to.

        """
        glRotatef(transform.rotation[0], 1, 0, 0)
        glRotatef(transform.rotation[1], 0, 1, 0)
        glRotatef(transform.rotation[2], 0, 0, 1)
        glTranslatef(transform.position[0],
                    transform.position[1],
                    transform.position[2])

    def render(self):
        """
        Render the mesh that the MeshRenderer has.

        Notes
        -----
        It loops through the trianges in the mesh, then draws them. Each
        triangle has the same material, and when rendered, the mesh will
        be like a silhouette or shadow, do to the lack of lighting. When
        `render` is called, the MeshRenderer will call `render` on its
        own children, moving it accordingly. The `render` function
        assumes that the transform was applied already.

        """
        glBegin(GL_TRIANGLES)
        for index, triangle in enumerate(self.mesh.triangles):
            glNormal3fv(list(self.mesh.normals[index]))
            for vertex in triangle:
                glColor3f(*self.mat.color)
                glVertex3f(*list(self.mesh.verts[vertex] * -1))
        glEnd()
        
        for child in self.transform.children:
            renderer = child.GetComponent(MeshRenderer)
            if renderer:
                glPushMatrix()
                self.move(child)
                renderer.render()
                glPopMatrix()

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