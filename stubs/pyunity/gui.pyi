## Copyright (c) 2020-2022 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

__all__ = ["Canvas", "RectData", "RectAnchors",
           "RectOffset", "RectTransform", "Image2D", "Gui",
           "Text", "FontLoader", "GuiComponent",
           "NoResponseGuiComponent", "CheckBox",
           "GuiRenderComponent", "TextAlign", "Font",
           "Button", "RenderTarget"]

import enum
from pathlib import Path
from typing import Callable, Dict, List, NoReturn, Optional, Tuple, Type, Union, Any
from PIL import ImageFont
from .core import Component, SingleComponent, Transform
from .values import Vector2, ABCMeta, abstractmethod, Color
from .files import Texture2D
from .input import KeyState, MouseCode
from .scenes import Scene
from .render import Camera
from .events import EventLoop

_RAQM_SUPPORT: bool = ...

class Canvas(Component):
    def Update(self, loop: EventLoop) -> None: ...

class RectData:
    min: Vector2
    max: Vector2
    def __init__(self, min_or_both: Optional[Union[Vector2, RectData]] = ..., max: Optional[Vector2] = ...) -> None: ...
    def size(self) -> Vector2: ...
    def SetPoint(self, pos: Vector2) -> None: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other: Union[RectData, Any]) -> bool: ...
    def __hash__(self) -> int: ...
    def __add__(self, other: Union[RectData, Vector2, float]) -> RectData: ...
    def __sub__(self, other: Union[RectData, Vector2, float]) -> RectData: ...
    def __mul__(self, other: Union[RectData, Vector2, float]) -> RectData: ...

class RectAnchors(RectData):
    def RelativeTo(self, other: RectData) -> RectData: ...

class RectOffset(RectData):
    @staticmethod
    def Rectangle(size: Vector2, center: Vector2 = ...) -> RectOffset: ...
    @staticmethod
    def Square(size: Vector2, center: Vector2 = ...) -> RectOffset: ...
    def Move(self, pos: Vector2) -> None: ...
    def SetCenter(self, pos: Vector2) -> None: ...

class RectTransform(SingleComponent):
    anchors: RectAnchors = ...
    offset: RectOffset = ...
    pivot: Vector2 = ...
    rotation: float = ...
    @property
    def parent(self) -> RectTransform: ...
    def __init__(self, transform: Transform) -> None: ...
    def GetRect(self, bb: Optional[Vector2] = ...) -> RectData: ...

class GuiComponent(Component, metaclass=ABCMeta):
    @abstractmethod
    async def HoverUpdate(self) -> None: ...

class NoResponseGuiComponent(GuiComponent):
    async def HoverUpdate(self) -> None: ...

class GuiRenderComponent(NoResponseGuiComponent):
    flipX: int = ...
    flipY: int = ...

    def PreRender(self) -> None: ...

class Image2D(GuiRenderComponent):
    texture: Texture2D = ...
    depth: float = ...
    rectTransform: RectTransform
    def __init__(self, transform: Transform) -> None: ...

class RenderTarget(GuiRenderComponent):
    source: Camera = ...
    depth: float = ...
    canvas: bool = ...
    setup: bool
    size: Vector2
    texture: int
    renderPass: bool
    def __init__(self, transform: Transform) -> None: ...
    def PreRender(self) -> None: ...
    def saveImg(self, path: Union[str, Path]) -> None: ...
    def genBuffers(self, force: bool = ...) -> None: ...
    def setSize(self, size: Vector2) -> None: ...

class Button(GuiComponent):
    callback: Callable[[], None] = ...
    state: KeyState = ...
    mouseButton: MouseCode = ...
    pressed: bool = ...

    async def HoverUpdate(self) -> None: ...

buttonDefault: Texture2D = ...
checkboxDefaults: List[Texture2D] = ...

class _FontLoader:
    fonts: Dict[str, Font]

    @classmethod
    def LoadFont(cls, name: str, size: int) -> Font: ...
    @classmethod
    def FromFile(cls, name: str, file: str, size: int) -> Union[Font, None]: ...
    @classmethod
    def LoadFile(cls, name: str) -> NoReturn: ...

class WinFontLoader(_FontLoader):
    @classmethod
    def LoadFile(cls, name: str) -> str: ...

class UnixFontLoader(_FontLoader):
    @classmethod
    def LoadFile(cls, name: str) -> str: ...

class FontLoader(_FontLoader): ...

class Font:
    _font: ImageFont.FreeTypeFont
    name: str
    size: int
    def __init__(self, name: str, size: int, imagefont: ImageFont.FreeTypeFont) -> None: ...
    def __reduce__(self) -> Tuple[Callable[[str, int], Font], Tuple[str, int]]: ...

class TextAlign(enum.IntEnum):
    Left: TextAlign = ...
    Center: TextAlign = ...
    Right: TextAlign = ...
    Top: TextAlign = ...
    Bottom: TextAlign = ...

class Text(GuiRenderComponent):
    font: Font = ...
    text: str = ...
    color: Color = ...
    depth: float = ...
    centeredX: TextAlign = ...
    centeredY: TextAlign = ...
    rect: RectTransform
    texture: Texture2D
    def __init__(self, transform: Transform) -> None: ...
    def PreRender(self) -> None: ...
    def GenTexture(self) -> None: ...
    def __setattr__(self, name: str, value: object) -> None: ...

class CheckBox(GuiComponent):
    checked: bool = ...
    async def Update(self) -> None: ...

class Gui:
    @classmethod
    def MakeButton(
        cls, name: str, scene: Scene, text: str = ...,
        font: Optional[Font] = ..., color: Optional[Color] = ...,
        texture: Optional[Texture2D] = ...) -> Tuple[RectTransform, Button, Text]: ...
    @classmethod
    def MakeCheckBox(cls, name: str, scene: Scene) -> Tuple[RectTransform, CheckBox]: ...
