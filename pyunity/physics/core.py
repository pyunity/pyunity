"""
Core classes of the PyUnity
physics engine.

"""

from ..vector3 import *
from ..core import *

class Pair:
    """
    Class to store a pair of colliders together.

    Parameters
    ----------
    a : Collider
        The first collider
    b : Collider
        The second collider

    """

    def __init__(self, a, b):
        self.a = a
        self.b = b

class Collider(Component):
    """
    Collider base class. The default
    mass is 100.

    """

    def __init__(self):
        super(Collider, self).__init__()
        self.mass = 100
        self.velocity = Vector3.zero()

class SphereCollider(Collider):
    """
    A spherical collider that cannot be
    deformed.
    
    """

    def __init__(self):
        super(SphereCollider, self).__init__()
    
    def SetSize(self, radius, offset):
        """
        Sets the size of the collider.

        Parameters
        ----------
        radius : float
            The radius of the collider.
        offset : Vector3
            Offset of the collider.
        
        """
        self.radius = radius
        self.pos = offset + self.transform.position
        self.min = pos - radius
        self.max = pos + radius
    
    def Move(self, dt):
        """
        Moves the whole collider by its velocity times
        the delta time.

        Parameters
        ----------
        dt : float
            Delta time to move the velocity by
        
        """
        self.min += dt * self.velocity
        self.max += dt * self.velocity
        self.pos += dt * self.velocity
    
    def collidingWith(self, other):
        """
        Check to see if the collider is
        colliding with another collider.

        Parameters
        ----------
        other : Collider
            Other collider to check against

        Returns
        -------
        Pair or None
            Pair of colliders
        
        Notes
        -----
        To check against another SphereCollider, the
        distance and the sum of the radii is checked.

        To check against an AABBoxColider, the check
        is as follows:

        1.  The sphere's center is checked to see if it
            is inside the AABB.
        #.  If it is, then the two are colliding.
        #.  If it isn't, then a copy of the position is
            clamped to the AABB's bounds.
        #.  Finally, the distance between the clamped
            position and the original position is
            measured.
        #.  If the distance is bigger than the sphere's
            radius, then the two are colliding.
        #.  If not, then they aren't colliding.
        
        """
        if isinstance(other, SphereCollider):
            objDistSqrd = abs(self.pos - other.pos).get_length_sqrd()
            radDistSqrd = (self.radius + other.radius) ** 2
            return Pair(self, other) if objDistSqrd <= radDistSqrd else None
        elif isinstance(other, AABBoxCollider):
            inside = (other.min.x < self.pos.x < other.max.x and 
                    other.min.y < self.pos.y < other.max.y and
                    other.min.z < self.pos.z < other.max.z)
            if not inside:
                pos = self.pos.copy()
                pos.clamp(other.min, other.max)
                dist = (self.pos - pos).get_length_sqrd()
                if dist > self.radius ** 2:
                    return None
            return Pair(self, other)

class AABBoxCollider(Collider):
    """
    An axis-aligned box collider.

    """

    def __init__(self):
        super(AABBoxCollider, self).__init__()
        
    def SetSize(self, min, max):
        """
        Sets the size of the collider.

        Parameters
        ----------
        min : Vector3
            The corner with the lowest coordinates.
        max : Vector3
            The corner with the highest coordinates.
        
        """
        self.min = min
        self.max = max
        self.pos = Vector3((min.x + max.x) / 2, (min.y + max.y) / 2, (min.z + max.z) / 2)
    
    def Move(self, dt):
        """
        Moves the whole collider by its velocity times
        the delta time.

        Parameters
        ----------
        dt : float
            Delta time to move the velocity by
        
        """
        self.min += dt * self.velocity
        self.max += dt * self.velocity
        self.pos += dt * self.velocity
    
    def collidingWith(self, other):
        """
        Check to see if the collider is
        colliding with another collider.

        Parameters
        ----------
        other : Collider
            Other collider to check against

        Returns
        -------
        Pair or None
            Pair of colliders
        
        Notes
        -----
        To check against another AABBoxCollider, the
        corners are checked to see if they are inside
        the other collider.

        To check against a SphereCollider, the check
        is as follows:

        1.  The sphere's center is checked to see if it
            is inside the AABB.
        #.  If it is, then the two are colliding.
        #.  If it isn't, then a copy of the position is
            clamped to the AABB's bounds.
        #.  Finally, the distance between the clamped
            position and the original position is
            measured.
        #.  If the distance is bigger than the sphere's
            radius, then the two are colliding.
        #.  If not, then they aren't colliding.
        
        """
        if isinstance(other, AABBoxCollider):
            if self.min.x > other.max.x or self.max.x < other.min.x: collided = False
            elif self.min.y > other.max.y or self.max.y < other.min.y: collided = False
            elif self.min.z > other.max.z or self.max.z < other.min.z: collided = False
            else: collided = True
            return None if not collided else Pair(self, other)
        elif isinstance(other, SphereCollider):
            inside = (self.min.x < other.pos.x < self.max.x and 
                    self.min.y < other.pos.y < self.max.y and
                    self.min.z < other.pos.z < self.max.z)
            if not inside:
                pos = other.pos.copy()
                pos.clamp(self.min, self.max)
                dist = (other.pos - pos).get_length_sqrd()
                if dist > other.radius ** 2:
                    return None
            return Pair(self, other)

class CollManager:
    """
    Manage the collisions between all colliders.

    """

    def __init__(self):
        self.colliders = []
    
    def AddColliders(self, scene):
        """
        Get all colliders from a specified scene.
        This overwrites the collider list, and so
        can be called whenever a new collider is
        added or removed.

        """
        self.colliders = []
        for gameObject in scene.gameObjects:
            for component in gameObject.components:
                if isinstance(component, Collider):
                    self.colliders.append(component)

    def CheckCollisions(self):
        """
        Goes through every pair exactly once,
        then checks their collisions and
        resolves them.

        """
        for i in range(0, len(self.colliders) - 1):
            for j in range(i + 1, len(self.colliders)):
                a = self.colliders[i]
                b = self.colliders[j]

                m = a.collidingWith(b) or b.collidingWith(a)
                if m:
                    normal = m.a.pos - m.b.pos
                    a = 2 * m.b.mass / (m.a.mass + m.b.mass)
                    b = (m.a.velocity - m.b.velocity).dot(normal) / normal.dot(normal)
                    newVelA = m.a.velocity - a * b * normal
                    
                    normal = m.b.pos - m.a.pos
                    a = 2 * m.a.mass / (m.a.mass + m.b.mass)
                    b = (m.b.velocity - m.a.velocity).dot(normal) / normal.dot(normal)
                    newVelB = m.b.velocity - a * b * normal

                    m.a.velocity = newVelA
                    m.b.velocity = newVelB
    
    def Step(self, dt):
        """
        Steps through the simulation at a
        given delta time.

        Parameters
        ----------
        dt : float
            Delta time to step
        
        Notes
        -----
        The simulation is stepped 10 times,
        so that it is more precise.

        """
        for i in range(10):
            for collider in self.colliders:
                collider.Move(dt / 10)
                collider.transform.position = collider.pos
            self.CheckCollisions()