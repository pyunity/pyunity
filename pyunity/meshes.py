"""Module for meshes created at runtime."""

__all__ = ["Mesh"]

from .vector3 import Vector3
from . import render
from .scenes import SceneManager

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
    texcoords : list
        List of lists containing the texture coordinate of each vertex.

    Notes
    -----
    When a mesh is created, you cannot edit any of
    the attributes to update the mesh while a scene
    is running. Instead you will have to instantiate
    a new mesh:

        >>> mesh = Mesh.cube(2)
        >>> mesh2 = Mesh(mesh.verts, mesh.triangles, mesh.normals, mesh.texcoords)
        >>> # Or this:
        >>> mesh2 = mesh.copy()

    """

    def __init__(self, verts, triangles, normals, texcoords=None):
        self.verts = verts
        self.triangles = triangles
        self.normals = normals
        if texcoords is not None:
            self.texcoords = texcoords
        else:
            self.texcoords = [[0, 0] for _ in range(len(self.verts))]

        if SceneManager.CurrentScene() is not None:
            self.vbo, self.ibo = render.gen_buffers(self)
            self.ibo = render.gen_array()

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
    
    def copy(self):
        """
        Create a copy of the current Mesh.

        Returns
        -------
        Mesh
            Copy of the mesh
        """
        return Mesh(self.verts, self.triangles, self.normals, self.texcoords)

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
            A quad centered at Vector3(0, 0) with side length of ``size`` 
            facing in the direction of the negative z axis.

        """
        return Mesh(
            [
                Vector3(size / 2, size / 2, 0), Vector3(-size / 2, size / 2, 0),
                Vector3(-size / 2, -size / 2,
                        0), Vector3(size / 2, -size / 2, 0)
            ],
            [[0, 1, 2], [0, 2, 3]],
            [Vector3.forward(), Vector3.forward(),
             Vector3.forward(), Vector3.forward()],
            [[0, 0], [0, 1], [1, 1], [1, 0]]
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
            of ``size``.

        """
        return Mesh(
            [
                Vector3(size / 2, size / 2, 0), Vector3(-size / 2, size / 2, 0),
                Vector3(-size / 2, -size / 2,
                        0), Vector3(size / 2, -size / 2, 0),
                Vector3(size / 2, size / 2, 0), Vector3(-size / 2, size / 2, 0),
                Vector3(-size / 2, -size / 2,
                        0), Vector3(size / 2, -size / 2, 0),
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
        return Mesh(
            [
                Vector3(-1, 1, -1),
                Vector3(1, 1, -1),
                Vector3(1, -1, -1),
                Vector3(-1, -1, -1),
                Vector3(-1, 1, 1),
                Vector3(1, 1, 1),
                Vector3(1, -1, 1),
                Vector3(-1, -1, 1),
                Vector3(-1, -1, -1),
                Vector3(1, -1, -1),
                Vector3(1, -1, 1),
                Vector3(-1, -1, 1),
                Vector3(-1, 1, -1),
                Vector3(1, 1, -1),
                Vector3(1, 1, 1),
                Vector3(-1, 1, 1),
                Vector3(1, 1, -1),
                Vector3(1, 1, 1),
                Vector3(1, -1, 1),
                Vector3(1, -1, -1),
                Vector3(-1, 1, -1),
                Vector3(-1, 1, 1),
                Vector3(-1, -1, 1),
                Vector3(-1, -1, -1),
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
