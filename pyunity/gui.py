__all__ = ["Canvas", "RectData", "RectAnchors",
           "RectOffset", "RectTransform", "Image2D", "Gui",
           "Text", "FontLoader", "GuiComponent",
           "NoResponseGuiComponent", "CheckBox",
           "TextAlign", "Font", "Button"]

from .errors import PyUnityException
from .values import Vector2, Color, RGB
from .core import Component, SingleComponent, GameObject, ShowInInspector
from .files import Texture2D
from .input import Input, MouseCode, KeyState
from .values import ABCMeta, abstractmethod
from PIL import Image, ImageDraw, ImageFont
from types import FunctionType
import os
import sys
import enum

class Canvas(Component):
    """
    A Component that manages GUI interactions
    and 2D rendering. Only GameObjects which
    are a descendant of a Canvas will be
    rendered.

    """
    def Update(self, updated):
        """
        Check if any components have been clicked on.

        Parameters
        ----------
        updated : list
            List of already updated GameObjects.
        """
        for descendant in self.transform.GetDescendants():
            if descendant in updated:
                continue
            updated.append(descendant)
            comp = descendant.GetComponent(GuiComponent)
            if comp is not None:
                comp.pressed = Input.GetMouse(MouseCode.Left)
                rectTransform = descendant.GetComponent(RectTransform)
                rect = rectTransform.GetRect() + rectTransform.offset
                pos = Vector2(Input.mousePosition)
                if rect.min < pos < rect.max:
                    if Input.GetMouseState(MouseCode.Left, KeyState.UP):
                        comp.Update()

class RectData:
    """
    Class to represent a 2D rect.

    Parameters
    ----------
    min_or_both : Vector2 or RectData
        Minimum value, or another RectData object
    max : Vector2 or None
        Maximum value. Default is None

    """
    def __init__(self, min_or_both=None, max=None):
        if min_or_both is None:
            self.min = Vector2.zero()
            self.max = Vector2.zero()
        elif max is None:
            if isinstance(min_or_both, RectData):
                self.min = min_or_both.min.copy()
                self.max = min_or_both.max.copy()
            else:
                self.min = min_or_both.copy()
                self.min = min_or_both.copy()
        else:
            self.min = min_or_both.copy()
            self.max = max.copy()

    def __repr__(self):
        """String representation of the RectData"""
        return "<{} min={} max={}>".format(self.__class__.__name__, self.min, self.max)

    def __add__(self, other):
        if isinstance(other, RectData):
            return RectData(self.min + other.min, self.max + other.max)
        else:
            return RectData(self.min + other, self.max + other)

    def __sub__(self, other):
        if isinstance(other, RectData):
            return RectData(self.min - other.min, self.max - other.max)
        else:
            return RectData(self.min - other, self.max - other)

    def __mul__(self, other):
        if isinstance(other, RectData):
            return RectData(self.min * other.min, self.max * other.max)
        else:
            return RectData(self.min * other, self.max * other)

class RectAnchors(RectData):
    """
    A type of RectData which represents
    the anchor points of a RectTransform.

    """

    def SetPoint(self, p):
        """
        Changes both the minimum and maximum anchor points.

        Parameters
        ----------
        p : Vector2
            Point
        
        """
        self.min = p.copy()
        self.max = p.copy()

    def RelativeTo(self, other):
        """
        Get RectData of another Rect relative to the
        anchor points.

        Parameters
        ----------
        other : RectData
            Querying rect

        Returns
        -------
        RectData
            Relative rect to this
        """
        parentSize = other.max - other.min
        absAnchorMin = other.min + (self.min * parentSize)
        absAnchorMax = other.min + (self.max * parentSize)
        return RectData(absAnchorMin, absAnchorMax)

class RectOffset(RectData):
    """
    Rect to represent the offset from the
    anchor points of a RectTransform.

    """

    @staticmethod
    def Rectangle(size, center=Vector2.zero()):
        """
        Create a rectangular RectOffset.

        Parameters
        ----------
        size : float or Vector2
            Size of offset
        center : Vector2, optional
            Central point of RectOffset, by default Vector2.zero()

        Returns
        -------
        RectOffset
            The generated RectOffset
        
        """
        return RectOffset(center - size / 2, center + size / 2)

    def Move(self, pos):
        """
        Move the RectOffset by a specified amount.

        Parameters
        ----------
        pos : Vector2
        
        """
        self.min += pos
        self.max += pos

    def SetCenter(self, pos):
        """
        Sets the center of the RectOffset. The size is preserved.

        Parameters
        ----------
        pos : Vector2
            Center point of the RectOffset
        
        """
        size = self.max - self.min
        self.min = pos - size / 2
        self.max = pos + size / 2

class RectTransform(SingleComponent):
    """
    A Component that represents the size, position and
    orientation of a 2D object.

    Attributes
    ----------
    anchors : RectAnchors
        Anchor points of the RectTransform. Measured
        between Vector2(0, 0) and Vector2(1, 1)
    offset : RectOffset
        Offset vectors representing the offset of
        opposite corners from the anchors. Measured
        in pixels
    pivot : Vector2
        Point in which the object rotates around.
        Measured between Vector2(0, 0) and Vector2(1, 1)
    rotation : float
        Rotation in degrees
    parent : RectTransform
        Parent RectTransform

    """

    anchors = ShowInInspector(RectAnchors)
    offset = ShowInInspector(RectOffset)
    pivot = ShowInInspector(Vector2)
    rotation = ShowInInspector(float, 0)
    def __init__(self, transform):
        super(RectTransform, self).__init__(transform)
        self.anchors = RectAnchors()
        self.offset = RectOffset()
        self.pivot = Vector2(0.5, 0.5)

    @property
    def parent(self):
        if self.transform.parent is not None:
            return self.transform.parent.GetComponent(RectTransform)

    def GetRect(self):
        """
        Gets screen coordinates of the bounding box.

        Returns
        -------
        RectData
            Screen coordinates
        
        """
        from .render import Screen
        if self.parent is None:
            return self.anchors * Screen.size
        else:
            parentRect = self.parent.GetRect() + self.parent.offset
            rect = self.anchors.RelativeTo(parentRect)
            return rect

class GuiComponent(Component, metaclass=ABCMeta):
    """
    A Component that represents a clickable area.

    """
    @abstractmethod
    def Update(self):
        pass

class NoResponseGuiComponent(GuiComponent):
    """
    A Component that blocks all clicks that are behind it.

    """
    def Update(self):
        """
        Empty Update function. This is to ensure
        nothing happens when the component is clicked.

        """
        pass

class Image2D(NoResponseGuiComponent):
    """
    A 2D image component, which is uninteractive.

    Attributes
    ----------
    texture : Texture2D
        Texture to render
    depth : float
        Z ordering of image. Higher depths are drawn on top.

    """
    texture = ShowInInspector(Texture2D)
    depth = ShowInInspector(float, 0.0)
    def __init__(self, transform):
        super(Image2D, self).__init__(transform)
        self.rectTransform = self.GetComponent(RectTransform)

class Button(GuiComponent):
    """
    A Component that calls a function when clicked.

    Attributes
    ----------
    callback : function
        Callback function
    state : KeyState
        Which state triggers the callback
    mouseButton : MouseCode
        Which mouse button triggers the callback
    pressed : bool
        If the button is pressed down or not

    """
    callback = ShowInInspector(FunctionType, lambda: None)
    state = ShowInInspector(KeyState, KeyState.UP)
    mouseButton = ShowInInspector(MouseCode, MouseCode.Left)
    pressed = ShowInInspector(bool, False)

    def Update(self):
        self.callback()

textureDir = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), "shaders", "gui", "textures")
buttonDefault = Texture2D(os.path.join(textureDir, "button.png"))
checkboxDefaults = [
    Texture2D(os.path.join(textureDir, "checkboxOff.png")),
    Texture2D(os.path.join(textureDir, "checkboxOn.png"))
]

class _FontLoader:
    """
    Base font loader. Uses ImageFont.
    
    """
    fonts = {}

    @classmethod
    def LoadFont(cls, name, size):
        """
        Loads and returns a Font object. This
        will internally call FontLoader.LoadFile,
        which will fail if the default FontLoader
        is :class:`_FontLoader`.

        Parameters
        ----------
        name : str
            Name of font. This should be either in
            the Windows registry, or can be found
            using fc-match.
        size : int
            Size, in points, of the font.

        Returns
        -------
        Font
            Generated Font object, or None if
            ``PYUNITY_TESTING`` is set.
        
        """
        if os.getenv("PYUNITY_TESTING") is not None:
            return None
        if name in cls.fonts:
            if size in cls.fonts[name]:
                return cls.fonts[name][size]
        else:
            cls.fonts[name] = {}
        file = cls.LoadFile(name)
        font = ImageFont.truetype(file, size)
        fontobj = Font(name, size, font)
        cls.fonts[name][size] = fontobj
        return fontobj

    @classmethod
    def LoadFile(cls, name):
        """
        Default file loader. Overriden to return
        the font file name. Raises PyUnityException by default.
        Do NOT call ``super().LoadFile()``.
        
        """
        raise PyUnityException("No font loading function found")

class WinFontLoader(_FontLoader):
    @classmethod
    def LoadFile(cls, name):
        """
        Use the Windows registry to find a font file name.

        Parameters
        ----------
        name : str
            Font name. This is not the same as the file name.

        Returns
        -------
        str
            Font file name

        Raises
        ------
        PyUnityException
            If the font is not found
        
        """
        import winreg
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Fonts\\")
        try:
            file = winreg.QueryValueEx(key, name + " (TrueType)")
        except WindowsError:
            file = None
        if file is None:
            raise PyUnityException(f"Cannot find font called {name!r}")
        return file[0]

class UnixFontLoader(_FontLoader):
    @classmethod
    def LoadFile(cls, name):
        """
        Use ``fc-match`` to find the font file name.

        Parameters
        ----------
        name : str
            Font name. This is not the same as the file name.

        Returns
        -------
        str
            Font file name

        Raises
        ------
        PyUnityException
            If the font is not found
        
        """
        import subprocess
        process = subprocess.Popen(["fc-match", name], stdout=subprocess.PIPE)
        stdout, _ = process.communicate()
        out = stdout.decode()
        if out == "":
            raise PyUnityException(f"Cannot find font called {name!r}")

        return out.split(": ")[0]

if sys.platform.startswith("linux") or sys.platform == "darwin":
    class FontLoader(UnixFontLoader): pass
    """Font loader, either :class:`UnixFontLoader` or :class:`WinFontLoader`."""
else:
    class FontLoader(WinFontLoader): pass
    """Font loader, either :class:`UnixFontLoader` or :class:`WinFontLoader`."""

class Font:
    """
    Font object to represent font data.

    Attributes
    ----------
    _font : ImageFont.FreeTypeFont
        Image font object. Do not use unless you know what you are doing.
    name : str
        Font name
    size : int
        Font size, in points
    
    """
    def __init__(self, name, size, imagefont):
        if not isinstance(imagefont, ImageFont.FreeTypeFont):
            raise PyUnityException("Please specify a FreeType font" +
                                   "created from ImageFont.freetype")

        self._font = imagefont
        self.name = name
        self.size = size

    def __reduce__(self):
        return (FontLoader.LoadFont, (self.name, self.size))

class TextAlign(enum.IntEnum):
    Left = enum.auto()
    Center = enum.auto()
    Right = enum.auto()

class Text(NoResponseGuiComponent):
    """
    Component to render text.

    Attributes
    ----------
    font : Font
        Font object to render
    text : str
        Contents of the Text
    color : Color
        Fill color
    depth : float
        Z ordering of the text. Higher values are on top.
    centeredX : TextAlign
        How to align in the X direction
    centeredY : TextAlign
        How to align in the Y direction
    rect : RectTransform
        RectTransform of the GameObject. Can be None
    texture : Texture2D
        Texture of the text, to save computation time.
    
    Notes
    -----
    Modifying :attr:`font`, :attr:`text`, or :attr:`color` will call
    :meth:`GenTexture`.
    
    """
    font = ShowInInspector(Font, FontLoader.LoadFont("Arial", 24))
    text = ShowInInspector(str, "Text")
    color = ShowInInspector(Color)
    depth = ShowInInspector(float, 0.1)
    centeredX = ShowInInspector(TextAlign, TextAlign.Left)
    centeredY = ShowInInspector(TextAlign, TextAlign.Center)
    def __init__(self, transform):
        super(Text, self).__init__(transform)
        self.rect = None
        self.texture = None
        self.color = RGB(255, 255, 255)

    def GenTexture(self):
        """
        Generate a :class:`Texture2D` to render.

        """
        if self.rect is None:
            self.rect = self.GetComponent(RectTransform)
            if self.rect is None:
                return

        rect = self.rect.GetRect() + self.rect.offset
        size = (rect.max - rect.min).abs()
        im = Image.new("RGBA", tuple(size), (255, 255, 255, 0))

        draw = ImageDraw.Draw(im)
        width, height = draw.textsize(self.text, font=self.font._font)
        if self.centeredX == TextAlign.Left:
            offX = 0
        elif self.centeredX == TextAlign.Center:
            offX = (size.x - width) // 2
        else:
            offX = size.x - width
        if self.centeredY == TextAlign.Left:
            offY = 0
        elif self.centeredY == TextAlign.Center:
            offY = (size.y - height) // 2
        else:
            offY = size.y - height

        draw.text((offX, offY), self.text, font=self.font._font,
                  fill=tuple(self.color))
        if self.texture is not None:
            self.texture.setImg(im)
        else:
            self.texture = Texture2D(im)

    def __setattr__(self, name, value):
        super(Text, self).__setattr__(name, value)
        if name in ["font", "text", "color"]:
            if self.gameObject.scene is not None:
                self.GenTexture()

class CheckBox(GuiComponent):
    """
    A component that updates the Image2D
    of its GameObject when clicked.

    Attributes
    ----------
    checked : bool
        Current state of the checkbox

    """
    checked = ShowInInspector(bool, False)

    def Update(self):
        """
        Inverts ``checked`` and updates the texture of
        the Image2D, if there is one.
        """
        self.checked = not self.checked
        cmp = self.GetComponent(Image2D)
        if cmp is not None:
            cmp.texture = checkboxDefaults[int(self.checked)]

class Gui:
    """
    Helper class to create GUI GameObjects.
    Do not instantiate.

    """
    @classmethod
    def MakeButton(cls, name, scene, text="Button", font=None, color=None, texture=None):
        """
        Create a Button GameObject and add all
        relevant GameObjects to the scene.

        Parameters
        ----------
        name : str
            Name of the GameObject
        scene : Scene
            Scene to add all generated GameObjects to
        text : str, optional
            Text content of the button, by default "Button"
        font : Font, optional
            Default font to use, if None then "Arial" is used
        color : Color, optional
            Fill color of the button text, by default black
        texture : Texture2D, optional
            Texture for the button background.

        Returns
        -------
        Tuple
            A tuple containing the :class:`RectTransform` of
            button, the :class:`Button` component and
            the :class:`Text` component.
        
        Notes
        -----
        This will create 3 GameObjects in this hierarchy::

            <specified button name>
            |- Button
            |- Text
        
        The ``Button`` GameObject will have two components,
        :class:`Button` and :class:`RectTransform`. The
        ``Button`` GameObject will have two components,
        :class:`Image2D` and :class:`RectTransform`.
        
        """
        if texture is None:
            texture = buttonDefault

        button = GameObject(name)
        transform = button.AddComponent(RectTransform)
        buttonComponent = button.AddComponent(Button)

        textureObj = GameObject("Button", button)
        transform2 = textureObj.AddComponent(RectTransform)
        transform2.anchors = RectAnchors(Vector2.zero(), Vector2.one())
        img = textureObj.AddComponent(Image2D)
        img.texture = texture
        img.depth = -0.1

        textObj = GameObject("Text", button)
        transform3 = textObj.AddComponent(RectTransform)
        transform3.anchors = RectAnchors(Vector2.zero(), Vector2.one())

        textComp = textObj.AddComponent(Text)
        textComp.text = text
        if font is None:
            font = FontLoader.LoadFont("Arial", 16)
        textComp.font = font
        if color is None:
            color = RGB(0, 0, 0)
        textComp.color = color
        textComp.centeredX = TextAlign.Center

        scene.Add(button)
        scene.Add(textureObj)
        return transform, buttonComponent, textComp

    @classmethod
    def MakeCheckBox(cls, name, scene):
        box = GameObject(name)
        transform = box.AddComponent(RectTransform)
        checkbox = box.AddComponent(CheckBox)
        img = box.AddComponent(Image2D)
        img.texture = checkboxDefaults[0]
        scene.Add(box)
        return transform, checkbox
