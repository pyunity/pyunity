"""
Module for prebuilt meshes.

"""

from .vector3 import Vector3

class Mesh:
    """
    Class to create a mesh for rendering with a MeshRenderer

    Parameters
    ----------
    verts : list
        List of Vector3's containing each vertex
    triangles : list
        List of ints containing triangles joining up the vertexes.
        Each int is the index of a vertex above.
    normals : list
        List of Vector3's containing the normal of each triangle.
        Unlike Unity, PyUnity uses normals per triangle.

    Attributes
    ----------
    verts : list
        List of Vector3's containing each vertex
    triangles : list
        List of ints containing triangles joining up the vertexes.
        Each int is the index of a vertex above.
    normals : list
        List of Vector3's containing the normal of each triangle.
        Unlike Unity, PyUnity uses normals per triangle.
    
    """

    def __init__(self, verts, triangles, normals):
        self.verts = verts
        self.triangles = triangles
        self.normals = normals
    
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
                Vector3(-size / 2, -size / 2, 0), Vector3(size / 2, -size / 2, 0)
            ],
            [[0, 1, 2], [0, 2, 3]],
            [Vector3(0, 0, -1), Vector3(0, 0, -1)]
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
            [Vector3(x, y, z)   for x in [-size / 2, size / 2] 
                                for y in [-size / 2, size / 2]
                                for z in [-size / 2, size / 2]],
            [
                [0, 2, 1], [1, 2, 3], [4, 5, 6], [5, 7, 6], [0, 4, 2], [2, 4, 6],
                [1, 3, 5], [3, 7, 5], [2, 6, 3], [3, 6, 7], [0, 1, 4], [4, 1, 5],
            ],
            [
                Vector3(-1, 0, 0), Vector3(-1, 0, 0), Vector3(1, 0, 0), Vector3(1, 0, 0),
                Vector3(0, 0, 1), Vector3(0, 0, 1), Vector3(0, 0, -1), Vector3(0, 0, -1),
                Vector3(0, 1, 0), Vector3(0, 1, 0), Vector3(0, -1, 0), Vector3(0, -1, 0),
            ]
        )