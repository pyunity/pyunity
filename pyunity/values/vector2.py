"""
A class to represent a 3D point
in space, with a lot of utility
functions.

"""

__all__ = ["Vector2", "clamp"]

import glm
import operator

def clamp(x, _min, _max): return min(_max, max(_min, x))
"""Clamp a value between a minimum and a maximum"""

class Vector2:
    def __init__(self, x_or_list=None, y=None):
        if x_or_list is not None:
            if y is None:
                if hasattr(x_or_list, "x") and hasattr(x_or_list, "y"):
                    self.x = x_or_list.x
                    self.y = x_or_list.y
                else:
                    self.x = x_or_list[0]
                    self.y = x_or_list[1]
            else:
                self.x = x_or_list
                self.y = y
        else:
            self.x = 0
            self.y = 0

    def __repr__(self):
        """String representation of the vector"""
        return "Vector2(%r, %r)" % (self.x, self.y)
    __str__ = __repr__

    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        raise IndexError()

    def __iter__(self):
        yield self.x
        yield self.y

    def __list__(self):
        return [self.x, self.y]

    def __len__(self):
        return 2

    def __bool__(self):
        return self.x != 0 or self.y != 0

    def _o2(self, other, f):
        """Any two-operator operation where the left operand is a Vector2"""
        if hasattr(other, "__getitem__"):
            return Vector2(f(self.x, other[0]), f(self.y, other[1]))
        else:
            return Vector2(f(self.x, other), f(self.y, other))

    def _r_o2(self, other, f):
        """Any two-operator operation where the right operand is a Vector2"""
        if hasattr(other, "__getitem__"):
            return Vector2(f(other[0], self.x), f(other[1], self.y))
        else:
            return Vector2(f(other, self.x), f(other, self.y))

    def _io(self, other, f):
        """Inplace operator"""
        if hasattr(other, "__getitem__"):
            self.x = f(self.x, other[0])
            self.y = f(self.y, other[1])
        else:
            self.x = f(self.x, other)
            self.y = f(self.y, other)
        return self

    def __add__(self, other):
        return self._o2(other, operator.add)
    __radd__ = __add__
    def __iadd__(self, other):
        return self._io(other, operator.add)

    def __sub__(self, other):
        return self._o2(other, operator.sub)
    def rsub(self, other):
        return self._r_o2(other, operator.sub)
    def __isub__(self, other):
        return self._io(other, operator.sub)

    def __mul__(self, other):
        return self._o2(other, operator.mul)
    __rmul__ = __mul__
    def __imul__(self, other):
        return self._io(other, operator.mul)

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
    def __imod__(self, other):
        return self._io(other, operator.mod)

    def __lshift__(self, other):
        return self._o2(other, operator.lshift)
    def __rlshift__(self, other):
        return self._r_o2(other, operator.lshift)
    def __ilshift__(self, other):
        return self._io(other, operator.lshift)

    def __rshift__(self, other):
        return self._o2(other, operator.rshift)
    def __rrshift__(self, other):
        return self._r_o2(other, operator.rshift)
    def __irshift__(self, other):
        return self._io(other, operator.rshift)

    def __eq__(self, other):
        return self._o2(other, operator.eq)
    def __ne__(self, other):
        return self._o2(other, operator.ne)
    def __gt__(self, other):
        return self._o2(other, operator.gt)
    def __lt__(self, other):
        return self._o2(other, operator.lt)
    def __ge__(self, other):
        return self._o2(other, operator.ge)
    def __le__(self, other):
        return self._o2(other, operator.le)

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
        return Vector2(operator.neg(self.x), operator.neg(self.y))

    def __pos__(self):
        return Vector2(operator.pos(self.x), operator.pos(self.y))

    def __abs__(self):
        return Vector2(abs(self.x), abs(self.y))

    def __round__(self, other):
        return self._r_o2(other, round)

    def __invert__(self):
        return Vector2(operator.invert(self.x), operator.invert(self.y))

    def copy(self):
        """
        Makes a copy of the Vector2

        Returns
        -------
        Vector2
            A shallow copy of the vector

        """
        return Vector2(self.x, self.y)

    def get_length_sqrd(self):
        """
        Gets the length of the vector squared. This
        is much faster than finding the length.

        Returns
        -------
        float
            The length of the vector squared

        """
        return self.x ** 2 + self.y ** 2

    @property
    def length(self):
        """Gets or sets the magnitude of the vector"""
        return glm.sqrt(self.x ** 2 + self.y ** 2)

    @length.setter
    def length(self, value):
        length = self.length
        if length != 0:
            self.x *= value / length
            self.y *= value / length

    def normalized(self):
        """
        Get a normalized copy of the vector, or Vector2(0, 0)
        if the length is 0.

        Returns
        -------
        Vector2
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
        return length

    def get_distance(self, other):
        """
        The distance between this vector and the other vector

        Returns
        -------
        float
            The distance

        """
        return glm.sqrt((self.x - other[0]) ** 2 + (self.y - other[1]) ** 2)

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
        return (self.x - other[0]) ** 2 + (self.y - other[1]) ** 2

    @property
    def int_tuple(self):
        """Return the x, y and z values of this vector as ints"""
        return int(self.x), int(self.y)

    @property
    def rounded(self):
        """Return the x, y and z values of this vector rounded to the nearest integer"""
        return round(self.x), round(self.y)

    def clamp(self, min, max):
        """
        Clamps a vector between two other vectors,
        resulting in the vector being as close to the
        edge of a bounding box created as possible.

        Parameters
        ----------
        min : Vector2
            Min vector
        max : Vector2
            Max vector

        """
        self.x = clamp(self.x, min.x, max.x)
        self.y = clamp(self.y, min.y, max.y)

    def dot(self, other):
        """
        Dot product of two vectors.

        Parameters
        ----------
        other : Vector2
            Other vector

        Returns
        -------
        float
            Dot product of the two vectors

        """
        return self.x * other[0] + self.y * other[1]

    def cross(self, other):
        """
        Cross product of two vectors. In 2D this
        is a scalar.

        Parameters
        ----------
        other : Vector2
            Other vector

        Returns
        -------
        float
            Cross product of the two vectors

        """
        z = self.x * other[1] - self.y * other[0]
        return z

    @staticmethod
    def zero():
        """A vector of zero length"""
        return Vector2(0, 0)

    @staticmethod
    def one():
        """A vector of ones"""
        return Vector2(1, 1)

    @staticmethod
    def left():
        """Vector2 pointing in the negative x axis"""
        return Vector2(-1, 0)

    @staticmethod
    def right():
        """Vector2 pointing in the postive x axis"""
        return Vector2(1, 0)

    @staticmethod
    def up():
        """Vector2 pointing in the postive y axis"""
        return Vector2(0, 1)

    @staticmethod
    def down():
        """Vector2 pointing in the negative y axis"""
        return Vector2(0, -1)
