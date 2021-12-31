"""
Core classes of the PyUnity
physics engine.
"""

__all__ = ["PhysicMaterial", "Collider", "SphereCollider", "Manifold",
           "AABBoxCollider", "Rigidbody", "CollManager", "Infinity"]

from ..errors import PyUnityException
from ..values import *
from ..core import *
from . import config
import math

Infinity = math.inf
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

    def exception(self, *args, **kwargs):
        raise PyUnityException(
            "Cannot modify properties of PhysicMaterial: it is immutable")

    def __init__(self, restitution=0.75, friction=1, immutable=False):
        self.restitution = restitution
        self.friction = friction
        self.combine = -1
        if immutable:
            self.__setattr__ = self.exception

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

class Collider(Component, metaclass=ABCMeta):
    """Collider base class."""
    
    offset = ShowInInspector(Vector3)
    
    def __init__(self, transform):
        super(Collider, self).__init__(transform)
        self.offset = Vector3.zero()

    @property
    def pos(self):
        return self.transform.position + self.offset
    
    @pos.setter
    def pos(self, value):
        self.transform.position = value - self.offset

    @abstractmethod
    def collidingWith(self, other):
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

    radius = ShowInInspector(float, 0)

    def __init__(self, transform):
        super(SphereCollider, self).__init__(transform)
        self.radius = self.transform.scale.length

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
            otherMin = other.pos - other.size / 2
            otherMax = other.pos + other.size / 2
            inside = (otherMin.x < self.pos.x < otherMax.x and
                      otherMin.y < self.pos.y < otherMax.y and
                      otherMin.z < self.pos.z < otherMax.z)

            pos = self.pos.copy()
            if inside:
                pos.x = otherMin.x if pos.x - otherMin.x < otherMax.x - pos.x else otherMax.x
                pos.y = otherMin.y if pos.y - otherMin.y < otherMax.y - pos.y else otherMax.y
                pos.z = otherMin.z if pos.z - otherMin.z < otherMax.z - pos.z else otherMax.z
            else:
                pos.clamp(otherMin, otherMax)
            dist = (self.pos - pos).get_length_sqrd()
            if not inside and dist > self.radius ** 2:
                return None
            return Manifold(self, other, self.pos - other.pos, self.radius - math.sqrt(dist))

class AABBoxCollider(Collider):
    """
    An axis-aligned box collider that
    cannot be deformed.
    
    Attributes
    ----------
    size : Vector3
        The size of the AABBoxCollider.
    
    """

    size = ShowInInspector(Vector3)

    def __init__(self, transform):
        super(AABBoxCollider, self).__init__(transform)
        self.size = self.transform.scale * 2

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
        selfMin = self.pos - self.size / 2
        selfMax = self.pos + self.size / 2
        if isinstance(other, AABBoxCollider):
            otherMin = other.pos - other.size / 2
            otherMax = other.pos + other.size / 2
            n = other.pos - self.pos

            a_extent = (selfMax.x - selfMin.x) / 2
            b_extent = (otherMax.x - otherMin.x) / 2
            x_overlap = a_extent + b_extent - abs(n.x)
            if x_overlap > 0:
                a_extent = (selfMax.y - selfMin.y) / 2
                b_extent = (otherMax.y - otherMin.y) / 2
                y_overlap = a_extent + b_extent - abs(n.y)
                if y_overlap > 0:
                    a_extent = (selfMax.z - selfMin.z) / 2
                    b_extent = (otherMax.z - otherMin.z) / 2
                    z_overlap = a_extent + b_extent - abs(n.z)
                    if z_overlap > 0:
                        if x_overlap < y_overlap and x_overlap < z_overlap:
                            if n.x < 0:
                                normal = Vector3.left()
                            else:
                                normal = Vector3.right()
                            penetration = x_overlap
                        elif y_overlap < x_overlap and y_overlap < z_overlap:
                            if n.y < 0:
                                normal = Vector3.down()
                            else:
                                normal = Vector3.up()
                            penetration = y_overlap
                        else:
                            if n.z < 0:
                                normal = Vector3.back()
                            else:
                                normal = Vector3.forward()
                            penetration = z_overlap
                        return Manifold(self, other, normal, penetration)

        elif isinstance(other, SphereCollider):
            inside = (selfMin.x < other.pos.x < selfMax.x and
                      selfMin.y < other.pos.y < selfMax.y and
                      selfMin.z < other.pos.z < selfMax.z)

            pos = other.pos.copy()
            if inside:
                pos.x = selfMin.x if pos.x - selfMin.x < selfMax.x - pos.x else selfMax.x
                pos.y = selfMin.y if pos.y - selfMin.y < selfMax.y - pos.y else selfMax.y
                pos.z = selfMin.z if pos.z - selfMin.z < selfMax.z - pos.z else selfMax.z
            else:
                pos.clamp(selfMin, self.max)
            dist = (other.pos - pos).get_length_sqrd()
            if not inside and dist > other.radius ** 2:
                return None
            return Manifold(self, other, self.pos - other.pos, other.radius - dist)

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
    
    """

    mass = ShowInInspector(float, 100)
    velocity = ShowInInspector(Vector3)
    physicMaterial = ShowInInspector(
        PhysicMaterial, PhysicMaterial(immutable=True))
    force = ShowInInspector(Vector3)
    gravity = ShowInInspector(bool, True)

    def __init__(self, transform, dummy=False):
        super(Rigidbody, self).__init__(transform, dummy)
        self.mass = 100
        self.position = Vector3.zero()
        self.velocity = Vector3.zero()
        self.force = Vector3.zero()

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
        if self.gravity:
            self.force += config.gravity
        self.velocity += self.force * (1 / self.mass)
        # self.velocity *= 0.999
        self.transform.position += self.velocity * dt

        self.force = Vector3.zero()

    def AddForce(self, force):
        """
        Apply a force to the center of the Rigidbody.
        Parameters
        ----------
        force : Vector3
            Force to apply
        Notes
        -----
        A force is a gradual change in velocity, whereas
        an impulse is just a jump in velocity.
        """
        self.force += force

    def AddImpulse(self, impulse):
        """
        Apply an impulse to the center of the Rigidbody.
        Parameters
        ----------
        impulse : Vector3
            Impulse to apply
        Notes
        -----
        A force is a gradual change in velocity, whereas
        an impulse is just a jump in velocity.
        """
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
        self.dummyRigidbody = Rigidbody(None, True)
        self.dummyRigidbody.mass = Infinity
        self.steps = 10

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
            colliders = gameObject.GetComponents(Collider)
            if colliders != []:
                rb = gameObject.GetComponent(Rigidbody)
                if rb is None:
                    dummies += colliders
                    continue
                else:
                    rb.position = rb.transform.position
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
                        m = colliderA.collidingWith(colliderB) or \
                            colliderB.collidingWith(colliderA)
                        if m:
                            self.ResolveCollision(m, rbA, rbB)
    
    def ResolveCollision(self, m, rbA, rbB):
        e = self.GetRestitution(rbA, rbB)

        normal = m.normal.copy()

        rv = rbA.velocity - rbB.velocity
        velAlongNormal = rv.dot(normal)
        if velAlongNormal < 0:
            return
        b = velAlongNormal / normal.dot(normal)

        # Infinite mass testing
        if math.isinf(rbA.mass):
            a = 0
        elif math.isinf(rbB.mass):
            a = 1 + e
        else:
            a = (1 + e) * rbB.mass / (rbA.mass + rbB.mass)

        velA = a * b * normal

        # Reverse the normal (normal from B to A)
        normal *= -1

        # Infinite mass testing
        if math.isinf(rbA.mass):
            a = 1 + e
        elif math.isinf(rbB.mass):
            a = 0
        else:
            a = (1 + e) * rbA.mass / (rbA.mass + rbB.mass)

        velB = a * b * normal

        rbA.velocity -= velA
        rbB.velocity -= velB

        # Start friction
        rv = rbB.velocity - rbA.velocity
        t = (rv - rv.dot(m.normal) * m.normal).normalized()

        jt = rv.dot(t)
        jt /= 1 / rbA.mass + 1 / rbB.mass

        if math.isinf(rbA.mass + rbB.mass):
            j = 0
        else:
            j = -(1 + e) * (rbB.velocity -
                            rbA.velocity).dot(normal)
            j /= 1 / rbA.mass + 1 / rbB.mass

        mu = (rbA.physicMaterial.friction +
                rbB.physicMaterial.friction) / 2
        if abs(jt) < j * mu:
            frictionImpulse = jt * t
        else:
            frictionImpulse = -j * t * mu

        rbA.velocity -= 1 / rbA.mass * frictionImpulse
        rbB.velocity += 1 / rbB.mass * frictionImpulse
        # End friction

        correction = m.penetration * \
            (rbA.mass + rbB.mass) * 0.8 * m.normal
        if rbA is not self.dummyRigidbody:
            rbA.transform.position += self.correct_inf(
                rbA.mass, rbB.mass, correction, rbA.mass)
        if rbB is not self.dummyRigidbody:
            rbB.transform.position += self.correct_inf(
                rbA.mass, rbB.mass, correction, rbB.mass)

    def correct_inf(self, a, b, correction, target):
        if not math.isinf(a + b):
            return 1 / target * correction
        else:
            return 0

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
        The simulation is stepped 10 times
        manually by the scene, so it is more
        precise.
        """
        for rb in self.rigidbodies:
            if rb is not self.dummyRigidbody:
                rb.Move(dt / 1)
        self.CheckCollisions()