## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""Module for meshes created at runtime and their various attributes."""

__all__ = ["Mesh", "MeshRenderer", "Color", "RGB", "HSV", "Material"]

from .core import ShowInInspector, SingleComponent
from .files import Asset, convert
from .values import Mathf, Vector3
import OpenGL.GL as gl
from ctypes import c_uint, c_float, c_void_p
from pathlib import Path
import os
import colorsys
import itertools

floatSize = gl.sizeof(c_float)

class Mesh(Asset):
    """
    Class to create a mesh for rendering with a MeshRenderer

    Parameters
    ----------
    verts : list
        List of Vector3's containing each vertex
    triangles : list
        List of ints containing triangles joining up the vertices.
        Each int is the index of a vertex above.
    normals : list
        List of Vector3's containing the normal of each vertex.

    Attributes
    ----------
    verts : list
        List of Vector3's containing each vertex
    triangles : list
        List of lists containing triangles joining up the vertices.
        Each int is the index of a vertex above. The list is
        two-dimesional, meaning that each item in the list is a list
        of three ints.
    normals : list
        List of Vector3's containing the normal of each vertex.
    texcoords : list (optional)
        List of lists containing the texture coordinate of each vertex.
        The list is two-dimesional, meaning that each item in the list
        is a list of two floats.

    Notes
    -----
    When any of the mesh attributes are updated while
    a scene is running, you must use ``compile(force=True)``
    to update the mesh so that it is displayed correctly.

        >>> mesh = Mesh.cube(2)
        >>> mesh.vertices[1] = Vector3(2, 0, 0)
        >>> mesh.compile(force=True)

    """

    def __init__(self, verts, triangles, normals, texcoords=None):
        self.verts = verts
        self.triangles = triangles
        self.normals = normals
        if texcoords is not None:
            self.texcoords = texcoords
        else:
            self.texcoords = [[0, 0] for _ in range(len(self.verts))]

        self.compiled = False
        if ("PYUNITY_GL_CONTEXT" in os.environ and
                os.environ["PYUNITY_INTERACTIVE"] == "1"):
            self.compile()

        self.min = Vector3(
            min(v.x for v in verts),
            min(v.y for v in verts),
            min(v.z for v in verts),
        )
        self.max = Vector3(
            max(v.x for v in verts),
            max(v.y for v in verts),
            max(v.z for v in verts),
        )

    def compile(self, force=False):
        if not self.compiled or force:
            data = list(itertools.chain(*[[*item[0], *item[1], *item[2]]
                                          for item in zip(self.verts, self.normals, self.texcoords)]))
            indices = list(itertools.chain(*self.triangles))

            self.vbo = gl.glGenBuffers(1)
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
            gl.glBufferData(gl.GL_ARRAY_BUFFER, len(data) * floatSize,
                            convert(c_float, data), gl.GL_STATIC_DRAW)
            self.ibo = gl.glGenBuffers(1)
            gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ibo)
            gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, len(indices) * gl.sizeof(c_uint),
                            convert(c_uint, indices), gl.GL_STATIC_DRAW)

            self.vao = gl.glGenVertexArrays(1)
            gl.glBindVertexArray(self.vao)
            gl.glVertexAttribPointer(
                0, 3, gl.GL_FLOAT, gl.GL_FALSE, 8 * floatSize, None)
            gl.glEnableVertexAttribArray(0)
            gl.glVertexAttribPointer(
                1, 3, gl.GL_FLOAT, gl.GL_FALSE, 8 * floatSize, c_void_p(3 * floatSize))
            gl.glEnableVertexAttribArray(1)
            gl.glVertexAttribPointer(
                2, 2, gl.GL_FLOAT, gl.GL_FALSE, 8 * floatSize, c_void_p(6 * floatSize))
            gl.glEnableVertexAttribArray(2)

            self.compiled = True

    def draw(self):
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBindVertexArray(self.vao)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ibo)
        gl.glDrawElements(gl.GL_TRIANGLES, len(
            self.triangles) * 3, gl.GL_UNSIGNED_INT, None)

    def copy(self):
        """
        Create a copy of the current Mesh.

        Returns
        -------
        Mesh
            Copy of the mesh
        """
        return Mesh(self.verts, self.triangles, self.normals, self.texcoords)

    def GetAssetFile(self, gameObject):
        return Path("Meshes") / (gameObject.name + ".mesh")

    def SaveAsset(self, ctx):
        path = ctx.project.path / ctx.filename
        ctx.savers[Mesh](self, ctx.project, path)

    @staticmethod
    def quad(size):
        """
        Creates a quadrilateral mesh.

        Parameters
        ----------
        size : float
            Side length of quad

        Returns
        -------
        Mesh
            A quad centered at Vector3(0, 0, 0) with side length of ``size``
            facing in the direction of the positive z axis.

        """
        half = size / 2
        return Mesh(
            [
                Vector3(-half, half, 0), Vector3(half, half, 0),
                Vector3(half, -half, 0), Vector3(-half, -half, 0)
            ],
            [[0, 1, 2], [0, 2, 3]],
            [Vector3.forward(), Vector3.forward(),
             Vector3.forward(), Vector3.forward()],
            [[0, 0], [0, 1], [1, 1], [1, 0]]
        )

    @staticmethod
    def doubleQuad(size):
        """
        Creates a two-sided quadrilateral mesh.

        Parameters
        ----------
        size : float
            Side length of quad

        Returns
        -------
        Mesh
            A double-sided quad centered at Vector3(0, 0) with side length
            of ``size``.

        """
        half = size / 2
        return Mesh(
            [
                Vector3(half, half, 0), Vector3(-half, half, 0),
                Vector3(-half, -half,
                        0), Vector3(half, -half, 0),
                Vector3(half, half, 0), Vector3(-half, half, 0),
                Vector3(-half, -half,
                        0), Vector3(half, -half, 0),
            ],
            [[0, 1, 2], [0, 2, 3], [4, 6, 5], [4, 7, 6]],
            [
                Vector3.forward(), Vector3.forward(), Vector3.forward(),
                Vector3.forward(), Vector3.back(), Vector3.back(),
                Vector3.back(), Vector3.back()
            ],
            [[0, 0], [0, 1], [1, 1], [1, 0], [0, 0], [0, 1], [1, 1], [1, 0]]
        )

    @staticmethod
    def cylinder(radius, height, detail=32):
        verts = []
        normals = []
        triangles = []

        verts.append(Vector3(0, height / 2, 0))
        normals.append(Vector3(0, 1, 0))
        for i in range(detail):
            angle = i / detail * Mathf.PI * 2
            verts.append(Vector3(radius * Mathf.Cos(angle), height / 2, radius * Mathf.Sin(angle)))
            normals.append(Vector3(0, 1, 0))
            triangles.append([i + 1, 0, i + 2])
        verts.append(Vector3(radius, height / 2, 0))
        normals.append(Vector3(0, 1, 0))

        offset = len(verts)
        verts.append(Vector3(0, -height / 2, 0))
        normals.append(Vector3(0, -1, 0))
        for i in range(detail):
            angle = i / detail * Mathf.PI * 2
            verts.append(Vector3(radius * Mathf.Cos(angle), -height / 2, radius * Mathf.Sin(angle)))
            normals.append(Vector3(0, -1, 0))
            triangles.append([offset + i + 1, offset + i + 2, offset])
        verts.append(radius * Vector3(1, -height / 2, 0))
        normals.append(Vector3(0, -1, 0))

        offset = len(verts)
        for i in range(detail):
            angle = i / detail * Mathf.PI * 2
            verts.append(Vector3(radius * Mathf.Cos(angle), height / 2, radius * Mathf.Sin(angle)))
            verts.append(Vector3(radius * Mathf.Cos(angle), -height / 2, radius * Mathf.Sin(angle)))
            normals.append(Vector3(Mathf.Cos(angle), 0, Mathf.Sin(angle)))
            normals.append(Vector3(Mathf.Cos(angle), 0, Mathf.Sin(angle)))
            triangles.append([offset + i * 2, offset + i * 2 + 2, offset + i * 2 + 1])
            triangles.append([offset + i * 2 + 2, offset + i * 2 + 3, offset + i * 2 + 1])
        verts.append(Vector3(radius, height / 2, 0))
        verts.append(Vector3(radius, -height / 2, 0))
        normals.append(Vector3(1, 0, 0))
        normals.append(Vector3(1, 0, 0))

        return Mesh(verts, triangles, normals)

    @staticmethod
    def sphere(size, detail=16):
        verts = []
        normals = []
        texcoords = []
        for i in range(detail * 2):
            azimuth = i / detail * Mathf.PI
            for j in range(detail + 1):
                polar = j / detail * Mathf.PI
                x = Mathf.Cos(azimuth) * Mathf.Sin(polar)
                y = Mathf.Cos(polar)
                z = Mathf.Sin(azimuth) * Mathf.Sin(polar)
                point = Vector3(x, y, z)
                verts.append(point * size)
                normals.append(point)
                texcoords.append([i / detail / 2 % 1, j / detail % 1])

        triangles = []
        for i in range(detail * 2):
            for j in range(detail):
                inext = i + 1 if i < detail * 2 - 1 else 0
                jnext = j + 1
                a = i * (detail + 1) + j
                b = inext * (detail + 1) + j
                c = i * (detail + 1) + jnext
                d = inext * (detail + 1) + jnext
                if j != 0:
                    triangles.append([a, b, c])
                if j != detail - 1:
                    triangles.append([b, d, c])

        return Mesh(verts, triangles, normals, texcoords)

    @staticmethod
    def capsule(radius, height, detail=16):
        verts = []
        normals = []
        triangles = []

        for i in range(detail * 2):
            azimuth = i / detail * Mathf.PI
            for j in range(detail // 2 + 1):
                polar = j / detail * Mathf.PI
                x = Mathf.Cos(azimuth) * Mathf.Sin(polar)
                y = Mathf.Cos(polar)
                z = Mathf.Sin(azimuth) * Mathf.Sin(polar)
                point = Vector3(x, y, z)
                verts.append((point + Vector3(0, height / 2, 0)) * radius)
                normals.append(point)

        for i in range(detail * 2):
            for j in range(detail // 2):
                inext = i + 1 if i < detail * 2 - 1 else 0
                jnext = j + 1
                a = i * (detail // 2 + 1) + j
                b = inext * (detail // 2 + 1) + j
                c = i * (detail // 2 + 1) + jnext
                d = inext * (detail // 2 + 1) + jnext
                if j != 0:
                    triangles.append([a, b, c])
                triangles.append([b, d, c])

        offset = len(verts)
        for i in range(detail * 2):
            azimuth = i / detail * Mathf.PI
            for j in range(detail // 2 + 1):
                polar = (1 - j / detail) * Mathf.PI
                x = Mathf.Cos(azimuth) * Mathf.Sin(polar)
                y = Mathf.Cos(polar)
                z = Mathf.Sin(azimuth) * Mathf.Sin(polar)
                point = Vector3(x, y, z)
                verts.append((point - Vector3(0, height / 2, 0)) * radius)
                normals.append(point)

        for i in range(detail * 2):
            for j in range(detail // 2):
                inext = i + 1 if i < detail * 2 - 1 else 0
                jnext = j + 1
                a = offset + i * (detail // 2 + 1) + j
                b = offset + inext * (detail // 2 + 1) + j
                c = offset + i * (detail // 2 + 1) + jnext
                d = offset + inext * (detail // 2 + 1) + jnext
                if j != 0:
                    triangles.append([a, c, b])
                triangles.append([b, c, d])

        for i in range(detail * 2):
            inext = i + 1 if i < detail * 2 - 1 else 0
            a = i * (detail // 2 + 1) + detail // 2
            b = inext * (detail // 2 + 1) + detail // 2
            triangles.append([a, b, a + offset])
            triangles.append([a + offset, b, b + offset])

        return Mesh(verts, triangles, normals)

    @staticmethod
    def cube(size):
        """
        Creates a cube mesh.

        Parameters
        ----------
        size : float
            Side length of cube

        Returns
        -------
        Mesh
            A cube centered at Vector3(0, 0, 0) that has a side length of ``size``

        """
        half = size / 2
        return Mesh(
            [
                Vector3(-1, 1, -1) * half,
                Vector3(1, 1, -1) * half,
                Vector3(1, -1, -1) * half,
                Vector3(-1, -1, -1) * half,
                Vector3(-1, 1, 1) * half,
                Vector3(1, 1, 1) * half,
                Vector3(1, -1, 1) * half,
                Vector3(-1, -1, 1) * half,
                Vector3(-1, -1, -1) * half,
                Vector3(1, -1, -1) * half,
                Vector3(1, -1, 1) * half,
                Vector3(-1, -1, 1) * half,
                Vector3(-1, 1, -1) * half,
                Vector3(1, 1, -1) * half,
                Vector3(1, 1, 1) * half,
                Vector3(-1, 1, 1) * half,
                Vector3(1, 1, -1) * half,
                Vector3(1, 1, 1) * half,
                Vector3(1, -1, 1) * half,
                Vector3(1, -1, -1) * half,
                Vector3(-1, 1, -1) * half,
                Vector3(-1, 1, 1) * half,
                Vector3(-1, -1, 1) * half,
                Vector3(-1, -1, -1) * half,
            ],
            [
                [0, 1, 2],
                [0, 2, 3],
                [4, 6, 5],
                [4, 7, 6],
                [8, 9, 10],
                [8, 10, 11],
                [12, 14, 13],
                [12, 15, 14],
                [16, 17, 18],
                [16, 18, 19],
                [20, 22, 21],
                [20, 23, 22]
            ],
            [Vector3.back()] * 4 +
            [Vector3.forward()] * 4 +
            [Vector3.down()] * 4 +
            [Vector3.up()] * 4 +
            [Vector3.right()] * 4 +
            [Vector3.left()] * 4,
            [[0, 0], [0, 1], [1, 1], [1, 0]] * 6
        )

class Material(Asset):
    """
    Class to hold data on a material.

    Attributes
    ----------
    color : Color
        An albedo tint.
    texture : Texture2D
        A texture to map onto the mesh provided by a MeshRenderer

    """

    def __init__(self, color, texture=None):
        self.color = color
        self.texture = texture

    def GetAssetFile(self, gameObject):
        return Path("Materials") / (gameObject.name + ".mat")

    def SaveAsset(self, ctx):
        if self.texture is not None:
            ctx.project.ImportAsset(self.texture, ctx.gameObject)
        path = ctx.project.path / ctx.filename
        ctx.savers[Material](self, ctx.project, path)

class Color:
    def toString(self):
        return str(self)

    @staticmethod
    def fromString(string):
        if string.startswith("RGB"):
            return RGB(*list(map(int, string[4:-1].split(", "))))
        elif string.startswith("HSV"):
            return HSV(*list(map(int, string[4:-1].split(", "))))

class RGB(Color):
    """
    A class to represent an RGB color.

    Parameters
    ----------
    r : int
        Red value (0-255)
    g : int
        Green value (0-255)
    b : int
        Blue value (0-255)

    """

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __eq__(self, other):
        if not isinstance(other, RGB):
            return False
        return self.r == other.r and self.g == other.g and self.b == other.b

    def __hash__(self):
        return hash(tuple(self))

    def __list__(self):
        return [self.r, self.g, self.b]

    def __iter__(self):
        yield self.r
        yield self.g
        yield self.b

    def __repr__(self):
        return f"RGB({', '.join(map(str, tuple(self)))})"
    def __str__(self):
        return f"RGB({', '.join(map(str, tuple(self)))})"

    def __truediv__(self, other):
        a, b, c = tuple(self)
        return a / other, b / other, c / other

    def __mul__(self, other):
        a, b, c = tuple(self)
        return a * other, b * other, c * other

    def toRGB(self):
        return self

    def toHSV(self):
        return HSV.fromRGB(self.r, self.g, self.b)

    @staticmethod
    def fromHSV(h, s, v):
        r, g, b = colorsys.hsv_to_rgb(h / 360, s / 100, v / 100)
        return RGB(int(r * 255), int(g * 255), int(b * 255))

class HSV(Color):
    """
    A class to represent a HSV color.

    Parameters
    ----------
    h : int
        Hue (0-360)
    s : int
        Saturation (0-100)
    v : int
        Value (0-100)

    """
    def __init__(self, h, s, v):
        self.h = h
        self.s = s
        self.v = v

    def __eq__(self, other):
        if not isinstance(other, HSV):
            return False
        return self.h == other.h and self.s == other.s and self.v == other.v

    def __hash__(self):
        return hash(tuple(self))

    def __list__(self):
        return [self.h, self.s, self.v]

    def __iter__(self):
        yield self.h
        yield self.s
        yield self.v

    def __repr__(self):
        return f"HSV({', '.join(map(str, tuple(self)))})"
    def __str__(self):
        return f"HSV({', '.join(map(str, tuple(self)))})"

    def toRGB(self):
        return RGB.fromHSV(self.h, self.s, self.v)

    def toHSV(self):
        return self

    @staticmethod
    def fromRGB(r, g, b):
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        return HSV(int(h * 360), int(s * 100), int(v * 100))

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
    mesh = ShowInInspector(Mesh, None)
    mat = ShowInInspector(Material, DefaultMaterial, "material")

    def Render(self):
        """Render the mesh that the MeshRenderer has."""
        if self.mesh is None:
            return

        if os.environ["PYUNITY_INTERACTIVE"] == "1":
            self.mesh.compile()
            self.mesh.draw()
