## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

__all__ = ["Vector", "Vector2", "Vector3"]

from . import Mathf
from .abc import ABCMeta, abstractmethod, abstractproperty
from .other import LockedLiteral
from collections.abc import Iterable
import operator

def conv(num):
    """Convert float to string and removing decimal place as necessary."""
    if isinstance(num, float) and num.is_integer():
        return str(int(num))
    return str(num)

class Vector(LockedLiteral, metaclass=ABCMeta):
    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(map(conv, self))})"
    def __str__(self):
        return f"{self.__class__.__name__}({', '.join(map(conv, self))})"

    def __getitem__(self, i):
        return list(self)[i]

    @abstractmethod
    def __iter__(self):
        pass

    def __list__(self):
        return list(iter(self))

    def __hash__(self):
        return hash(list(self))

    @abstractmethod
    def __len__(self):
        pass

    def __bool__(self):
        return all(self)

    @abstractmethod
    def _o1(self, f):
        pass

    @abstractmethod
    def _o2(self, other, f):
        pass

    @abstractmethod
    def _o2r(self, other, f):
        pass

    def __add__(self, other):
        return self._o2(other, operator.add)
    def __radd__(self, other):
        return self._o2r(other, operator.add)

    def __sub__(self, other):
        return self._o2(other, operator.sub)
    def __rsub__(self, other):
        return self._o2r(other, operator.sub)

    def __mul__(self, other):
        return self._o2(other, operator.mul)
    def __rmul__(self, other):
        return self._o2r(other, operator.mul)

    def __div__(self, other):
        return self._o2(other, operator.div)
    def __rdiv__(self, other):
        return self._o2r(other, operator.div)

    def __floordiv__(self, other):
        return self._o2(other, operator.floordiv)
    def __rfloordiv__(self, other):
        return self._o2r(other, operator.floordiv)

    def __truediv__(self, other):
        return self._o2(other, operator.truediv)
    def __rtruediv__(self, other):
        return self._o2r(other, operator.truediv)

    def __mod__(self, other):
        return self._o2(other, operator.mod)
    def __rmod__(self, other):
        return self._o2r(other, operator.mod)

    def __lshift__(self, other):
        return self._o2(other, operator.lshift)
    def __rlshift__(self, other):
        return self._o2r(other, operator.lshift)

    def __rshift__(self, other):
        return self._o2(other, operator.rshift)
    def __rrshift__(self, other):
        return self._o2r(other, operator.rshift)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return all(self._o2(other, operator.eq))
    def __ne__(self, other):
        return any(self._o2(other, operator.ne))
    def __gt__(self, other):
        return all(self._o2(other, operator.gt))
    def __lt__(self, other):
        return all(self._o2(other, operator.lt))
    def __ge__(self, other):
        return all(self._o2(other, operator.ge))
    def __le__(self, other):
        return all(self._o2(other, operator.le))

    def __and__(self, other):
        return self._o2(other, operator.and_)
    def __rand__(self, other):
        return self._o2r(other, operator.and_)

    def __or__(self, other):
        return self._o2(other, operator.or_)
    def __ror__(self, other):
        return self._o2r(other, operator.or_)

    def __xor__(self, other):
        return self._o2(other, operator.xor)
    def __rxor__(self, other):
        return self._o2r(other, operator.xor)

    def __neg__(self):
        return self._o1(operator.neg)

    def __pos__(self):
        return self._o1(operator.pos)

    def __abs__(self):
        return self.length

    def abs(self):
        return self._o1(abs)

    def __round__(self, other=None):
        return self._o2(other, round)

    def __invert__(self):
        return self._o1(operator.invert)

    @abstractproperty
    def length(self):
        pass

    @property
    def intTuple(self):
        """Return the x, y and z values of this vector as ints"""
        return tuple(map(int, self))

    @abstractmethod
    def replace(self, num, value):
        pass

class Vector2(Vector):
    def __init__(self, xOrList=None, y=None):
        super(Vector2, self).__init__()
        if xOrList is not None:
            if y is None:
                if hasattr(xOrList, "x") and hasattr(xOrList, "y"):
                    l = [xOrList.x, xOrList.y]
                else:
                    l = xOrList
            else:
                l = [xOrList, y]
        else:
            l = [0, 0]
        l = [x if isinstance(x, (int, float)) else float(x) for x in l]
        self.x, self.y = l
        self._lock()

    def __iter__(self):
        yield self.x
        yield self.y

    def __len__(self):
        return 2

    def _o1(self, f):
        """Unary operator"""
        return Vector2(f(self.x), f(self.y))

    def _o2(self, other, f):
        """Any two-operator operation where the left operand is a Vector2"""
        if isinstance(other, Iterable):
            return Vector2(f(self.x, other[0]), f(self.y, other[1]))
        else:
            return Vector2(f(self.x, other), f(self.y, other))

    def _o2r(self, other, f):
        """Any two-operator operation where the right operand is a Vector2"""
        if isinstance(other, Iterable):
            return Vector2(f(other[0], self.x), f(other[1], self.y))
        else:
            return Vector2(f(other, self.x), f(other, self.y))

    def replace(self, num, value):
        l = list(self)
        l[num] = value
        return Vector2(l)

    def copy(self):
        """Makes a copy of the Vector2"""
        return Vector2(self.x, self.y)

    def getLengthSqrd(self):
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
        """Gets the magnitude of the vector"""
        return Mathf.Sqrt(self.x ** 2 + self.y ** 2)

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

    def getDistance(self, other):
        """
        The distance between this vector and the other vector

        Returns
        -------
        float
            The distance

        """
        return Mathf.Sqrt((self.x - other[0]) ** 2 + (self.y - other[1]) ** 2)

    def getDistSqrd(self, other):
        """
        The distance between this vector and the other vector, squared.
        It is more efficient to call this than to call
        :meth:`Vector2.getDistance` and square it.

        Returns
        -------
        float
            The squared distance

        """
        return (self.x - other[0]) ** 2 + (self.y - other[1]) ** 2

    def clamp(self, min, max):
        """
        Returns a clamped vector between two other vectors,
        resulting in the vector being as close to the
        edge of a bounding box created as possible.

        Parameters
        ----------
        min : Vector2
            Min vector
        max : Vector2
            Max vector

        Returns
        -------
        Vector3
            A vector inside or on the surface of the
            bounding box specified by min and max.

        """
        x = Mathf.Clamp(self.x, min.x, max.x)
        y = Mathf.Clamp(self.y, min.y, max.y)
        return Vector2(x, y)

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
    def min(a, b):
        return a._o2(b, min)

    @staticmethod
    def max(a, b):
        return a._o2(b, max)

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

class Vector3(Vector):
    def __init__(self, xOrList=None, y=None, z=None):
        super(Vector3, self).__init__()
        if xOrList is not None:
            if y is None:
                if hasattr(xOrList, "x") and hasattr(xOrList, "y") and hasattr(xOrList, "z"):
                    l = [xOrList.x, xOrList.y, xOrList.z]
                else:
                    l = xOrList
            else:
                if z is None:
                    raise ValueError("Expected 3 arguments, got 2")
                l = [xOrList, y, z]
        else:
            l = [0, 0, 0]
        l = [x if isinstance(x, (int, float)) else float(x) for x in l]
        self.x, self.y, self.z = l
        self._lock()

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __len__(self):
        return 3

    def _o1(self, f):
        """Unary operator"""
        return Vector3(f(self.x), f(self.y), f(self.z))

    def _o2(self, other, f):
        """Any two-operator operation where the left operand is a Vector3"""
        if isinstance(other, Vector3):
            return Vector3(f(self.x, other.x), f(self.y, other.y), f(self.z, other.z))
        elif isinstance(other, Iterable):
            return Vector3(f(self.x, other[0]), f(self.y, other[1]), f(self.z, other[2]))
        else:
            return Vector3(f(self.x, other), f(self.y, other), f(self.z, other))

    def _o2r(self, other, f):
        """Any two-operator operation where the right operand is a Vector3"""
        if isinstance(other, Iterable):
            return Vector3(f(other[0], self.x), f(other[1], self.y), f(other[2], self.z))
        else:
            return Vector3(f(other, self.x), f(other, self.y), f(other, self.z))

    def replace(self, num, value):
        l = list(self)
        l[num] = value
        return Vector3(l)

    def copy(self):
        """
        Makes a copy of the Vector3

        Returns
        -------
        Vector3
            A shallow copy of the vector

        """
        return Vector3(self.x, self.y, self.z)

    def getLengthSqrd(self):
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
        """Gets the magnitude of the vector"""
        return Mathf.Sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

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

    def getDistance(self, other):
        """
        The distance between this vector and the other vector

        Returns
        -------
        float
            The distance

        """
        return Mathf.Sqrt((self.x - other[0]) ** 2 + (self.y - other[1]) ** 2 + (self.z - other[2]) ** 2)

    def getDistSqrd(self, other):
        """
        The distance between this vector and the other vector, squared.
        It is more efficient to call this than to call
        :meth:`Vector3.getDistance` and square it.

        Returns
        -------
        float
            The squared distance

        """
        return (self.x - other[0]) ** 2 + (self.y - other[1]) ** 2 + (self.z - other[2]) ** 2

    def clamp(self, min, max):
        """
        Returns a clamped vector between two other vectors,
        resulting in the vector being as close to the
        edge of a bounding box created as possible.

        Parameters
        ----------
        min : Vector3
            Min vector
        max : Vector3
            Max vector

        Returns
        -------
        Vector3
            A vector inside or on the surface of the
            bounding box specified by min and max.

        """
        x = Mathf.Clamp(self.x, min.x, max.x)
        y = Mathf.Clamp(self.y, min.y, max.y)
        z = Mathf.Clamp(self.z, min.z, max.z)
        return Vector3(x, y, z)

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
        if isinstance(other, Vector3):
            x = self.y * other.z - self.z * other.y
            y = self.z * other.x - self.x * other.z
            z = self.x * other.y - self.y * other.x
        else:
            x = self.y * other[2] - self.z * other[1]
            y = self.z * other[0] - self.x * other[2]
            z = self.x * other[1] - self.y * other[0]
        return Vector3(x, y, z)

    @staticmethod
    def min(a, b):
        return a._o2(b, min)

    @staticmethod
    def max(a, b):
        return a._o2(b, max)

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
