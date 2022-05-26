# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

__all__ = ["RAQM_SUPPORT", "Canvas", "RectData", "RectAnchors",
           "RectOffset", "RectTransform", "Image2D", "Gui",
           "Text", "FontLoader", "GuiComponent",
           "NoResponseGuiComponent", "CheckBox",
           "GuiRenderComponent", "TextAlign", "Font",
           "Button", "RenderTarget", "UnixFontLoader", "WinFontLoader"]

from . import Logger
from .errors import PyUnityException
from .values import Vector2, Color, RGB
from .core import Component, SingleComponent, GameObject, ShowInInspector, MeshRenderer, addFields
from .files import Texture2D, convert
from .input import Input, MouseCode, KeyState
from .values import ABCMeta, abstractmethod
from .render import Screen, Camera, Light
from PIL import Image, ImageDraw, ImageFont, features
from collections.abc import Callable
from contextlib import ExitStack
import OpenGL.GL as gl
import atexit
import os
import sys
import enum
import ctypes

if sys.version_info < (3, 9):
    from importlib_resources import files, as_file
else:
    from importlib.resources import files, as_file

RAQM_SUPPORT = features.check("raqm")
if not RAQM_SUPPORT:
    Logger.LogLine(Logger.INFO, "No raqm support, ligatures disabled")

class Canvas(Component):
    """
    A Component that manages GUI interactions
    and 2D rendering. Only GameObjects which
    are a descendant of a Canvas will be
    rendered.

    """

    def Update(self):
        """
        Check if any components have been hovered over.

        """
        for descendant in self.transform.GetDescendants():
            comp = descendant.GetComponent(GuiComponent)
            if comp is not None:
                rectTransform = descendant.GetComponent(RectTransform)
                rect = rectTransform.GetRect() + rectTransform.offset
                pos = Vector2(Input.mousePosition)
                if rect.min < pos < rect.max:
                    comp.HoverUpdate()

decorator = addFields(canvas=ShowInInspector(Canvas))
decorator(Camera)

class RectData:
    """
    Class to represent a 2D rect.

    Parameters
    ----------
    minOrBoth : Vector2 or RectData
        Minimum value, or another RectData object
    max : Vector2 or None
        Maximum value. Default is None

    """

    def __init__(self, minOrBoth=None, max=None):
        if minOrBoth is None:
            self.min = Vector2.zero()
            self.max = Vector2.zero()
        elif max is None:
            if isinstance(minOrBoth, RectData):
                self.min = minOrBoth.min.copy()
                self.max = minOrBoth.max.copy()
            else:
                self.min = minOrBoth.copy()
                self.max = minOrBoth.copy()
        else:
            self.min = minOrBoth.copy()
            self.max = max.copy()

    def size(self):
        return self.max - self.min

    def SetPoint(self, pos):
        """
        Changes both the minimum and maximum points.

        Parameters
        ----------
        pos : Vector2
            Point

        """
        self.min = pos.copy()
        self.max = pos.copy()

    def __repr__(self):
        """String representation of the RectData"""
        return "<{} min={} max={}>".format(self.__class__.__name__, self.min, self.max)

    def __eq__(self, other):
        if isinstance(other, RectData):
            return self.max == other.max and self.min == other.min
        return False

    def __hash__(self):
        return hash((self.min, self.max))

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

    def GetRect(self, bb=None):
        """
        Gets screen coordinates of the bounding box
        not including offset.

        Parameters
        ----------
        bb : Vector2, optional
            Bounding box to base anchors off of

        Returns
        -------
        RectData
            Screen coordinates

        """
        if self.parent is None:
            if bb is None:
                return self.anchors * Screen.size
            else:
                return self.anchors * bb
        else:
            parentRect = self.parent.GetRect() + self.parent.offset
            rect = self.anchors.RelativeTo(parentRect)
            return rect

class GuiComponent(Component, metaclass=ABCMeta):
    """
    A Component that represents a clickable area.

    """

    @abstractmethod
    def HoverUpdate(self):
        pass

class NoResponseGuiComponent(GuiComponent):
    """
    A Component that blocks all clicks that are behind it.

    """

    def HoverUpdate(self):
        """
        Empty HoverUpdate function. This is to ensure
        nothing happens when the component is clicked,
        and so components behind won't be updated.

        """
        pass

class GuiRenderComponent(NoResponseGuiComponent):
    """
    A Component that renders something in its RectTransform.

    """

    flipX = 0
    flipY = 0

    def PreRender(self):
        pass

class Image2D(GuiRenderComponent):
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

class RenderTarget(GuiRenderComponent):
    source = ShowInInspector(Camera)
    depth = ShowInInspector(float, 0.0)
    canvas = ShowInInspector(bool, True, "Render Canvas")
    flipY = 1

    def __init__(self, transform):
        super(RenderTarget, self).__init__(transform)
        self.setup = False
        self.size = Vector2.zero()
        self.texture = None
        self.renderPass = False

    def PreRender(self):
        if self.renderPass:
            return 1
        self.renderPass = True

        if self.source is self.scene.mainCamera:
            raise PyUnityException(
                "Cannot render main camera with main camera")

        rectTransform = self.GetComponent(RectTransform)
        if rectTransform is None:
            return

        previousShader = gl.glGetIntegerv(gl.GL_CURRENT_PROGRAM)
        previousVAO = gl.glGetIntegerv(gl.GL_VERTEX_ARRAY_BINDING)
        previousVBO = gl.glGetIntegerv(gl.GL_ARRAY_BUFFER_BINDING)
        previousFBO = gl.glGetIntegerv(gl.GL_DRAW_FRAMEBUFFER_BINDING)
        previousViewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
        previousDepthMask = gl.glGetIntegerv(gl.GL_DEPTH_WRITEMASK)

        self.genBuffers()
        size = (rectTransform.GetRect() + rectTransform.offset).size()
        if size != self.size:
            self.setSize(size)

        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.framebuffer)
        gl.glDepthMask(gl.GL_TRUE)
        self.source.Resize(*self.size)

        renderers = self.scene.FindComponentsByType(MeshRenderer)
        lights = self.scene.FindComponentsByType(Light)
        self.source.renderPass = True
        self.source.RenderScene(renderers, lights)
        self.source.RenderSkybox()

        if self.canvas and self.source.canvas is not None:
            previousProjection = self.source.guiShader.uniforms["projection"]
            self.source.Render2D()
            self.source.guiShader.setMat4(b"projection", previousProjection)

        gl.glUseProgram(previousShader)
        gl.glBindVertexArray(previousVAO)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, previousVBO)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, previousFBO)
        gl.glViewport(*previousViewport)
        gl.glDepthMask(previousDepthMask)

        self.renderPass = False

    def saveImg(self, path):
        previousFBO = gl.glGetIntegerv(gl.GL_DRAW_FRAMEBUFFER_BINDING)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.framebuffer)
        data = gl.glReadPixels(0, 0, *self.size,
                               gl.GL_RGB, gl.GL_UNSIGNED_BYTE)
        im = Image.frombytes("RGB", tuple(self.size), data)
        im.save(path)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, previousFBO)

    def genBuffers(self, force=False):
        if self.setup and not force:
            return

        self.framebuffer = gl.glGenFramebuffers(1)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.framebuffer)
        self.texID = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texID)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, *Screen.size,
                        0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, None)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glEnable(gl.GL_TEXTURE_2D)

        self.texture = Texture2D.FromOpenGL(self.texID)

        self.renderbuffer = gl.glGenRenderbuffers(1)
        gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, self.renderbuffer)
        gl.glRenderbufferStorage(gl.GL_RENDERBUFFER, gl.GL_DEPTH_COMPONENT, *Screen.size)
        gl.glFramebufferRenderbuffer(gl.GL_FRAMEBUFFER, gl.GL_DEPTH_ATTACHMENT, gl.GL_RENDERBUFFER, self.renderbuffer)
        gl.glFramebufferTexture(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, self.texID, 0)
        gl.glDrawBuffers(1, convert(ctypes.c_int, [gl.GL_COLOR_ATTACHMENT0]))

        if (gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) !=
                gl.GL_FRAMEBUFFER_COMPLETE):
            raise PyUnityException("Framebuffer setup failed")

        self.setup = True

    def setSize(self, size):
        self.size = round(size)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texID)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, *self.size,
                        0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, None)

        gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, self.renderbuffer)
        gl.glRenderbufferStorage(gl.GL_RENDERBUFFER,
                                 gl.GL_DEPTH_COMPONENT, *self.size)

class Button(GuiComponent):
    """
    A Component that calls a function when clicked.

    Attributes
    ----------
    callback : Callable
        Callback function
    state : KeyState
        Which state triggers the callback
    mouseButton : MouseCode
        Which mouse button triggers the callback
    pressed : bool
        If the button is pressed down or not

    """

    callback = ShowInInspector(Callable)
    state = ShowInInspector(KeyState, KeyState.UP)
    mouseButton = ShowInInspector(MouseCode, MouseCode.Left)
    pressed = ShowInInspector(bool, False)

    def __init__(self, transform):
        super(Button, self).__init__(transform)
        self.callback = lambda: None

    def HoverUpdate(self):
        if Input.GetMouseState(self.mouseButton, self.state):
            self.callback()

stack = ExitStack()
atexit.register(stack.close)
ref = files("pyunity") / "shaders/gui/textures"

buttonDefault = Texture2D(stack.enter_context(as_file(ref / "button.png")))
checkboxDefaults = [
    Texture2D(stack.enter_context(as_file(ref / "checkboxOff.png"))),
    Texture2D(stack.enter_context(as_file(ref / "checkboxOn.png")))
]
stack.close()

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
    def FromFile(cls, name, file, size):
        """
        Loads a font file into PyUnity.

        Parameters
        ----------
        name : str
            Font name
        file : str
            Path to the font file
        size : int
            Size in points of the font

        Returns
        -------
        Font
            The loaded font, or a preloaded one

        """
        if os.getenv("PYUNITY_TESTING") is not None:
            return None
        if name in cls.fonts:
            if size in cls.fonts[name]:
                return cls.fonts[name][size]
        else:
            cls.fonts[name] = {}
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
            raise PyUnityException(f"Cannot find font named {name!r}")
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
            raise PyUnityException(f"Cannot find font named {name!r}")

        return out.split(": ")[0]

if sys.platform.startswith("linux") or sys.platform == "darwin":
    class FontLoader(UnixFontLoader):
        pass
    """Font loader, either :class:`UnixFontLoader` or :class:`WinFontLoader`."""
else:
    class FontLoader(WinFontLoader):
        pass
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
            raise PyUnityException("Please specify a FreeType font "
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

    Top = Left
    Bottom = Right

class Text(GuiRenderComponent):
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

    font = ShowInInspector(Font)
    text = ShowInInspector(str, "Text")
    color = ShowInInspector(Color)
    depth = ShowInInspector(float, 0.1)
    centeredX = ShowInInspector(TextAlign, TextAlign.Left)
    centeredY = ShowInInspector(TextAlign, TextAlign.Center)
    def __init__(self, transform):
        super(Text, self).__init__(transform)
        self.font = FontLoader.LoadFont("Arial", 24)
        self.rect = None
        self.texture = None
        self.color = RGB(255, 255, 255)

    def PreRender(self):
        if self.texture is None:
            self.GenTexture()

    def GenTexture(self):
        """
        Generate a :class:`Texture2D` to render.

        """
        if self.rect is None:
            self.rect = self.GetComponent(RectTransform)
            if self.rect is None:
                return

        if self.font is None:
            return

        rect = self.rect.GetRect() + self.rect.offset
        size = (rect.max - rect.min).abs()
        im = Image.new("RGBA", tuple(round(size)), (255, 255, 255, 0))

        if RAQM_SUPPORT:
            ft = "-liga"
        else:
            ft = None

        draw = ImageDraw.Draw(im)
        width, height = draw.textsize(self.text, font=self.font._font,
                                      features=ft)
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
                  fill=tuple(self.color), features=ft)
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

    def HoverUpdate(self):
        """
        Inverts :attr:`checked` and updates the texture of
        the Image2D, if there is one.

        """
        if Input.GetMouseDown(MouseCode.Left):
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
        tuple
            A tuple containing the :class:`RectTransform` of
            button, the :class:`Button` component and
            the :class:`Text` component.

        Notes
        -----
        This will create 3 GameObjects in this hierarchy::

            <specified button name>
            |- Button
            |- Text

        The generated GameObject can be accessed from the
        ``gameObject`` property of the returned components.
        The :class:`Button` GameObject will have two components,
        :class:`Button` and :class:`RectTransform`. The
        :class:`Button` GameObject will have two components,
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
        scene.Add(textObj)
        scene.Add(textureObj)
        return transform, buttonComponent, textComp

    @classmethod
    def MakeCheckBox(cls, name, scene):
        """
        Create a CheckBox GameObject and add the
        appropriate components needed.

        Parameters
        ----------
        name : str
            Name of GameObject
        scene : Scene
            Scene to add GameObject to

        Returns
        -------
        tuple
            A tuple of the :class:`RectTransform` as well as the
            :class:`CheckBox` component.

        Notes
        -----
        The generated GameObject can be accessed from the
        ``gameObject`` property of the returned components.
        The GameObject will have 3 properties added: a
        :class:`RectTransform`, a :class:`CheckBox` and
        an :class:`Image2D`.

        """
        box = GameObject(name)
        transform = box.AddComponent(RectTransform)
        checkbox = box.AddComponent(CheckBox)
        img = box.AddComponent(Image2D)
        img.texture = checkboxDefaults[0]
        scene.Add(box)
        return transform, checkbox
