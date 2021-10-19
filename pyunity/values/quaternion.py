"""Class to represent a rotation in 3D space."""

__all__ = ["Quaternion", "QuaternionDiff"]

import glm
from .vector import Vector3

class Quaternion:
    """
    Class to represent a unit quaternion, also known as a versor.

    Parameters
    ----------
    w : float
        Real value of Quaternion
    x : float
        x coordinate of Quaternion
    y : float
        y coordinate of Quaternion
    z : float
        z coordinate of Quaternion

    """
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "Quaternion(%r, %r, %r, %r)" % (self.w, self.x, self.y, self.z)
    def __str__(self):
        return "Quaternion(%r, %r, %r, %r)" % (self.w, self.x, self.y, self.z)

    def __getitem__(self, i):
        if i == 0:
            return self.w
        elif i == 1:
            return self.x
        elif i == 2:
            return self.y
        elif i == 3:
            return self.z
        raise IndexError()

    def __iter__(self):
        yield self.w
        yield self.x
        yield self.y
        yield self.z

    def __list__(self):
        return [self.w, self.x, self.y, self.z]

    def __len__(self):
        return 4

    def __eq__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 4:
            return self.w == other[0] and self.x == other[1] and self.y == other[2] and self.z == other[3]
        else:
            return False

    def __ne__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 4:
            return self.w != other[0] or self.x != other[1] or self.y != other[2] or self.z != other[3]
        else:
            return True

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
            x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
            y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
            z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
            return Quaternion(w, x, y, z)

    def __sub__(self, other):
        if isinstance(other, Quaternion):
            return QuaternionDiff(*(self * other.conjugate))

    def abs_diff(self, other):
        return abs(other - self)

    def copy(self):
        """
        Deep copy of the Quaternion.

        Returns
        -------
        Quaternion
            A deep copy

        """
        return Quaternion(self.w, self.x, self.y, self.z)

    def normalized(self):
        """
        A normalized Quaternion, for rotations.
        If the length is 0, then the identity
        quaternion is returned.

        Returns
        -------
        Quaternion
            A unit quaternion
        """
        length = glm.sqrt(self.w ** 2 + self.x ** 2 +
                          self.y ** 2 + self.z ** 2)
        if length:
            return Quaternion(self.w / length, self.x / length, self.y / length, self.z / length)
        else:
            return Quaternion.identity()

    @property
    def conjugate(self):
        """The conjugate of a unit quaternion"""
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    @conjugate.setter
    def conjugate(self, value):
        self.w = value[0]
        self.x, self.y, self.z = -value[1], -value[2], -value[3]

    def RotateVector(self, vector):
        """Rotate a vector by the quaternion"""
        t = (2 * Vector3(self)).cross(vector)
        return vector + self.w * t + Vector3(self).cross(t)

    @staticmethod
    def FromAxis(angle, a):
        """
        Create a quaternion from an angle and an axis.

        Parameters
        ----------
        angle : float
            Angle to rotate
        a : Vector3
            Axis to rotate about

        """
        axis = a.normalized()
        cos = glm.cos(glm.radians(angle / 2))
        sin = glm.sin(glm.radians(angle / 2))
        return Quaternion(cos, axis[0] * sin, axis[1] * sin, axis[2] * sin)

    @staticmethod
    def Between(v1, v2):
        a = v1.cross(v2)
        if a.dot(a) == 0:
            if v1 == v2 or v1.dot(v1) == 0 or v2.dot(v2) == 0:
                return Quaternion.identity()
            else:
                return Quaternion.FromAxis(180, Vector3.up())
        angle = glm.acos(v1.dot(v2) / (glm.sqrt(v1.length * v2.length)))
        q = Quaternion.FromAxis(glm.degrees(angle), a)
        return q.normalized()

    @staticmethod
    def FromDir(v):
        a = Quaternion.FromAxis(glm.degrees(glm.atan(v.x, v.z)), Vector3.up())
        b = Quaternion.FromAxis(
            glm.degrees(glm.atan(-v.y, glm.sqrt(v.z ** 2 + v.x ** 2))),
            Vector3.right())
        return a * b

    @property
    def angleAxisPair(self):
        """
        Gets or sets the angle and axis pair.

        Notes
        -----
        When getting, it returns a tuple in the
        form of ``(angle, x, y, z)``. When setting,
        assign like ``q.eulerAngles = (angle, vector)``.

        """
        angle = 2 * glm.degrees(glm.acos(self.w))
        if angle == 0:
            return (0, 0, 1, 0)
        magnitude = glm.sin(2 * glm.acos(self.w / 2))
        return (angle, self.x / magnitude, self.y / magnitude, self.z / magnitude)

    @angleAxisPair.setter
    def angleAxisPair(self, value):
        angle, axis = value
        cos = glm.cos(glm.radians(angle / 2))
        sin = glm.sin(glm.radians(angle / 2))
        self.w, self.x, self.y, self.z = cos, axis[0] * \
            sin, axis[1] * sin, axis[2] * sin

    @staticmethod
    def Euler(vector):
        """
        Create a quaternion using Euler rotations.

        Parameters
        ----------
        vector : Vector3
            Euler rotations

        Returns
        -------
        Quaternion
            Generated quaternion

        """
        a = Quaternion.FromAxis(vector.x, Vector3.right())
        b = Quaternion.FromAxis(vector.y, Vector3.up())
        c = Quaternion.FromAxis(vector.z, Vector3.forward())
        return c * a * b

    @property
    def eulerAngles(self):
        """Gets or sets the Euler Angles of the quaternion"""
        sx = 2 * (self.w * self.x + self.y * self.z)
        x = glm.degrees(glm.asin(sx))
        if abs(x - 90) > 0.001:
            sz = 2 * (self.w * self.z - self.y * self.x)
            cz = 1 - 2 * (self.x ** 2 + self.z ** 2)
            z = glm.degrees(glm.atan(sz, cz))
            sy = 2 * (self.w * self.y - self.x * self.z)
            cy = 1 - 2 * (self.y ** 2 + self.x ** 2)
            y = glm.degrees(glm.atan(sy, cy))
        else:
            y = 0
            z = glm.degrees(glm.atan(self.y, self.w))
        return Vector3(x, y, z)

    @eulerAngles.setter
    def eulerAngles(self, value):
        self.w, self.x, self.y, self.z = Quaternion.Euler(value)
    
    def SetBackward(self, value):
        a = Quaternion.FromAxis(value.x, Vector3.right())
        b = Quaternion.FromAxis(value.y, Vector3.up())
        c = Quaternion.FromAxis(value.z, Vector3.forward())
        self.w, self.x, self.y, self.z = b * a * c

    @staticmethod
    def identity():
        """Identity quaternion representing no rotation"""
        return Quaternion(1, 0, 0, 0)

class QuaternionDiff:
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def __abs__(self):
        return abs(2 * glm.degrees(glm.acos(self.w)))
