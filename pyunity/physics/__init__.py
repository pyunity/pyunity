from vector3 import *

class IntersectData:
    def __init__(self, collided, penetration):
        self.collided = collided
        self.penetration = penetration

    def __repr__(self):
        return f"<IntersectData collided={self.collided} penetration={self.penetration}>"
    __str__ = __repr__

class Collider:
    pass

class SphereCollider(Collider):
    def __init__(self, radius, position):
        self.radius = radius
        self.position = position
    
    def collidingWith(self, other):
        if isinstance(other, SphereCollider):
            objDist = abs(self.position - other.position).length
            radDist = self.radius + other.radius
            return IntersectData(objDist <= radDist, radDist - objDist)

a = SphereCollider(2, Vector3(1, 1, 0))
b = SphereCollider(2, Vector3(0, 0, 0))
print(a.collidingWith(b))