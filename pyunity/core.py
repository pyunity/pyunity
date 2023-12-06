## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

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
    Loaded PyUnity version 0.9.0
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
    [<Transform position=Vector3(-2, 0, 0) rotation=Quaternion(1, 0, 0, 0) scale=Vector3(1, 1, 1) path='/Root/Child1'>, <pyunity.MeshRenderer object at 0x00000170E4199CF0>]
    >>> child2.transform.children # List child2's children
    [<Transform position=Vector3(0, 5, 0) rotation=Quaternion(1, 0, 0, 0) scale=Vector3(1, 1, 1) path='/Root/Child2/Grandchild'>]

"""

__all__ = ["Component", "ComponentType", "GameObject", "HideInInspector",
           "SavedAttribute", "SavesProjectID", "ShowInInspector",
           "SingleComponent", "Space", "Tag", "Transform", "addFields"]

from . import Logger
from .errors import ComponentException, PyUnityException
from .values import ABCMeta, IncludeInstanceMixin, Quaternion, Vector3
import os
import enum

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

class SavesProjectID:
    """
    Base class for PyUnity classes to inherit. Instances of
    the subclass will have a UUID generated but no asset
    saved. Only used internally.

    """
    pass

class GameObject(SavesProjectID):
    """
    Class to create a GameObject, which is an object containing
    :class:`Component`\\s.

    Parameters
    ----------
    name : str, optional
        Name of GameObject
    parent : GameObject, optional
        Parent of GameObject, defaults to None

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
        self.transform = self.AddComponent(Transform)
        if parent is not None:
            self.transform.ReparentTo(parent.transform)
        self.tag = Tag(0)
        self.enabled = True
        self.scene = None

    @classmethod
    def BareObject(cls, name="GameObject"):
        """
        Create a bare GameObject with no components or attributes.

        Parameters
        ----------
        name : str
            Name of the GameObject

        """
        obj = cls.__new__(cls)
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
        componentClass : type
            Component to add. Must inherit from :class:`Component`

        Raises
        ------
        ComponentException
            If the provided component is not a component type,
        ComponentException
            If the component subclasses :class:`SingleComponent`
            and the GameObject already has a component of that
            type

        """
        if not isinstance(componentClass, type):
            raise ComponentException(
                f"Cannot add {componentClass!r} to the GameObject; "
                f"it is not a component"
            )
        if not issubclass(componentClass, Component):
            raise ComponentException(
                f"Cannot add {componentClass.__name__} to the GameObject; "
                f"it is not a component"
            )
        if (issubclass(componentClass, SingleComponent) and
                self.GetComponent(componentClass) is not None):
            raise ComponentException(
                f"Cannot add {componentClass.__name__} to the GameObject; "
                f"it already has one")

        component = Component.__new__(componentClass)
        if componentClass is Transform:
            component.transform = component
        else:
            component.transform = self.transform
        component.gameObject = self
        component.__init__()

        self.components.append(component)
        return component

    def GetComponent(self, componentClass):
        """
        Gets a component from the GameObject. Will return first match.

        For all matches, use :meth:`GameObject.GetComponents`.

        Parameters
        ----------
        componentClass : type
            Component to get. Must inherit from :class:`Component`

        Returns
        -------
        Component or None
            The specified component, or ``None`` if the component is not found

        """
        for component in self.components:
            if isinstance(component, componentClass):
                return component

        return None

    def RemoveComponent(self, componentClass):
        """
        Removes the first matching component from a GameObject.
        To remove all matching components, use
        :meth:`GameObject.RemoveComponents`.

        Parameters
        ----------
        componentClass : type
            Component to remove. Must inherit from :class:`Component`

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
        componentClass : type
            Component to get. Must inherit from :class:`Component`

        Returns
        -------
        list
            A list of all matching components

        """

        return [cpnt for cpnt in self.components if isinstance(cpnt, componentClass)]

    def RemoveComponents(self, componentClass):
        """
        Removes all matching component from a GameObject.

        Parameters
        ----------
        componentClass : type
            Component to remove. Must inherit from :class:`Component`

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
                f"{[type(x).__name__ for x in self.components]}>")
    def __str__(self):
        return (f"<GameObject name={self.name!r} components="
                f"{[type(x).__name__ for x in self.components]}>")

class SavedAttribute:
    """
    An attribute that should be saved when saving a project.
    Do not instantiate this class, only use one of its
    subclasses (either :class:`HideInInspector` or
    :class:`ShowInInspector`). However, this class will be
    used to reference an instance of either of these.

    """

    class _Sentinel:
        pass

    Sentinel = _Sentinel()
    del _Sentinel

class HideInInspector(SavedAttribute):
    """
    An attribute that should be saved when saving a project,
    but not shown in the Inspector of the PyUnityEditor.

    Parameters
    ----------
    Attributes
    ----------
    type : type
        Type of the attribute
    default : Any
        Default value for the attribute (will be set to the Component)

    Notes
    -----
    The class variable is replaced only when instances are created.
    For example:

    .. code-block:: python

        class MyBehaviour(Behaviour):
            attr = HideInInspector(str)

    If ``behaviour`` is an added component of type ``MyBehaviour``,
    accessing ``behaviour.attr`` would raise ``AttributeError``, and

    .. code-block:: python

        class MyBehaviour(Behaviour):
            attr = HideInInspector(str, "default string")

    Here, accessing ``behaviour.attr`` would return
    ``"default string"``.

    """

    def __init__(self, type_, default=SavedAttribute.Sentinel):
        if isinstance(type_, str):
            import pyunity
            if type_ not in pyunity.__all__:
                raise PyUnityException(f"No type named {type_!r}")
            self.type = getattr(pyunity, type_)
        else:
            self.type = type_
        if (isinstance(self.type, type) and issubclass(self.type, float)
                and isinstance(default, int)):
            self.default = float(default)
        else:
            self.default = default
        self.name = None

    def __set_name__(self, owner, name):
        owner._saved[name] = self

class ShowInInspector(HideInInspector):
    """
    An attribute that should be saved when saving a project,
    and shown in the Inspector of the PyUnityEditor.

    Parameters
    ----------
    type : type
        Type of the variable
    default : Any
        Default value (will be set to the Behaviour)
    name : str
        Alternate name shown in the Inspector. The
        default name is a properly capitalized phrase
        consisting of the words in the attribute name.
        For example, ``checkBox`` would be named
        ``Check Box`` and ``snake_case_Var`` would be
        named ``Snake Case Var``.

    """
    def __init__(self, type, default=SavedAttribute.Sentinel, name=None):
        super(ShowInInspector, self).__init__(type, default)
        self.name = name

    def __set_name__(self, owner, name):
        super(ShowInInspector, self).__set_name__(owner, name)
        owner._shown[name] = self

class _AddFields(IncludeInstanceMixin):
    def __init__(self):
        self.selfref = HideInInspector(type)

    def __call__(self, **kwargs):
        # To disambiguate between the two `self` parameters
        selfref = self.selfref

        class _decorator:
            def __init__(self, fields):
                self.fields = fields

            def apply(self, cls):
                return self.__call__(cls)

            def __call__(self, cls):
                for name, value in self.fields.items():
                    if "PYUNITY_SPHINX_CHECK" not in os.environ:
                        if not hasattr(cls, name):
                            if value.default is not SavedAttribute.Sentinel:
                                setattr(cls, name, value.default)

                    if value.name is None:
                        value.name = name
                    if value.type is selfref:
                        value.type = cls
                    cls._saved[name] = value
                    if isinstance(value, ShowInInspector):
                        cls._shown[name] = value
                return cls
        return _decorator(kwargs)

addFields = _AddFields()
del _AddFields
setattr(addFields, "__module__", __name__)

class ComponentType(ABCMeta):
    """
    Component metaclass to ensure that every subclass
    has its own unique ``_saved`` and ``_shown``
    attributes.

    """
    @classmethod
    def __prepare__(cls, name, bases, **kwds):
        namespace = dict(super(ComponentType, cls).__prepare__(name, bases, **kwds))
        namespace["_saved"] = {}
        namespace["_shown"] = {}
        return namespace

    def __getattr__(self, name):
        if name in self._saved:
            raise PyUnityException(
                "Cannot modify SavedAttribute of ComponentType; "
                "can only access attribute on instance")
        return super(ComponentType, self).__getattr__(name)

    def __setattr__(self, name, value):
        if name in self._saved:
            raise PyUnityException(
                "Cannot modify SavedAttribute of ComponentType; "
                "can only access attribute on instance")
        super(ComponentType, self).__setattr__(name, value)

class Component(SavesProjectID, metaclass=ComponentType):
    """
    Base class for built-in components.

    Attributes
    ----------
    gameObject : GameObject
        GameObject that the component belongs to.
    transform : Transform
        Transform that the component belongs to.

    Notes
    -----
    For a component to define an attribute visible in the
    PyUnity editor and savable in the scene file, a
    class variable needs to be defined using a subclass of
    :class:`SavedAttribute` with the appropriate type. This
    instance of :class:`SavedAttribute` will be replaced
    with its default value. See the notes for
    :class:`HideInInspector` for more details.

    Sometimes, the type for the :class:`SavedAttribute` is
    inaccessible from the current namespace, possibly
    because it is the component of which this attribute
    belongs to, or it is in another file which importing
    would cause a circular import. Or, the attribute that
    you want to define is a Python ``@property`` which means
    that you cannot define a class variable of the same
    name. In all three of these situations, a class variable
    would not work. The ``addFields`` decorator deals with
    this.

    For example:

    .. code-block:: python

        # in file1.py
        @addFields(attr1=HideInInspector(int, 5),
                   attr3=ShowInInspector(addFields.selfref, name="Attribute 3"))
        class SomeComponent(Component):
            attr4 = HideInInspector(str, "default value")

            @property
            def attr1(self):
                return 2

        # In another file
        from file1 import SomeComponent
        ...
        decorator = addFields(attr2=ShowInInspector(SomeTypeOnlyAccessibleHere))
        decorator.apply(SomeComponent)

    Here you can see that ``attr1`` is a property but is also
    a saved attribute, ``attr2`` is a saved attribute added
    after the class is defined, and ``attr3`` is a saved
    attribute with the type of ``SomeComponent``.

    """

    _saved = {}
    _shown = {}

    def __init__(self):
        super(Component, self).__init__()
        # gameObject and transform to be set by AddComponent
        self.enabled = True
        for attr in self._saved:
            if self._saved[attr].default is not SavedAttribute.Sentinel:
                newObj = self._getAttrCopy(self._saved[attr].default)
                setattr(self, attr, newObj)

    def _getAttrCopy(self, obj):
        if isinstance(obj, (Vector3, Quaternion, list, dict)):
            return obj.copy()
        return obj

    @classmethod
    def __init_subclass__(cls):
        if "PYUNITY_SPHINX_CHECK" not in os.environ:
            protected = ["gameObject", "transform", "enabled", "scene"]
            for name, val in cls._saved.items():
                if name in protected:
                    raise PyUnityException(f"Cannot use an attribute named one of {protected}")
                if val.name is None:
                    val.name = name
                delattr(cls, name)

    def AddComponent(self, componentClass):
        """
        Calls :meth:`GameObject.AddComponent` on the component's GameObject.

        Parameters
        ----------
        componentClass : Component
            Component to add. Must inherit from :class:`Component`

        """
        return self.gameObject.AddComponent(componentClass)

    def GetComponent(self, componentClass):
        """
        Calls :meth:`GameObject.GetComponent` on the component's GameObject.

        Parameters
        ----------
        componentClass : Component
            Component to get. Must inherit from :class:`Component`

        """
        return self.gameObject.GetComponent(componentClass)

    def RemoveComponent(self, componentClass):
        """
        Calls :meth:`GameObject.RemoveComponent` on the component's GameObject.

        Parameters
        ----------
        componentClass : Component
            Component to remove. Must inherit from :class:`Component`

        """
        return self.gameObject.RemoveComponent(componentClass)

    def GetComponents(self, componentClass):
        """
        Calls :meth:`GameObject.GetComponents` on the component's GameObject.

        Parameters
        ----------
        componentClass : Component
            Component to get. Must inherit from :class:`Component`

        """
        return self.gameObject.GetComponents(componentClass)

    def RemoveComponents(self, componentClass):
        """
        Calls :meth:`GameObject.RemoveComponents` on the component's GameObject.

        Parameters
        ----------
        componentClass : Component
            Component to remove. Must inherit from :class:`Component`

        """
        return self.gameObject.RemoveComponents(componentClass)

    @property
    def scene(self):
        """Get the scene of the GameObject."""
        return self.gameObject.scene

class Space(enum.Enum):
    World = enum.auto()
    Self = enum.auto()
    Local = Self

class SingleComponent(Component):
    """
    A base class for components that can only be added once.

    """
    pass

@addFields(
    localPosition=ShowInInspector(Vector3, name="position"),
    localRotation=ShowInInspector(Quaternion, name="rotation"),
    localScale=ShowInInspector(Vector3, name="scale"),
    parent=HideInInspector(addFields.selfref, None))
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
        formed by the Transform, not the GameObject.
        Do not modify this attribute.
    children : list
        List of children

    """

    def __init__(self):
        super(Transform, self).__init__()
        self._localPosition = Vector3.zero()
        self._localRotation = Quaternion.identity()
        self._localScale = Vector3.one()
        self.hasChanged = False
        self.children = []
        self.modelMatrix = None

    def _setChanged(self):
        self.hasChanged = True
        for child in self.children:
            child._setChanged()

    @property
    def localPosition(self):
        return self._localPosition

    @localPosition.setter
    def localPosition(self, value):
        if not isinstance(value, Vector3):
            raise PyUnityException(
                f"Cannot set position to object of type {type(value).__name__!r}")
        self._localPosition = value
        self._setChanged()

    @property
    def localRotation(self):
        return self._localRotation

    @localRotation.setter
    def localRotation(self, value):
        if not isinstance(value, Quaternion):
            raise PyUnityException(
                f"Cannot set rotation to object of type {type(value).__name__!r}")
        self._localRotation = value
        self._setChanged()

    @property
    def localScale(self):
        return self._localScale

    @localScale.setter
    def localScale(self, value):
        if not isinstance(value, Vector3):
            raise PyUnityException(
                f"Cannot set position to object of type {type(value).__name__!r}")
        self._localScale = value
        self._setChanged()

    @property
    def position(self):
        """Position of the Transform in world space."""
        if self.parent is None:
            return self.localPosition.copy()
        else:
            return self.parent.position + self.parent.rotation.RotateVector(
                self.localPosition) * self.parent.scale

    @position.setter
    def position(self, value):
        if not isinstance(value, Vector3):
            raise PyUnityException(
                f"Cannot set position to object of type {type(value).__name__!r}")

        if self.parent is None:
            self.localPosition = value
        else:
            self.localPosition = self.parent.rotation.conjugate.RotateVector(
                value - self.parent.position) / self.parent.scale

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
            self.localRotation = value * self.parent.rotation.conjugate

    @property
    def localEulerAngles(self):
        """
        Rotation of the Transform in local space.
        It is measured in degrees around x, y, and z.

        """
        return self.localRotation.eulerAngles

    @localEulerAngles.setter
    def localEulerAngles(self, value):
        if not isinstance(value, Vector3):
            raise PyUnityException(
                f"Cannot set localEulerAngles to object of type {type(value).__name__!r}")

        self.localRotation = Quaternion.Euler(value)

    @property
    def eulerAngles(self):
        """
        Rotation of the Transform in world space.
        It is measured in degrees around x, y, and z.

        """
        return self.rotation.eulerAngles

    @eulerAngles.setter
    def eulerAngles(self, value):
        if not isinstance(value, Vector3):
            raise PyUnityException(
                f"Cannot set eulerAngles to object of type {type(value).__name__!r}")

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

    @property
    def up(self):
        """
        Return a normalized vector pointing in the up direction
        of this Transform in world space.

        """
        return self.rotation.RotateVector(Vector3.up())

    @property
    def forward(self):
        """
        Return a normalized vector pointing in the forward direction
        of this Transform in world space.

        """
        return self.rotation.RotateVector(Vector3.forward())

    @property
    def right(self):
        """
        Return a normalized vector pointing in the right direction
        of this Transform in world space.

        """
        return self.rotation.RotateVector(Vector3.right())

    def Translate(self, translation, relativeTo=Space.Self):
        """
        Moves the transform in the direction and distance of ``translation``.

        Parameters
        ----------
        translation : Vector3
            Distance to translate by
        relativeTo : Space or Transform, optional
            If Space.Self, translates relative to the transform. If
            Space.World, trranslates relative to the world. If
            another transform, translates relative to that transform.
            By default Space.Self

        """
        if isinstance(relativeTo, Transform):
            self.position += relativeTo.TransformDirection(translation)
        elif relativeTo == Space.Self:
            self.localPosition += translation
        else:
            self.position += translation

    def Rotate(self, rotation, relativeTo=Space.Self):
        """
        Rotates the transform by either a quaternion or a vector
        of Euler angles (around the x, y and z axes).

        Parameters
        ----------
        rotation : Vector3 or Quaternion
            Amount to rotate by
        relativeTo : Space, optional
            If Space.Self, rotates relative to the transform.
            If Space.World, rotates relative to the world.
            By default Space.Self

        """
        if not isinstance(rotation, Quaternion):
            rotation = Quaternion.Euler(rotation)
        if relativeTo == Space.Self:
            self.rotation *= rotation
        else:
            self.rotation *= self.rotation * rotation * self.rotation.conjugate

    def ReparentTo(self, parent, relativeTo=Space.World):
        """
        Reparent a Transform.

        Parameters
        ----------
        parent : Transform
            The parent to reparent to.
        relativeTo : Space
            If Space.World, keeps the world space position, rotation
            and scale. If Space.Self, only preserves local space
            position, rotation and scale.

        """
        if self.parent is not None:
            self.parent.children.remove(self)
        if parent is not None:
            parent.children.append(self)

        if relativeTo == Space.World:
            oldPos = self.position
            oldRot = self.rotation
            oldScl = self.scale
            self.parent = parent
            self.position = oldPos
            self.rotation = oldRot
            self.scale = oldScl
        else:
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
        ----------
        transform : Transform
            Transform to face towards

        Notes
        -----
        The rotation generated may not be upright, and
        to fix this just use ``transform.rotation.eulerAngles *= Vector3(1, 1, 0)``
        which will remove the Z component of the Euler angles (the
        "roll" component). However, in most cases it will be upright.

        """
        v = transform.position - self.position
        self.rotation = Quaternion.FromDir(v)

    def LookAtGameObject(self, gameObject):
        """
        Face towards another GameObject's position. See
        :meth:`Transform.LookAtTransform` for details.

        Parameters
        ----------
        gameObject : GameObject
            GameObject to face towards

        """
        v = gameObject.transform.position - self.position
        self.rotation = Quaternion.FromDir(v)

    def LookAtPoint(self, vec):
        """
        Face towards a point. See
        :meth:`Transform.LookAtTransform` for details.

        Parameters
        ----------
        vec : Vector3
            Point to face towards

        """
        v = vec - self.position
        self.rotation = Quaternion.FromDir(v)

    def LookInDirection(self, vec):
        """
        Face in a vector direction (from origin to point).
        See :meth:`Transform.LookAtTransform` for details.

        Parameters
        ----------
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
