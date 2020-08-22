from ..vector3 import *
from ..core import *

class IntersectData:
    def __init__(self, collided):
        self.collided = collided

    def __repr__(self):
        return f"<IntersectData collided={self.collided}>"
    __str__ = __repr__

class Collider(Component):
    pass

class SphereCollider(Collider):
    def __init__(self, radius, pos):
        super(SphereCollider, self).__init__()
        self.radius = radius
        self.pos = pos
    
    def collidingWith(self, other):
        if isinstance(other, SphereCollider):
            objDist = abs(self.pos - other.pos).length
            radDist = self.radius + other.radius
            return IntersectData(objDist <= radDist)
        elif isinstance(other, AABBoxCollider):
            inside = (other.min.x < self.pos.x < other.max.x and 
                    other.min.y < self.pos.y < other.max.y and
                    other.min.z < self.pos.z < other.max.z)
            if not inside:
                pos = self.pos.copy()
                pos.clamp(other.min, other.max)
                dist = (self.pos - pos).get_length_sqrd()
                if dist > self.radius ** 2:
                    return IntersectData(False)
            return IntersectData(True)

class AABBoxCollider(Collider):
    def __init__(self, min, max):
        super(SphereCollider, self).__init__()
        self.min = min
        self.max = max
        self.pos = Vector3((min.x + max.x) / 2, (min.y + max.y) / 2, (min.y + max.y) / 2)
    
    def collidingWith(self, other):
        if isinstance(other, AABBoxCollider):
            if self.min.x > other.max.x or self.max.x < other.min.x: collided = False
            elif self.min.y > other.max.y or self.max.y < other.min.y: collided = False
            elif self.min.z > other.max.z or self.max.z < other.min.z: collided = False
            else: collided = True
            return IntersectData(collided)
        elif isinstance(other, SphereCollider):
            inside = (self.min.x < other.pos.x < self.max.x and 
                    self.min.y < other.pos.y < self.max.y and
                    self.min.z < other.pos.z < self.max.z)
            if not inside:
                pos = other.pos.copy()
                pos.clamp(self.min, self.max)
                dist = (other.pos - pos).get_length_sqrd()
                if dist > other.radius ** 2:
                    return IntersectData(False)
            return IntersectData(True)

class CollHandler:
    def __init__(self):
        self.colliders = []
    
    def AddColliders(self, scene):
        for gameObject in scene.gameObjects:
            for component in gameObject.components:
                if isinstance(component, Collider):
                    self.colliders.append(component)

    def CheckCollisions(self):
        for i in range(0, len(self.colliders) - 1):
            for j in range(i + 1, len(self.colliders)):
                a = self.colliders[i]
                b = self.colliders[j]
                if a.collidingWith(b) or b.collidingWith(a):
                    for component in a.gameObject:
                        if a != component and hasattr(component, "OnColliderEnter"):
                            component.OnColliderEnter(b)
                    for component in b.gameObject:
                        if b != component and hasattr(component, "OnColliderEnter"):
                            component.OnColliderEnter(a)