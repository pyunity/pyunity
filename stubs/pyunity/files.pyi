## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""
Module to load files and scripts.
Also manages project structure.

"""

__all__ = ["Asset", "Behaviour", "File", "Prefab", "Project",
           "ProjectSavingContext", "Scripts", "Skybox", "Texture2D"]

from typing import List, Dict, Optional, Type, Union, TypeVar, Callable, Any
from types import ModuleType
from PIL import Image
from pathlib import Path
from .core import Component, ShowInInspector, GameObject, SavesProjectID
from .scenes import Scene
from .values import ABCMeta, abstractmethod, Vector3, Quaternion
from .meshes import Material
import ctypes

def convert(type: Type[ctypes._SimpleCData], list: List[float]) -> object: ...

class Behaviour(Component):
    _script: ShowInInspector = ...
    def Awake(self) -> None: ...
    async def Start(self) -> None: ...
    async def Update(self, dt: float) -> None: ...
    async def FixedUpdate(self, dt: float) -> None: ...
    async def LateUpdate(self, dt: float) -> None: ...
    def OnDestroy(self) -> None: ...

class Scripts:
    template: str = ...
    var: Dict[int, Type[Behaviour]] = ...
    @staticmethod
    def CheckScript(text: str) -> bool: ...
    @staticmethod
    def GenerateModule() -> ModuleType: ...
    @staticmethod
    def LoadScript(path: Union[str, Path], force: bool = ...) -> Union[Type[Behaviour], None]: ...
    @staticmethod
    def Reset() -> None: ...

class Asset(SavesProjectID, metaclass=ABCMeta):
    @abstractmethod
    def GetAssetFile(self, gameObject: GameObject) -> Path: ...
    @abstractmethod
    def SaveAsset(self, ctx: ProjectSavingContext) -> None: ...

class Texture2D(Asset):
    path: str
    img: Image.Image
    imgData: bytes
    loaded: bool
    texture: int
    mipmaps: bool
    def __init__(self, pathOrImg: Union[str, Path, Image.Image]) -> None: ...
    def load(self) -> None: ...
    def setImg(self, im: Image.Image) -> None: ...
    def use(self) -> None: ...
    @classmethod
    def FromOpenGL(cls, texture: int) -> Texture2D: ...

class Skybox:
    names: List[str] = ...
    points: List[int] = ...
    path: str
    compiled: bool
    images: List[Image.Image]
    def __init__(self, path: str) -> None: ...
    def compile(self) -> None: ...
    def use(self) -> None: ...

class Prefab(Asset):
    gameObjects: List[GameObject]
    assets: List[Asset]
    gameObject: GameObject
    def __init__(self, root: GameObject, prune: bool = ...) -> None: ...
    def Contains(self, obj: Union[GameObject, Component]) -> bool: ...
    def Instantiate(self,
                    scene: Optional[Scene] = ...,
                    parent: Optional[GameObject] = ...,
                    position: Vector3 = ...,
                    rotation: Quaternion = ...,
                    scale: Vector3 = ...,
                    worldSpace: bool = ...) -> GameObject: ...

AT = TypeVar("AT", bound=Asset)

class ProjectSavingContext:
    asset: Asset
    gameObject: GameObject
    project: Project
    filename: Union[str, Path]
    savers: Dict[Type[AT], Callable[[AT, Union[str, Path]], None]]
    def __init__(self, asset: Asset, gameObject: GameObject, project: Project, filename: Union[str, Path] = ...) -> None: ...

class File:
    path: str
    uuid: str
    def __init__(self, path: str, uuid: str) -> None: ...

def checkScene(func: Callable[..., Any]) -> Callable[..., Any]: ...

class Project:
    path: Path
    name: str
    _ids: Dict[str, Asset]
    _idMap: Dict[Asset, str]
    fileIDs: Dict[str, File]
    filePaths: Dict[str, File]
    firstScene: int
    def __init__(self, name: str = ...) -> None: ...
    @property
    def assets(self) -> List[Asset]: ...
    @checkScene
    def Write(self) -> None: ...
    @checkScene
    def ImportFile(self, file: File, uuid: Optional[str] = ..., write: bool = ...) -> None: ...
    @checkScene
    def ImportAsset(self, asset: Asset, gameObject: Optional[GameObject] = ..., filename: Optional[Union[str, Path]] = ...) -> None: ...
    @checkScene
    def SetAsset(self, file: File, obj: Asset) -> None: ...
    @checkScene
    def GetUuid(self, obj: Optional[Asset]) -> str: ...

    @staticmethod
    def FromFolder(folder: Union[str, Path]) -> Project: ...
