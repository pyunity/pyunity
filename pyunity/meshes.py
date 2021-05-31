"""Module for meshes created at runtime."""

__all__ = ["Mesh"]

from .vector3 import Vector3
from . import render
from OpenGL import GL as gl
from ctypes import c_float, c_ubyte, c_void_p
import itertools

class Mesh:
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
        List of ints containing triangles joining up the vertices.
        Each int is the index of a vertex above.
    normals : list
        List of Vector3's containing the normal of each vertex.
    
    Notes
    -----
    When a mesh is created, you cannot edit any of
    the attributes to update the mesh while a scene
    is running. Instead you will have to instantiate
    a new mesh:

        >>> mesh = Mesh.cube(2)
        >>> mesh2 = Mesh(mesh.verts, mesh.triangles, mesh.normals)

    """

    def __init__(self, verts, triangles, normals):
        self.verts = verts
        self.triangles = triangles
        self.normals = normals

        # self.min, self.max = Vector3.zero(), Vector3.zero()
        # for vert in verts:
        #     if vert.x < self.min.x:
        #         self.min.x = vert.x
        #     if vert.y < self.min.y:
        #         self.min.y = vert.y
        #     if vert.z < self.min.z:
        #         self.min.z = vert.z

        #     if vert.x > self.max.x:
        #         self.max.x = vert.x
        #     if vert.y > self.max.y:
        #         self.max.y = vert.y
        #     if vert.z > self.max.z:
        #         self.max.z = vert.z

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
            A quad centered at Vector3(0, 0) with side length of `size` 
            facing in the direction of the negative z axis.

        """
        return Mesh(
            [
                Vector3(size / 2, size / 2, 0), Vector3(-size / 2, size / 2, 0),
                Vector3(-size / 2, -size / 2,
                        0), Vector3(size / 2, -size / 2, 0)
            ],
            [[0, 1, 2], [0, 2, 3]],
            [Vector3.forward(), Vector3.forward()]
        )

    @staticmethod
    def double_quad(size):
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
            of `size` facing in the direction of the negative z axis.

        """
        return Mesh(
            [
                Vector3(size / 2, size / 2, 0), Vector3(-size / 2, size / 2, 0),
                Vector3(-size / 2, -size / 2,
                        0), Vector3(size / 2, -size / 2, 0)
            ],
            [[0, 1, 2], [0, 2, 3], [0, 2, 1], [0, 3, 2]],
            [Vector3.forward(), Vector3.forward(), Vector3.back(), Vector3.back()]
        )

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
            A cube centered at Vector3(0, 0, 0) that has a side length of `size`

        """
        return Mesh(
            [Vector3(x, y, z) for x in [-size / 2, size / 2]
             for y in [-size / 2, size / 2]
             for z in [-size / 2, size / 2]],
            [
                [0, 1, 2],
                [1, 3, 2],
                [4, 6, 5],
                [5, 6, 7],
                [0, 2, 4],
                [2, 6, 4],
                [1, 5, 3],
                [3, 5, 7],
                [2, 3, 6],
                [3, 7, 6],
                [0, 4, 1],
                [1, 4, 5],
            ],
            [
                Vector3.left(),
                Vector3.left(),
                Vector3.right(),
                Vector3.right(),
                Vector3.back(),
                Vector3.back(),
                Vector3.forward(),
                Vector3.forward(),
                Vector3.up(),
                Vector3.up(),
                Vector3.down(),
                Vector3.down(),
            ]
        )
