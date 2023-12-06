## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""Class to represent a rotation in 3D space."""

__all__ = ["Quaternion", "QuaternionDiff"]

from . import Mathf
from .other import LockedLiteral
from .vector import Vector3, conv

class Quaternion(LockedLiteral):
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
        self._lock()

    def __repr__(self):
        return f"Quaternion({', '.join(map(conv, self))})"
    def __str__(self):
        return f"Quaternion({', '.join(map(conv, self))})"

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

    def __hash__(self):
        return hash((self.w, self.x, self.y, self.z))

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
        elif isinstance(other, (int, float)):
            angle, axis = self.angleAxisPair
            return Quaternion.FromAxis((angle * other) % 360, axis)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            angle, axis = self.angleAxisPair
            return Quaternion.FromAxis((angle / other) % 360, axis)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Quaternion):
            diff = (self * other.conjugate).normalized()
            return QuaternionDiff(*diff)

    def absDiff(self, other):
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
        length = Mathf.Sqrt(self.w ** 2 + self.x ** 2 +
                            self.y ** 2 + self.z ** 2)
        if length:
            return Quaternion(self.w / length, self.x / length, self.y / length, self.z / length)
        else:
            return Quaternion.identity()

    @property
    def conjugate(self):
        """The conjugate of a unit quaternion"""
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def RotateVector(self, vector):
        """Rotate a vector by the quaternion"""
        other = Quaternion(0, *vector)
        return Vector3(self * other * self.conjugate)

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
        cos = Mathf.Cos(angle / 2 * Mathf.DEG_TO_RAD)
        sin = Mathf.Sin(angle / 2 * Mathf.DEG_TO_RAD)
        return Quaternion(cos, axis.x * sin, axis.y * sin, axis.z * sin)

    @staticmethod
    def Between(v1, v2):
        a = Quaternion.FromDir(v1).conjugate
        b = Quaternion.FromDir(v2)
        return a * b

    @staticmethod
    def FromDir(v):
        a = Quaternion.FromAxis(
            Mathf.Atan2(v.x, v.z) * Mathf.RAD_TO_DEG,
            Vector3.up())
        b = Quaternion.FromAxis(
            Mathf.Atan2(-v.y, Mathf.Sqrt(v.z ** 2 + v.x ** 2)) * Mathf.RAD_TO_DEG,
            Vector3.right())
        return a * b

    @property
    def angleAxisPair(self):
        """
        Gets the angle and axis pair. Tuple of form (angle, axis).

        """
        angle = 2 * Mathf.Acos(self.w) * Mathf.RAD_TO_DEG
        if angle == 0:
            return (0, Vector3.up())
        return (angle, Vector3(self).normalized())

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
        return b * a * c

    @property
    def eulerAngles(self):
        """Gets the Euler angles of the quaternion"""
        s = self.w ** 2 + self.x ** 2 + self.y ** 2 + self.z ** 2
        r23 = 2 * (self.w * self.x - self.y * self.z)
        if r23 > 0.999999 * s:
            x = Mathf.PI / 2
            y = 2 * Mathf.Atan2(self.y, self.x)
            z = 0
        elif r23 < -0.999999 * s:
            x = -Mathf.PI / 2
            y = -2 * Mathf.Atan2(self.y, self.x)
            z = 0
        else:
            x = Mathf.Asin(r23)
            r13 = 2 * (self.w * self.y + self.z * self.x) / s
            r33 = 1 - 2 * (self.x ** 2 + self.y ** 2) / s
            r21 = 2 * (self.w * self.z + self.x * self.y) / s
            r22 = 1 - 2 * (self.x ** 2 + self.z ** 2) / s
            y = Mathf.Atan2(r13, r33)
            z = Mathf.Atan2(r21, r22)

        euler = [x, y, z]
        for i in range(3):
            euler[i] = (euler[i] * Mathf.RAD_TO_DEG + 180) % 360 - 180
        return Vector3(euler)

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
        return abs(2 * Mathf.Acos(self.w) * Mathf.DEG_TO_RAD)
