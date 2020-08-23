"""
Core classes of the PyUnity
physics engine.

"""

from ..vector3 import *
from ..core import *
import math

infinity = math.inf
"""A representation of infinity"""

class PhysicMaterial:
    """
    Class to store data on a collider's material.

    Parameters
    ----------
    restitution : float
        Bounciness of the material
    friction : float
        Friction of the material

    """

    def __init__(self, restitution = 0.75, friction = 1):
        self.restitution = restitution
        self.friction = friction

class Manifold:
    """
    Class to store collision data.

    Parameters
    ----------
    a : Collider
        The first collider
    b : Collider
        The second collider
    normal : Vector3
        The collision normal
    penetration : float
        How much the two colliders overlap

    """

    def __init__(self, a, b, normal, penetration):
        self.a = a
        self.b = b
        self.normal = normal
        self.penetration = penetration

class Collider(Component):
    """
    Collider base class. The default
    mass is 100.

    """

    def __init__(self):
        super(Collider, self).__init__()
        self.mass = 100
        self.velocity = Vector3.zero()
        self.physicMaterial = PhysicMaterial()

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
        Manifold or None
            Collision data
        
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
            normal = self.pos - other.pos
            penetration = radDistSqrd - objDistSqrd
            return Manifold(self, other, normal, penetration) if objDistSqrd <= radDistSqrd else None
        elif isinstance(other, AABBoxCollider):
            inside = (other.min.x < self.pos.x < other.max.x and 
                    other.min.y < self.pos.y < other.max.y and
                    other.min.z < self.pos.z < other.max.z)
            
            pos = self.pos.copy()
            if inside:
                pos.x = other.min.x if pos.x - other.min.x < other.max.x - pos.x else other.max.x
                pos.y = other.min.y if pos.y - other.min.y < other.max.y - pos.y else other.max.y
                pos.z = other.min.z if pos.z - other.min.z < other.max.z - pos.z else other.max.z
            else:
                pos.clamp(other.min, other.max)
            dist = (self.pos - pos).get_length_sqrd()
            if not inside and dist > self.radius ** 2:
                return None
            return Manifold(self, other, self.pos - other.pos, self.radius - dist)

class AABBoxCollider(Collider):
    """
    An axis-aligned box collider that
    cannot be deformed.

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
        Manifold or None
            Collision data
        
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
            n = other.pos - self.pos

            a_extent = (self.max.x - self.min.x) / 2
            b_extent = (other.max.x - other.min.x) / 2
            x_overlap = a_extent + b_extent - abs(n.x)
            if x_overlap > 0:
                a_extent = (self.max.y - self.min.y) / 2
                b_extent = (other.max.y - other.min.y) / 2
                y_overlap = a_extent + b_extent - abs(n.y)
                if y_overlap > 0:
                    a_extent = (self.max.z - self.min.z) / 2
                    b_extent = (other.max.z - other.min.z) / 2
                    z_overlap = a_extent + b_extent - abs(n.z)
                    if z_overlap > 0:
                        if x_overlap < y_overlap and x_overlap < z_overlap:
                            if n.x < 0: normal = Vector3.left()
                            else: normal = Vector3.right()
                            penetration = x_overlap
                        elif y_overlap < x_overlap and y_overlap < z_overlap:
                            if n.y < 0: normal = Vector3.down()
                            else: normal = Vector3.up()
                            penetration = y_overlap
                        else:
                            if n.z < 0: normal = Vector3.back()
                            else: normal = Vector3.forward()
                            penetration = z_overlap
                        return Manifold(self, other, normal, penetration)

            # if self.min.x > other.max.x or self.max.x < other.min.x: collided = False
            # elif self.min.y > other.max.y or self.max.y < other.min.y: collided = False
            # elif self.min.z > other.max.z or self.max.z < other.min.z: collided = False
            # else: collided = True

        elif isinstance(other, SphereCollider):
            inside = (self.min.x < other.pos.x < self.max.x and 
                    self.min.y < other.pos.y < self.max.y and
                    self.min.z < other.pos.z < self.max.z)
            
            pos = other.pos.copy()
            if inside:
                pos.x = self.min.x if pos.x - self.min.x < self.max.x - pos.x else self.max.x
                pos.y = self.min.y if pos.y - self.min.y < self.max.y - pos.y else self.max.y
                pos.z = self.min.z if pos.z - self.min.z < self.max.z - pos.z else self.max.z
            else:
                pos.clamp(self.min, self.max)
            dist = (other.pos - pos).get_length_sqrd()
            if not inside and dist > other.radius ** 2:
                return None
            return Manifold(self, other, self.pos - other.pos, other.radius - dist)

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
                    e = min(m.a.physicMaterial.restitution, m.b.physicMaterial.restitution)

                    normal = m.normal.copy()

                    if math.isinf(m.a.mass): a = 0
                    elif math.isinf(m.b.mass): a = 2
                    else: a =2 * m.b.mass / (m.a.mass + m.b.mass)
                    
                    b = (m.a.velocity - m.b.velocity).dot(normal) / normal.dot(normal)
                    velA = a * b * normal * (0.5 + e / 2)
                    
                    normal *= -1

                    if math.isinf(m.a.mass): a = 2
                    elif math.isinf(m.b.mass): a = 0
                    else: a = 2 * m.a.mass / (m.a.mass + m.b.mass)
                    
                    b = (m.b.velocity - m.a.velocity).dot(normal) / normal.dot(normal)
                    velB = a * b * normal * (0.5 + e / 2)

                    m.a.velocity -= velA
                    m.b.velocity -= velB

                    rv = m.b.velocity - m.a.velocity
                    t = (rv - rv.dot(m.normal) * m.normal).normalized()

                    jt = rv.dot(t)
                    jt /= 1 / m.a.mass + 1 / m.b.mass

                    mu = (m.a.physicMaterial.friction + m.b.physicMaterial.friction) / 2
                    if abs(jt) < j * mu:
                        frictionImpulse = jt * t
                    else:
                        frictionImpulse = -j * t * mu
                    
                    m.a.velocity -= 1 / m.a.mass * frictionImpulse
                    m.b.velocity += 1 / m.b.mass * frictionImpulse
    
                    correction = m.penetration * (m.a.mass + m.b.mass) * 0.8 * m.normal
                    m.a.pos -= 1 / m.a.mass * correction if not math.isinf(m.a.mass + m.b.mass) else 0
                    m.b.pos += 1 / m.b.mass * correction if not math.isinf(m.a.mass + m.b.mass) else 0

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
            self.CheckCollisions()
        for collider in self.colliders:
            collider.transform.position = collider.pos