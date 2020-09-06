"""
A class to store x, y and z values,
with a lot of utility functions.

"""

# print(*[[x, y, z] for x in [-1, 1] for y in [-1, 1] for z in [-1, 1]], sep="\n")

# TODO: division

import math, operator

clamp = lambda x, _min, _max: min(_max, max(_min, x))
"""Clamp a value between a minimum and a maximum"""

class Vector3:

    def __init__(self, x_or_list = None, y = None, z = None):
        if x_or_list != None:
            if y == None:
                if hasattr(x_or_list, "x") and hasattr(x_or_list, "y") and hasattr(x_or_list, "z"):
                    self.x = x_or_list.x
                    self.y = x_or_list.y
                    self.z = x_or_list.z
                else:
                    self.x = x_or_list[0]
                    self.y = x_or_list[1]
                    self.z = x_or_list[2]
            else:
                self.x = x_or_list
                self.y = y
                self.z = z
        else:
            self.x = 0
            self.y = 0
            self.z = 0
    
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
    
    def _o2(self, other, f):
        """Any two-operator operation where the left operand is a Vector3"""
        if isinstance(other, Vector3):
            return Vector3(f(self.x, other.x), f(self.y, other.y), f(self.z, other.z))
        elif hasattr(other, "__getitem__"):
            return Vector3(f(self.x, other[0]), f(self.y, other[1]), f(self.z, other[2]))
        else:
            return Vector3(f(self.x, other), f(self.y, other), f(self.z, other))
    
    def _r_o2(self, other, f):
        """Any two-operator operation where the right operand is a Vector3"""
        if hasattr(other, "__getitem__"):
            return Vector3(f(other[0], self.x), f(other[1], self.y), f(other[2], self.z))
        else:
            return Vector3(f(other, self.x), f(other, self.y), f(other, self.z))
    
    def _io(self, other, f):
        """Inplace operator"""
        if hasattr(other, "__getitem__"):
            self.x = f(self.x, other[0])
            self.y = f(self.y, other[1])
            self.z = f(self.z, other[2])
        else:
            self.x = f(self.x, other)
            self.y = f(self.y, other)
            self.z = f(self.z, other)
        return self
    
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
    
    def __div__(self, other):
        return self._o2(other, operator.div)
    def __rdiv__(self, other):
        return self._r_o2(other, operator.div)
    def __idiv__(self, other):
        return self._io(other, operator.div)

    def __floordiv__(self, other):
        return self._o2(other, operator.floordiv)
    def __rfloordiv__(self, other):
        return self._r_o2(other, operator.floordiv)
    def __ifloordiv__(self, other):
        return self._io(other, operator.floordiv)

    def __truediv__(self, other):
        return self._o2(other, operator.truediv)
    def __rtruediv__(self, other):
        return self._r_o2(other, operator.truediv)
    def __itruediv__(self, other):
        return self._io(other, operator.truediv)
    
    def __mod__(self, other):
        return self._o2(other, operator.mod)
    def __rmod__(self, other):
        return self._r_o2(other, operator.mod)

    def __divmod__(self, other):
        return self._o2(other, divmod)
    def __rdivmod__(self, other):
        return self._r_o2(other, divmod)
    
    def __pow__(self, other):
        return self._o2(other, operator.pow)
    def __rpow__(self, other):
        return self._r_o2(other, operator.pow)
    
    def __lshift__(self, other):
        return self._o2(other, operator.lshift)
    def __rlshift__(self, other):
        return self._r_o2(other, operator.lshift)

    def __rshift__(self, other):
        return self._o2(other, operator.rshift)
    def __rrshift__(self, other):
        return self._r_o2(other, operator.rshift)
    
    def __and__(self, other):
        return self._o2(other, operator.and_)
    __rand__ = __and__
    
    def __or__(self, other):
        return self._o2(other, operator.or_)
    __ror__ = __or__

    def __xor__(self, other):
        return self._o2(other, operator.xor)
    __rxor__ = __xor__
    
    def __neg__(self):
        return Vector3(operator.neg(self.x), operator.neg(self.y), operator.neg(self.z))

    def __pos__(self):
        return Vector3(operator.pos(self.x), operator.pos(self.y), operator.pos(self.y))

    def __abs__(self):
        return Vector3(abs(self.x), abs(self.y), abs(self.z))

    def __invert__(self):
        return Vec2d(-self.x, -self.y, -self.z)
    
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

    @property
    def length(self):
        """Gets or sets the magnitude of the vector"""
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
    
    @length.setter
    def length(self, value):
        length = self.get_length()
        self.x *= value / length
        self.y *= value / length
        self.z *= value / length
    
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
    
    @property
    def int_tuple(self):
        """Return the x, y and z values of this vector as ints"""
        return int(self.x), int(self.y), int(self.z)
    
    @property
    def rounded(self):
        """Return the x, y and z values of this vector rounded to the nearest integer"""
        return round(self.x), round(self.y), round(self.z)
    
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