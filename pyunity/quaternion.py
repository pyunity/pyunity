import math
from .vector3 import Vector3

class Quaternion:
    """
    Class to represent a 4D Quaternion.

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
        """String representation of the quaternion"""
        return f"Quaternion({self.w}, {self.x}, {self.y}, {self.z})"
    __str__ = __repr__
    
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
        if hasattr(other, "__getitem__") and len(other) == 3:
            return self.w == other[0] and self.x == other[1] and self.y == other[2] and self.z == other[3]
        else:
            return False
            
    def __ne__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 3:
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
        length = math.sqrt(self.w ** 2 + self.x ** 2 + self.y ** 2 + self.z ** 2)
        if length: return Quaternion(self.w / length, self.x / length, self.y / length, self.z / length)
        else: return Quaternion.identity()
    
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
        return self * Quaternion(0, *vector) * self.conjugate
    
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
        cos = math.cos(math.radians(angle / 2))
        sin = math.sin(math.radians(angle / 2))
        return Quaternion(cos, axis[0] * sin, axis[1] * sin, axis[2] * sin)
    
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
        angle = math.degrees(math.acos(self.w)) * 2
        sin = math.sin(math.radians(angle / 2))
        if not sin: sin = math.inf
        return (angle, self.x / sin, self.y / sin, self.z / sin)
    
    @angleAxisPair.setter
    def angleAxisPair(self, value):
        angle, axis = value
        cos = math.cos(math.radians(angle / 2))
        sin = math.sin(math.radians(angle / 2))
        self.w, self.x, self.y, self.z = cos, axis[0] * sin, axis[1] * sin, axis[2] * sin
    
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
        p = -math.asin(-2 * (self.y * self.z + self.w * self.x))
        if math.cos(p) != 0:
            h = -math.atan2(2 * self.x * self.z - 2 * self.w * self.y, 1 - 2 * self.x ** 2 - 2 * self.y ** 2)
            b = -math.atan2(self.x * self.y - self.w * self.z, 1/2 - self.x ** 2 - self.z ** 2)
        else:
            h = -math.atan2(-self.x * self.z - self.w * self.y, 1/2 - self.y ** 2 - self.z ** 2)
            b = 0
        
        return Vector3(math.degrees(p), math.degrees(h), math.degrees(b))
    
    @eulerAngles.setter
    def eulerAngles(self, value):
        a = Quaternion.FromAxis(value.x, Vector3.right())
        b = Quaternion.FromAxis(value.y, Vector3.up())
        c = Quaternion.FromAxis(value.z, Vector3.forward())
        self.w, self.x, self.y, self.z = c * a * b
    
    @staticmethod
    def identity():
        """Identity quaternion representing no rotation"""
        return Quaternion(1, 0, 0, 0)
