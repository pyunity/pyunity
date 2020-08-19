class Vector3:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return f"<Vector3 x={self.x} y={self.y} z={self.z}>"
    
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