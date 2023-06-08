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
           "SavesProjectID", "ShowInInspector", "SingleComponent", "Tag",
           "Transform", "addFields"]

from .scenes import Scene
from .values import Vector3, Quaternion, IncludeInstanceMixin, ABCMeta
from typing import (
    Dict, Iterator, List as _List, Type, TypeVar, Callable, Any, Tuple,
    Generic, Union, Mapping)

class Tag:
    tags: _List[str]
    tag: int
    tagName: str
    @classmethod
    def AddTag(cls, name: str) -> int: ...
    def __init__(self, tagNumOrName: Union[str, int]) -> None: ...

class SavesProjectID: ...

CT = TypeVar("CT", bound=Component)

class GameObject(SavesProjectID):
    name: str
    components: _List[Component]
    transform: Transform
    tag: Tag
    enabled: bool
    scene: Scene
    def __init__(self, name: str = ..., parent: GameObject | None = ...) -> None: ...
    @classmethod
    def BareObject(cls, name: str = ...) -> GameObject: ...
    def AddComponent(self, componentClass: Type[CT]) -> CT: ...
    def GetComponent(self, componentClass: Type[CT]) -> CT: ...
    def RemoveComponent(self, componentClass: Type) -> None: ...
    def GetComponents(self, componentClass: Type[CT]) -> _List[CT]: ...
    def RemoveComponents(self, componentClass: Type[CT]) -> None: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...

T = TypeVar("T")

class HideInInspector(Generic[T]):
    type: Type[T] | None
    default: T | None
    name: str | None
    def __init__(self, type_: Type[T] | None = ..., default: T | None = ...) -> None: ...
    def __set_name__(self, owner: Component, name: str) -> None: ...

class ShowInInspector(HideInInspector[T]):
    name: str | None
    def __init__(self, type: Type[T] | None = ..., default: T | None = ..., name: str | None = ...) -> None: ...
    def __set_name__(self, owner: Component, name: str) -> None: ...

class _AddFields(IncludeInstanceMixin):
    selfref: HideInInspector
    def __init__(self) -> None: ...
    def __call__(self, **kwargs: Dict[str, HideInInspector]) -> Callable[[Type[Component]], Type[Component]]: ...

addFields: _AddFields

class ComponentType(ABCMeta):
    @classmethod
    def __prepare__(cls, name: str, bases: Tuple[type, ...], /, **kwds: Any) -> Mapping[str, object]: ...

class Component(SavesProjectID, metaclass=ComponentType):
    _shown: Dict[str, HideInInspector] = ...
    _saved: Dict[str, HideInInspector] = ...
    gameObject: GameObject
    transform: Transform
    enabled: bool
    def __init__(self, transform: Transform, isDummy: bool = ...) -> None: ...
    @classmethod
    def __init_subclass__(cls) -> None: ...
    def AddComponent(self, componentClass: Type[CT]) -> CT: ...
    def GetComponent(self, componentClass: Type[CT]) -> CT: ...
    def RemoveComponent(self, componentClass: Type) -> None: ...
    def GetComponents(self, componentClass: Type[CT]) -> _List[CT]: ...
    def RemoveComponents(self, componentClass: Type[CT]) -> None: ...
    @property
    def scene(self) -> Scene: ...

class SingleComponent(Component): ...

class Transform(SingleComponent):
    localPosition: Vector3
    localRotation: Quaternion
    localScale: Vector3
    parent: Transform
    children: _List[Transform]
    def __init__(self, transform: None = ...) -> None: ...
    @property
    def position(self) -> Vector3: ...
    @position.setter
    def position(self, value: Vector3) -> None: ...
    @property
    def rotation(self) -> Quaternion: ...
    @rotation.setter
    def rotation(self, value: Quaternion) -> None: ...
    @property
    def localEulerAngles(self) -> Vector3: ...
    @localEulerAngles.setter
    def localEulerAngles(self, value: Vector3) -> None: ...
    @property
    def eulerAngles(self) -> Vector3: ...
    @eulerAngles.setter
    def eulerAngles(self, value: Vector3) -> None: ...
    @property
    def scale(self) -> Vector3: ...
    @scale.setter
    def scale(self, value: Vector3) -> None: ...
    def ReparentTo(self, parent: Transform) -> None: ...
    def List(self) -> None: ...
    def GetDescendants(self) -> Iterator[Transform]: ...
    def FullPath(self) -> str: ...
    def LookAtTransform(self, transform: Transform) -> None: ...
    def LookAtGameObject(self, gameObject: GameObject) -> None: ...
    def LookAtPoint(self, vec: Vector3) -> None: ...
    def LookInDirection(self, vec: Vector3) -> None: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
