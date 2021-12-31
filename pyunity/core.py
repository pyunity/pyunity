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
    GLFW doesn't work, trying PySDL2
    Trying PySDL2 as a window provider
    Using window provider PySDL2
    Loaded PyUnity version 0.8.4
    >>> mat = Material(RGB(255, 0, 0)) # Create a default material
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

__all__ = ["Component", "GameObject", "Light", "SingleComponent",
           "MeshRenderer", "Tag", "Transform", "ShowInInspector",
           "HideInInspector", "LightType"]

import inspect
import enum
from .errors import *
from .meshes import Mesh
from .values import *
from . import Logger

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
            raise TypeError(f"Argument 1:"
                            f"expected str or int, got {type(tagNumOrName).__name__}")

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
        self.transform = None
        self.AddComponent(Transform)
        if parent:
            self.transform.ReparentTo(parent.transform)
        self.tag = Tag(0)
        self.enabled = True
        self.scene = None

    @staticmethod
    def BareObject(name="GameObject"):
        """
        Create a bare GameObject with no components or attributes.

        Parameters
        ==========
        name : str
            Name of the GameObject

        """
        obj = GameObject.__new__(GameObject)
        obj.name = name
        obj.components = []
        obj.transform = None
        obj.scene = None
        return obj

    def AddComponent(self, componentClass):
        """
        Adds a component to the GameObject.
        If it is a transform, set
        GameObject's transform to it.

        Parameters
        ----------
        componentClass : Component
            Component to add. Must inherit from :class:`Component`

        """
        if not issubclass(componentClass, Component):
            raise ComponentException(
                f"Cannot add {componentClass.__name__} to the GameObject; "
                f"it is not a component"
            )
        if not (
                issubclass(componentClass, SingleComponent) and
                any(isinstance(component, componentClass) for component in self.components)):
            component = componentClass(self.transform)
            self.components.append(component)
            if componentClass is Transform:
                self.transform = component
            elif issubclass(componentClass, Light):
                if self.scene is not None:
                    self.scene.RegisterLight(component)

            component.gameObject = self
            component.transform = self.transform
            return component
        else:
            raise ComponentException(
                f"Cannot add {componentClass.__name__} to the GameObject; "
                f"it already has one")

    def GetComponent(self, componentClass):
        """
        Gets a component from the GameObject.
        Will return first match.
        For all matches, use `GetComponents`.

        Parameters
        ----------
        componentClass : Component
            Component to get. Must inherit from :class:`Component`

        Returns
        -------
        Component or None
            The specified component, or `None` if the component is not found

        """
        for component in self.components:
            if isinstance(component, componentClass):
                return component

        return None

    def RemoveComponent(self, componentClass):
        """
        Removes the first matching component from a GameObject.

        Parameters
        ----------
        componentClass : type
            Component to remove

        Raises
        ------
        ComponentException
            If the GameObject doesn't have the specified component
        ComponentException
            If the specified component is a Transform

        """
        component = self.GetComponent(componentClass)
        if component is None:
            raise ComponentException(
                f"Cannot remove {componentClass.__name__} from the GameObject; "
                f"it doesn't have one")
        if componentClass is Transform:
            raise ComponentException(
                "Cannot remove a Transform from a GameObject")
        self.components.remove(component)

    def GetComponents(self, componentClass):
        """
        Gets all matching components from the GameObject.

        Parameters
        ----------
        componentClass : Component
            Component to get. Must inherit from :class:`Component`

        Returns
        -------
        list
            A list of all matching components

        """

        return [component for component in self.components if isinstance(component, componentClass)]

    def RemoveComponents(self, componentClass):
        """
        Removes all matching component from a GameObject.

        Parameters
        ----------
        componentClass : type
            Component to remove

        Raises
        ------
        ComponentException
            If the specified component is a Transform

        """
        components = self.GetComponents(componentClass)
        if componentClass is Transform:
            raise ComponentException(
                "Cannot remove a Transform from a GameObject")
        for component in components:
            self.components.remove(component)

    def __repr__(self):
        return (f"<GameObject name={self.name!r} components="
                f"{list(map(lambda x: type(x).__name__, self.components))}>")
    def __str__(self):
        return (f"<GameObject name={self.name!r} components="
                f"{list(map(lambda x: type(x).__name__, self.components))}>")

class HideInInspector:
    """
    An attribute that should be saved when saving a project,
    but not shown in the Inspector of the PyUnityEditor.

    Attributes
    ==========
    type : type
        Type of the variable
    default : Any
        Default value (will be set to the Behaviour)
    name : NoneType
        None

    """
    def __init__(self, type=None, default=None):
        self.type = type
        self.default = default
        self.name = None

class ShowInInspector(HideInInspector):
    """
    An attribute that should be saved when saving a project,
    and shown in the Inspector of the PyUnityEditor.

    Attributes
    ==========
    type : type
        Type of the variable
    default : Any
        Default value (will be set to the Behaviour)
    name : str
        Alternate name shown in the Inspector

    """
    def __init__(self, type=None, default=None, name=None):
        super(ShowInInspector, self).__init__(type, default)
        self.name = name

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

    shown = {}
    saved = {}

    def __init__(self, transform, is_dummy=False):
        if is_dummy:
            self.gameObject = None
        else:
            self.gameObject = transform.gameObject
        self.transform = transform
        self.enabled = True

    def __init_subclass__(cls):
        members = inspect.getmembers(cls, lambda a: not inspect.isroutine(a))
        variables = list(
            filter(lambda a: not (a[0].startswith("__")), members))
        shown = {a[0]: a[1]
                 for a in variables if isinstance(a[1], ShowInInspector)}
        saved = {a[0]: a[1]
                 for a in variables if isinstance(a[1], HideInInspector)}
        cls.shown = shown
        cls.saved = saved
        for name, val in saved.items():
            if val.type is None:
                val.type = cls
            if val.name is None:
                val.name = name
            setattr(cls, name, val.default)

    def AddComponent(self, component):
        """
        Calls `AddComponent` on the component's GameObject.

        Parameters
        ----------
        component : Component
            Component to add. Must inherit from :class:`Component`

        """
        return self.gameObject.AddComponent(component)

    def GetComponent(self, component):
        """
        Calls `GetComponent` on the component's GameObject.

        Parameters
        ----------
        componentClass : Component
            Component to get. Must inherit from :class:`Component`

        """
        return self.gameObject.GetComponent(component)

    def RemoveComponent(self, component):
        """
        Calls `RemoveComponent` on the component's GameObject.

        Parameters
        ----------
        component : Component
            Component to remove. Must inherit from :class:`Component`

        """
        return self.gameObject.RemoveComponent(component)

    def GetComponents(self, component):
        """
        Calls `GetComponents` on the component's GameObject.

        Parameters
        ----------
        componentClass : Component
            Component to get. Must inherit from :class:`Component`

        """
        return self.gameObject.GetComponents(component)

    def RemoveComponents(self, component):
        """
        Calls `RemoveComponents` on the component's GameObject.

        Parameters
        ----------
        component : Component
            Component to remove. Must inherit from :class:`Component`

        """
        return self.gameObject.RemoveComponents(component)

    @property
    def scene(self):
        """Get either the scene of the GameObject or the current running scene."""
        from .scenes import SceneManager
        if self.gameObject.scene is None:
            return SceneManager.CurrentScene()
        else:
            return self.gameObject.scene

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
        Do not modify this attribute.
    children : list
        List of children

    """

    localPosition = ShowInInspector(Vector3, None, "position")
    localRotation = ShowInInspector(Quaternion, None, "rotation")
    localScale = ShowInInspector(Vector3, None, "scale")
    parent = HideInInspector()

    def __init__(self, transform=None):
        super(Transform, self).__init__(self, True)
        assert transform is None
        self.localPosition = Vector3.zero()
        self.localRotation = Quaternion.identity()
        self.localScale = Vector3.one()
        self.parent = None
        self.children = []

    @property
    def position(self):
        """Position of the Transform in world space."""
        if self.parent is None:
            return self.localPosition.copy()
        else:
            return self.parent.position + self.localRotation.RotateVector(self.localPosition) * self.scale

    @position.setter
    def position(self, value):
        if not isinstance(value, Vector3):
            raise PyUnityException(
                f"Cannot set position to object of type {type(value).__name__!r}")

        if self.parent is None:
            self.localPosition = value
        else:
            self.localPosition = self.localRotation.conjugate.RotateVector(
                value / self.scale - self.parent.position)

    @property
    def rotation(self):
        """Rotation of the Transform in world space."""
        if self.parent is None:
            return self.localRotation.copy()
        else:
            return self.parent.rotation * self.localRotation

    @rotation.setter
    def rotation(self, value):
        if not isinstance(value, Quaternion):
            raise PyUnityException(
                f"Cannot set rotation to object of type {type(value).__name__!r}")

        if self.parent is None:
            self.localRotation = value
        else:
            self.localRotation = self.parent.rotation.conjugate * value

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
        self.rotation = Quaternion.Euler(value)

    @property
    def scale(self):
        """Scale of the Transform in world space."""
        if self.parent is None:
            return self.localScale.copy()
        else:
            return self.parent.scale * self.localScale

    @scale.setter
    def scale(self, value):
        if not isinstance(value, Vector3):
            raise PyUnityException(
                f"Cannot set scale to object of type {type(value).__name__!r}")
        if self.parent is None or not bool(self.parent.scale):
            self.localScale = value
        else:
            self.localScale = value / self.parent.scale

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

    def GetDescendants(self):
        """Iterate through all descedants of this Transform."""
        yield self
        for child in self.children:
            for subchild in child.GetDescendants():
                yield subchild

    def FullPath(self):
        """
        Gets the full path of the Transform.

        Returns
        -------
        str
            The full path of the Transform.

        """
        path = f"/{self.gameObject.name}"
        parent = self.parent
        while parent is not None:
            path = f"/{parent.gameObject.name}{path}"
            parent = parent.parent
        return path

    def LookAtTransform(self, transform):
        """
        Face towards another transform's position.

        Parameters
        ==========
        transform : Transform
            Transform to face towards

        Notes
        =====
        The rotation generated may not be upright, and
        to fix this just use ``transform.rotation.eulerAngles *= Vector3(1, 1, 0)``
        which will remove the Z component of the Euler angles.

        """
        v = transform.position - self.position
        self.rotation = Quaternion.FromDir(v)

    def LookAtGameObject(self, gameObject):
        """
        Face towards another GameObject's position. See `Transform.LookAtTransform` for details.

        Parameters
        ==========
        gameObject : GameObject
            GameObject to face towards

        """
        v = gameObject.transform.position - self.position
        self.rotation = Quaternion.FromDir(v)

    def LookAtPoint(self, vec):
        """
        Face towards a point. See `Transform.LookAtTransform` for details.

        Parameters
        ==========
        vec : Vector3
            Point to face towards

        """
        v = vec - self.position
        self.rotation = Quaternion.FromDir(v)

    def LookInDirection(self, vec):
        """
        Face in a vector direction (from origin to point). See `Transform.LookAtTransform` for details.

        Parameters
        ==========
        vec : Vector3
            Direction to face in

        """
        self.rotation = Quaternion.FromDir(vec)

    def __repr__(self):
        return (f"<Transform position={self.position} rotation={self.rotation}"
                f" scale={self.scale} path={self.FullPath()!r}>")
    def __str__(self):
        return (f"<Transform position={self.position} rotation={self.rotation}"
                f" scale={self.scale} path={self.FullPath()!r}>")

class LightType(enum.IntEnum):
    Point = 0
    Directional = 1
    Spot = 2

class Light(SingleComponent):
    """
    Component to hold data about the light in a scene.

    Attributes
    ----------
    intensity : int
        Intensity of light
    color : Color
        Light color (will mix with material color)
    type : LightType
        Type of light (currently only Point and
        Directional are supported)

    """

    intensity = ShowInInspector(int, 20)
    color = ShowInInspector(Color, RGB(255, 255, 255))
    type = ShowInInspector(LightType, LightType.Directional)

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

    DefaultMaterial = Material(RGB(200, 200, 200))
    DefaultMaterial.default = True
    mesh = ShowInInspector(Mesh)
    mat = ShowInInspector(Material, DefaultMaterial, "material")

    def Render(self):
        """Render the mesh that the MeshRenderer has."""
        if self.mesh is None:
            return

        self.mesh.compile()
        self.mesh.draw()
