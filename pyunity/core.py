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
    Loaded PyUnity version 0.5.0
    >>> mat = Material(Color(255, 0, 0)) # Create a default material
    >>> root = GameObject("Root") # Create a root GameObjects
    >>> child1 = GameObject("Child1", root) # Create a child
    >>> child1.transform.localPosition = Vector3(-2, 0, 0) # Move the child
    >>> renderer = child1.AddComponent(MeshRenderer) # Add a renderer
    >>> renderer.mat = mat # Add a material
    >>> renderer.mesh = Mesh.cube(2) # Add a mesh
    >>> child2 = GameObject("Child2", root) # Create another child
    >>> renderer = child2.AddComponent(MeshRenderer) # Add a renderer
    >>> renderer.mat = mat # Add a material
    >>> renderer.mesh = Mesh.quad(1) # Add a mesh
    >>> grandchild = GameObject("Grandchild", child2) # Add a grandchild
    >>> grandchild.transform.localPosition = Vector3(0, 5, 0) # Move the grandchild
    >>> renderer = grandchild.AddComponent(MeshRenderer) # Add a renderer
    >>> renderer.mat = mat # Add a material
    >>> renderer.mesh = Mesh.cube(3) # Add a mesh
    >>> root.transform.List() # List all GameObjects
    /Root
    /Root/Child1
    /Root/Child2
    /Root/Child2/Grandchild
    >>> child1.components # List child1's components
    [<Transform position=Vector3(-2, 0, 0) rotation=Quaternion(1, 0, 0, 0) scale=Vector3(1, 1, 1) path="/Root/Child1">, <pyunity.core.MeshRenderer object at 0x0A929460>]
    >>> child2.transform.children # List child2's children
    [<Transform position=Vector3(0, 5, 0) rotation=Quaternion(1, 0, 0, 0) scale=Vector3(1, 1, 1) path="/Root/Child2/Grandchild">]

"""

__all__ = ["Component", "GameObject", "Light", "Color",
           "Material", "MeshRenderer", "Tag", "Transform"]

import os
import glm
from .vector3 import Vector3
from .quaternion import Quaternion
from .errors import *
from . import Logger
if os.environ["PYUNITY_INTERACTIVE"] == "1":
    from OpenGL import GL as gl


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
    
    tags = ["Default"]
    """List of current tags"""

    @classmethod
    def AddTag(cls, name):
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
        cls.tags.append(name)
        return len(cls.tags) - 1

    def __init__(self, tagNumOrName):
        if type(tagNumOrName) is str:
            self.tagName = tagNumOrName
            self.tag = Tag.tags.index(tagNumOrName)
        elif type(tagNumOrName) is int:
            self.tag = tagNumOrName
            self.tagName = Tag.tags[tagNumOrName]
        else:
            raise TypeError(
                "Argument 1: expected str or int, got " + type(tagNumOrName).__name__)

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
    tag : Tag
        Tag that the GameObject has (defaults to tag 0 or Default)
    transform : Transform
        Transform that belongs to the GameObject

    """

    def __init__(self, name="GameObject", parent=None):
        self.name = name
        self.components = []
        self.AddComponent(Transform)
        if parent:
            self.transform.ReparentTo(parent.transform)
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
            raise ComponentException(
                "Cannot add " + repr(componentClass.__name__) +
                " to the GameObject; it is not a component"
            )
        if not (
                issubclass(componentClass, SingleComponent) and
                any(isinstance(component, componentClass) for component in self.components)):
            component = componentClass()
            self.components.append(component)
            if componentClass is Transform:
                self.transform = component

            component.gameObject = self
            component.transform = self.transform
            return component
        else:
            raise ComponentException(
                "Cannot add " + repr(componentClass.__name__) +
                " to the GameObject; it already has one"
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

    def __repr__(self):
        return "<GameObject name=" + repr(self.name) + " components=" + \
            str(list(map(lambda x: type(x).__name__, self.components))) + ">"
    __str__ = __repr__

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
        self.enabled = True

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

class SingleComponent(Component):
    """
    Represents a component that can be added only once.

    """
    pass

class Transform(SingleComponent):
    """
    Class to hold data about a GameObject's transformation.

    Attributes
    ----------
    gameObject : GameObject
        GameObject that the component belongs to.
    localPosition : Vector3
        Position of the Transform in local space.
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
        """Position of the Transform in world space."""
        if self.parent is None:
            return self.localPosition
        else:
            return self.parent.position + self.localRotation.RotateVector(self.localPosition)

    @position.setter
    def position(self, value):
        if not isinstance(value, Vector3):
            raise PyUnityException(
                "Cannot set position to object of type \"" + type(value).__name__)

        if self.parent is None:
            self.localPosition = value
        else:
            self.localRotation.conjugate.RotateVector(
                value - self.parent.position)

    @property
    def rotation(self):
        """Rotation of the Transform in world space."""
        if self.parent is None:
            return self.localRotation
        else:
            return self.localRotation * self.parent.rotation

    @rotation.setter
    def rotation(self, value):
        if not isinstance(value, Quaternion):
            raise PyUnityException(
                "Cannot set rotation to object of type \"" + type(value).__name__)

        self.localRotation = value if self.parent is None else value * \
            self.parent.rotation.conjugate

    @property
    def localEulerAngles(self):
        """
        Rotation of the Transform in local space.
        It is measured in degrees around x, y, and z.

        """
        return self.localRotation.eulerAngles

    @localEulerAngles.setter
    def localEulerAngles(self, value):
        self.localRotation.eulerAngles = value

    @property
    def eulerAngles(self):
        """
        Rotation of the Transform in world space.
        It is measured in degrees around x, y, and z.

        """
        return self.rotation.eulerAngles

    @eulerAngles.setter
    def eulerAngles(self, value):
        self.rotation.eulerAngles = value

    @property
    def scale(self):
        """Scale of the Transform in world space."""
        if self.parent is None:
            return self.localScale
        else:
            return self.parent.scale * self.localScale

    @scale.setter
    def scale(self, value):
        if not isinstance(value, Vector3):
            raise PyUnityException(
                "Cannot set scale to object of type \"" + type(value).__name__)
        if self.parent is None or not bool(self.parent.scale):
            self.localScale = value
        else:
            value / self.parent.scale

    def ReparentTo(self, parent):
        """
        Reparent a Transform.

        Parameters
        ----------
        parent : Transform
            The parent to reparent to.

        """
        if self.parent:
            self.parent.children.remove(self)
        if parent:
            parent.children.append(self)
        self.parent = parent

    def List(self):
        """
        Prints the Transform's full path from the root, then
        lists the children in alphabetical order. This results in a
        nice list of all GameObjects.

        """
        Logger.Log(self.FullPath())
        for child in sorted(self.children, key=lambda x: x.gameObject.name):
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
        parent = self.parent
        while parent is not None:
            path = "/" + parent.gameObject.name + path
            parent = parent.parent
        return path

    def LookAtTransform(self, transform):
        v0 = Vector3(0, 0, 1)
        v1 = transform.position - self.position
        xyz = v0.cross(v1)
        w = glm.sqrt(v0.get_length_sqrd() * v1.get_length_sqrd()) + v0.dot(v1)
        self.rotation = Quaternion(w, *xyz).normalized()

    def LookAtGameObject(self, gameObject):
        v0 = Vector3(0, 0, 1)
        v1 = gameObject.transform.position - self.position
        xyz = v0.cross(v1)
        w = glm.sqrt(v0.get_length_sqrd() * v1.get_length_sqrd()) + v0.dot(v1)
        self.rotation = Quaternion(w, *xyz).normalized()

    def LookAtVector(self, vec):
        v0 = Vector3(0, 0, 1)
        v1 = vec - self.position
        xyz = v0.cross(v1)
        w = glm.sqrt(v0.get_length_sqrd() * v1.get_length_sqrd()) + v0.dot(v1)
        self.rotation = Quaternion(w, *xyz).normalized()

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

class Light(SingleComponent):
    """
    Component to hold data about the light in a scene.

    """

    def __init__(self):
        super(Light, self).__init__()
        self.intensity = 100
        self.type = 1

class MeshRenderer(SingleComponent):
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

    def Render(self):
        """Render the mesh that the MeshRenderer has."""
        if self.mesh is None:
            return
        
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.mesh.vbo)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.mesh.ibo)
        gl.glBindVertexArray(self.mesh.vao)
        gl.glDrawElements(gl.GL_TRIANGLES, len(self.mesh.triangles) * 3, gl.GL_UNSIGNED_BYTE, None)

        # gl.glBegin(gl.GL_TRIANGLES)
        # gl.glColor3f(
        #     self.mat.color[0] / 255, self.mat.color[1] / 255, self.mat.color[2] / 255)
        # for triangle, normal in zip(self.mesh.triangles, self.mesh.normals):
        #     gl.glNormal3f(*normal)
        #     for vertex in triangle:
        #         gl.glVertex3f(*self.mesh.verts[vertex])
        # gl.glEnd()

class Material:
    """
    Class to hold data on a material.

    Attributes
    ----------
    color : list or tuple
        A list or tuple of 4 floats that make up a RGBA color.

    """

    def __init__(self, color, texture=None):
        self.color = color
        self.texture = texture

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    
    def __truediv__(self, other):
        return self.r / other, self.g / other, self.b / other