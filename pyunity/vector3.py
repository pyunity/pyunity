"""
A class to store x, y and z values,
with a lot of utility functions.

"""

# TODO: division

import math

clamp = lambda x, _min, _max: min(_max, max(_min, x))
"""Clamp a value between a minimum and a maximum"""

class Vector3:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self):
        """String representation of the vector"""
        return f"Vector3({self.x}, {self.y}, {self.z})"
    __str__ = __repr__
    
    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        elif i == 2:
            return self.z
        raise IndexError()
    
    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z
    
    def __list__(self):
        return [self.x, self.y, self.z]

    def __len__(self):
        return 3

    def __abs__(self):
        return Vector3(abs(self.x), abs(self.y), abs(self.z))
    
    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)
    
    def __eq__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 3:
            return self.x == other[0] and self.y == other[1] and self.z == other[2]
        else:
            return False
            
    def __ne__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 3:
            return self.x != other[0] or self.y != other[1] or self.z != other[2]
        else:
            return True

    def __nonzero__(self):
        return self.x != 0 or self.y != 0 or self.z != 0
    
    def __add__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        elif hasattr(other, "__getitem__"):
            return Vector3(self.x + other[0], self.y + other[1], self.z + other[2])
        else:
            return Vector3(self.x + other, self.y + other, self.z + other)
    __radd__ = __add__
    
    def __iadd__(self, other):
        if isinstance(other, Vector3):
            self.x += other.x
            self.y += other.y
            self.z += other.z
        elif hasattr(other, "__getitem__"):
            self.x += other[0]
            self.y += other[1]
            self.z += other[2]
        else:
            self.x += other
            self.y += other
            self.z += other
        return self
    
    def __sub__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
        elif (hasattr(other, "__getitem__")):
            return Vector3(self.x - other[0], self.y - other[1], self.z - other[2])
        else:
            return Vector3(self.x - other, self.y - other, self.z - other)
    
    def __rsub__(self, other):
        if isinstance(other, Vector3):
            return Vector3(other.x - self.x, other.y - self.y, other.z - self.z)
        if (hasattr(other, "__getitem__")):
            return Vector3(other[0] - self.x, other[1] - self.y, other[2] - self.z)
        else:
            return Vector3(other - self.x, other - self.y, other - self.z)
    
    def __isub__(self, other):
        if isinstance(other, Vector3):
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
        elif (hasattr(other, "__getitem__")):
            self.x -= other[0]
            self.y -= other[1]
            self.z -= other[2]
        else:
            self.x -= other
            self.y -= other
            self.z -= other
        return self
    
    def __mul__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)
        if (hasattr(other, "__getitem__")):
            return Vector3(self.x * other[0], self.y * other[1], self.z * other[2])
        else:
            return Vector3(self.x * other, self.y * other, self.z * other)
    __rmul__ = __mul__
    
    def __imul__(self, other):
        if isinstance(other, Vector3):
            self.x *= other.x
            self.y *= other.y
            self.z *= other.z
        elif (hasattr(other, "__getitem__")):
            self.x *= other[0]
            self.y *= other[1]
            self.z *= other[2]
        else:
            self.x *= other
            self.y *= other
            self.z *= other
        return self
    
    def __div__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x / other.x, self.y / other.y, self.z / other.z)
        if (hasattr(other, "__getitem__")):
            return Vector3(self.x / other[0], self.y / other[1], self.z / other[2])
        else:
            return Vector3(self.x / other, self.y / other, self.z / other)
    
    def __imul__(self, other):
        if isinstance(other, Vector3):
            self.x /= other.x
            self.y /= other.y
            self.z /= other.z
        elif (hasattr(other, "__getitem__")):
            self.x /= other[0]
            self.y /= other[1]
            self.z /= other[2]
        else:
            self.x /= other
            self.y /= other
            self.z /= other
        return self
    
    def copy(self):
        """
        Makes a copy of the Vector3

        Returns
        -------
        Vector3
            A shallow copy of the vector
        
        """
        return Vector3(self.x, self.y, self.z)
    
    def get_length_sqrd(self): 
        """
        Gets the length of the vector squared. This
        is much faster than finding the length.

        Returns
        -------
        float
            The length of the vector squared

        """
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def get_length(self):
        """
        Gets the length of the vector. See `get_length_sqrd`
        for details on optimizing.

        Returns
        -------
        float
            The length of the vector squared
        
        """
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
    
    def __setlength(self, value):
        length = self.get_length()
        self.x *= value / length
        self.y *= value / length
        self.z *= value / length
    
    length = property(get_length, __setlength,
        doc = """Gets or sets the magnitude of the vector""")
    
    def normalized(self):
        """
        Get a normalized copy of the vector, or Vector3(0, 0, 0)
        if the length is 0.
        
        Returns
        -------
        Vector3
            A normalized vector
        
        """
        length = self.length
        if length != 0:
            return 1 / length * self
        return self.copy()
    
    def normalize_return_length(self):
        """
        Normalize the vector and return its length before the normalization
        
        Returns
        -------
        float
            The length before the normalization
        
        """
        length = self.length
        if length != 0:
            self.x /= length
            self.y /= length
            self.z /= length
        return length
    
    def get_distance(self, other):
        """
        The distance between this vector and the other vector
        
        Returns
        -------
        float
            The distance
        
        """
        return math.sqrt((self.x - other[0]) ** 2 + (self.y - other[1]) ** 2 + (self.z - other[2]) ** 2)

    def get_dist_sqrd(self, other):
        """
        The distance between this vector and the other vector, squared.
        It is more efficient to call this than to call `get_distance` and
        square it.
        
        Returns
        -------
        float
            The squared distance
        
        """
        return (self.x - other[0]) ** 2 + (self.y - other[1]) ** 2 + (self.z - other[2]) ** 2
    
    def __get_int_xyz(self):
        return int(self.x), int(self.y), int(self.z)
    
    int_tuple = property(__get_int_xyz, 
        doc="""Return the x, y and z values of this vector as ints""")
    
    def clamp(self, min, max):
        """
        Clamps a vector between two other vectors,
        resulting in the vector being as close to the
        edge of a bounding box created as possible.

        Parameters
        ----------
        min : Vector3
            Min vector
        max : Vector3
            Max vector
        
        """
        self.x = clamp(self.x, min.x, max.x)
        self.y = clamp(self.y, min.y, max.y)
        self.z = clamp(self.z, min.z, max.z)

    def dot(self, other):
        """
        Dot product of two vectors.

        Parameters
        ----------
        other : Vector3
            Other vector

        Returns
        -------
        float
            Dot product of the two vectors
        
        """
        return self.x * other[0] + self.y * other[1] + self.z * other[2]
    
    def cross(self, other):
        """
        Cross product of two vectors

        Parameters
        ----------
        other : Vector3
            Other vector

        Returns
        -------
        Vector3
            Cross product of the two vectors
        
        """
        x = self.y * other[2] - self.z * other[1]
        y = self.z * other[0] - self.x * other[2]
        z = self.x * other[1] - self.y * other[0]
        return Vector3(x, y, z)
    
    @staticmethod
    def zero():
        """A vector of zero length"""
        return Vector3(0, 0, 0)
    
    @staticmethod
    def one():
        """A vector of ones"""
        return Vector3(1, 1, 1)
    
    @staticmethod
    def forward():
        """Vector3 pointing in the positive z axis"""
        return Vector3(0, 0, 1)
    
    @staticmethod
    def back():
        """Vector3 pointing in the negative z axis"""
        return Vector3(0, 0, -1)
    
    @staticmethod
    def left():
        """Vector3 pointing in the negative x axis"""
        return Vector3(-1, 0, 0)
    
    @staticmethod
    def right():
        """Vector3 pointing in the postive x axis"""
        return Vector3(1, 0, 0)
    
    @staticmethod
    def up():
        """Vector3 pointing in the postive y axis"""
        return Vector3(0, 1, 0)
    
    @staticmethod
    def down():
        """Vector3 pointing in the negative y axis"""
        return Vector3(0, -1, 0)