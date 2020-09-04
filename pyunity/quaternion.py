import math

class Quaternion:
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self):
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
    
    @property
    def conjugate(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)
    
    @conjugate.setter
    def conjugate(self, value):
        self.w = value[0]
        self.x, self.y, self.z = -value[1], -value[2], -value[3]
    
    @staticmethod
    def FromAxis(angle, axis):
        cos = math.cos(math.radians(angle / 2))
        sin = math.sin(math.radians(angle / 2))
        return Quaternion(cos, axis[0] * sin, axis[1] * sin, axis[2] * sin)
    
    def RotateVector(self, vector):
        return self * Quaternion(0, *vector) * self.conjugate
    
    @property
    def angleAxisPair(self):
        angle = math.degrees(math.acos(self.w)) * 2
        sin = math.sin(math.radians(angle / 2))
        return (angle, self.x / sin, self.y / sin, self.z / sin)
    
    @angleAxisPair.setter
    def angleAxisPair(self, value):
        cos = math.cos(math.radians(angle / 2))
        sin = math.sin(math.radians(angle / 2))
        self.w, self.x, self.y, self.z = cos, axis[0] * sin, axis[1] * sin, axis[2] * sin