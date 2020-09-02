"""
Core classes of the PyUnity
physics engine.

"""

from ..vector3 import *
from ..core import *
from . import config
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
    
    Attributes
    ----------
    restitution : float
        Bounciness of the material
    friction : float
        Friction of the material
    combine : int
        Combining function. -1 means
        minimum, 0 means average,
        and 1 means maximum

    """

    def __init__(self, restitution = 0.75, friction = 1):
        self.restitution = restitution
        self.friction = friction
        self.combine = -1

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
    Collider base class.

    """
    
    pass

class SphereCollider(Collider):
    """
    A spherical collider that cannot be
    deformed.

    Attributes
    ----------
    min : Vector3
        The corner with the lowest coordinates.
    max : Vector3
        The corner with the highest coordinates.
    pos : Vector3
        The center of the SphereCollider
    radius : Vector3
        The radius of the SphereCollider
    
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

    def CheckOverlap(self, other):
        """
        Checks to see if the bounding box
        of two colliders overlap.

        Parameters
        ----------
        other : Collider
            Other collider to check against

        Returns
        -------
        bool
            Whether they are overlapping or not
        
        """
        if self.min.x > other.max.x or self.max.x < other.min.x: return False
        elif self.min.y > other.max.y or self.max.y < other.min.y: return False
        elif self.min.z > other.max.z or self.max.z < other.min.z: return False
        else: return True

class AABBoxCollider(Collider):
    """
    An axis-aligned box collider that
    cannot be deformed.

    Attributes
    ----------
    min : Vector3
        The corner with the lowest coordinates.
    max : Vector3
        The corner with the highest coordinates.
    pos : Vector3
        The center of the AABBoxCollider

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

    def CheckOverlap(self, other):
        """
        Checks to see if the bounding box
        of two colliders overlap.

        Parameters
        ----------
        other : Collider
            Other collider to check against

        Returns
        -------
        bool
            Whether they are overlapping or not
        
        """
        if self.min.x > other.max.x or self.max.x < other.min.x: return False
        elif self.min.y > other.max.y or self.max.y < other.min.y: return False
        elif self.min.z > other.max.z or self.max.z < other.min.z: return False
        else: return True

class Rigidbody(Component):
    """
    Class to let a GameObject follow physics
    rules.

    Attributes
    ----------
    mass : int or float
        Mass of the Rigidbody. Defaults
        to 100
    velocity : Vector3
        Velocity of the Rigidbody
    physicMaterial : PhysicMaterial
        Physics material of the Rigidbody
    position : Vector3
        Position of the Rigidbody. It is
        assigned to its GameObject's
        position when the CollHandler is
        created

    """

    def __init__(self):
        super(Rigidbody, self).__init__()
        self.mass = 100
        self.velocity = Vector3.zero()
        self.physicMaterial = PhysicMaterial()
        self.force = Vector3.zero()
        self.gravity = True
    
    def Move(self, dt):
        """
        Moves all colliders on the GameObject by
        the Rigidbody's velocity times the delta
        time.

        Parameters
        ----------
        dt : float
            Time to simulate movement by
        
        """
        if self.gravity: self.force += config.gravity
        self.velocity += self.force * (1 / self.mass) * dt
        self.position += self.velocity * dt
        for component in self.gameObject.components:
            if isinstance(component, Collider):
                component.min += self.velocity * dt
                component.max += self.velocity * dt
                component.pos += self.velocity * dt
        
        self.force = Vector3.zero()
    
    def MovePos(self, offset):
        """
        Moves the rigidbody and its colliders
        by an offset.

        Parameters
        ----------
        offset : Vector3
            Offset to move
        
        """
        self.position += offset
        for component in self.gameObject.components:
            if isinstance(component, Collider):
                component.min += offset
                component.max += offset
                component.pos += offset
    
    def AddForce(self, force):
        self.force += force
    
    def AddImpulse(self, impulse):
        self.velocity += impulse

class CollManager:
    """
    Manages the collisions between all colliders.

    Attributes
    ----------
    rigidbodies : dict
        Dictionary of rigidbodies andthe colliders
        on the gameObject that the Rigidbody belongs
        to
    dummyRigidbody : Rigidbody
        A dummy rigidbody used when a GameObject has
        colliders but no rigidbody. It has infinite
        mass

    """

    def __init__(self):
        self.rigidbodies = {}
        self.dummyRigidbody = Rigidbody()
        self.dummyRigidbody.mass = infinity
    
    def AddPhysicsInfo(self, scene):
        """
        Get all colliders and rigidbodies from a
        specified scene. This overwrites the
        collider and rigidbody lists, and so can
        be called whenever a new collider or
        rigidbody is added or removed.

        Parameters
        ----------
        scene : Scene
            Scene to search for physics info
        
        Notes
        -----
        This function will overwrite the
        pre-existing dictionary of
        rigidbodies. When there are colliders
        but no rigidbody is on the GameObject,
        then they are placed in the dictionary
        with a dummy Rigidbody that has
        infinite mass and a default physic
        material. Thus, they cannot move.

        """
        self.rigidbodies = {}
        dummies = []
        for gameObject in scene.gameObjects:
            if gameObject.GetComponent(Collider):
                colliders = []
                for component in gameObject.components:
                    if isinstance(component, Collider):
                        colliders.append(component)
                
                rb = gameObject.GetComponent(Rigidbody)
                if rb is None: dummies += colliders; continue
                else: rb.position = rb.transform.position
                self.rigidbodies[rb] = colliders
        
        self.rigidbodies[self.dummyRigidbody] = dummies
    
    def GetRestitution(self, a, b):
        """
        Get the restitution needed for
        two rigidbodies, based on their
        combine function

        Parameters
        ----------
        a : Rigidbody
            Rigidbody 1
        b : Rigidbody
            Rigidbody 2

        Returns
        -------
        float
            Restitution
        
        """
        if a.physicMaterial.combine + b.physicMaterial.combine < 0:
            return min(a.physicMaterial.restitution, b.physicMaterial.restitution)
        elif a.physicMaterial.combine + b.physicMaterial.combine > 0:
            return max(a.physicMaterial.restitution, b.physicMaterial.restitution)
        else:
            return (a.physicMaterial.restitution + b.physicMaterial.restitution) / 2

    def CheckCollisions(self):
        """
        Goes through every pair exactly once,
        then checks their collisions and
        resolves them.

        """
        for x, rbA in zip(range(0, len(self.rigidbodies) - 1), list(self.rigidbodies.keys())[:-1]):
            for y, rbB in zip(range(x + 1, len(self.rigidbodies)), list(self.rigidbodies.keys())[x + 1:]):
                for colliderA in self.rigidbodies[rbA]:
                    for colliderB in self.rigidbodies[rbB]:
                        m = colliderA.CheckOverlap(colliderB) and colliderA.collidingWith(colliderB)
                        if m:
                            e = self.GetRestitution(rbA, rbB)

                            normal = m.normal.copy()

                            rv = rbA.velocity - rbB.velocity
                            velAlongNormal = rv.dot(normal)
                            if velAlongNormal < 0: continue
                            b = velAlongNormal / normal.dot(normal)

                            if math.isinf(rbA.mass): a = 0
                            elif math.isinf(rbB.mass): a = 2
                            else: a = (1 + e) * rbB.mass / (rbA.mass + rbB.mass)

                            velA = a * b * normal

                            normal *= -1

                            if math.isinf(rbA.mass): a = 2
                            elif math.isinf(rbB.mass): a = 0
                            else: a = (1 + e) * rbA.mass / (rbA.mass + rbB.mass)
                            
                            velB = a * b * normal

                            rbA.velocity -= velA
                            rbB.velocity -= velB

                            # rv = rbB.velocity - rbA.velocity
                            # t = (rv - rv.dot(m.normal) * m.normal).normalized()

                            # jt = rv.dot(t)
                            # jt /= 1 / rbA.mass + 1 / rbB.mass
                            
                            # if math.isinf(rbA.mass + rbB.mass): j = 0
                            # else:
                            #     j = -(1 + e) * (rbB.velocity - rbA.velocity).dot(normal)
                            #     j /= 1 / rbA.mass + 1 / rbB.mass

                            # mu = (rbA.physicMaterial.friction + rbB.physicMaterial.friction) / 2
                            # if abs(jt) < j * mu:
                            #     frictionImpulse = jt * t
                            # else:
                            #     frictionImpulse = -j * t * mu
                            
                            # rbA.velocity -= 1 / rbA.mass * frictionImpulse
                            # rbB.velocity += 1 / rbB.mass * frictionImpulse

                            correction = m.penetration * (rbA.mass + rbB.mass) * 0.8 * m.normal
                            rbA.MovePos(
                                -1 / rbA.mass * correction if not math.isinf(rbA.mass + rbB.mass) else 0)
                            rbB.MovePos(
                                1 / rbB.mass * correction if not math.isinf(rbA.mass + rbB.mass) else 0)

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
            for rb in self.rigidbodies:
                if rb is not self.dummyRigidbody:
                    rb.Move(dt / 10)
            self.CheckCollisions()
        for rb in self.rigidbodies:
            if rb is not self.dummyRigidbody:
                rb.transform.position = rb.position