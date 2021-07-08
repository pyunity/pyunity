"""
Core classes of the PyUnity
physics engine.

"""

__all__ = ["PhysicMaterial", "Collider", "SphereCollider",
           "AABBoxCollider", "Rigidbody", "CollManager", "infinity"]

from ..vector3 import *
from ..quaternion import *
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

    def __init__(self, restitution=0.75, friction=1):
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
    """Collider base class."""
    
    attrs = []

    @property
    def pos(self):
        return self.transform.position
    
    @pos.setter
    def pos(self, value):
        self.transform.position = value
    
    @pos.setter
    def rot(self, value):
        self.transform.position = value
    
    @staticmethod
    def supportPoint(a, b, direction):
        return a.supportPoint(direction) - \
            b.supportPoint(direction)

    @staticmethod
    def nextSimplex(args):
        length = len(args[0])
        if length == 2:
            a, b = args[0]
            ab = a - b
            ao = -a
            if ab.dot(ao) > 0:
                args[1] = ab.cross(ao).cross(ab)
            else:
                args[0] = [a]
                args[1] = ao
        if length == 3:
            return Collider.triSimplex(points, direction)
        if length == 4:
            return Collider.tetraSimplex(points, direction)
        return False

    @staticmethod
    def generateManifold(a, b):
        support = Collider.supportPoint(a, b, Vector3.right())
        points = [support]
        direction = -support
        while True:
            support = Collider.supportPoint(a, b, direction)
            if support.dot(direction) <= 0:
                return None
            points.append(support)
            if Collider.nextSimplex(points, direction):
                pass # Need to return manifold

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

    attrs = ["enabled", "radius", "offset"]

    def __init__(self, transform):
        super(SphereCollider, self).__init__(transform)
        self.SetSize(max(abs(self.transform.scale)), Vector3.zero())
    
    @property
    def min(self):
        return self.pos - self.radius
    
    @property
    def max(self):
        return self.pos + self.radius

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
        self.offset = offset

    def collidingWith(self, other):
        if isinstance(other, SphereCollider):
            radii = (self.radius + other.radius) ** 2
            distance = self.pos.get_dist_sqrd(other.pos)
            if distance < radii:
                return Manifold(self, other, other.pos - self.pos,
                    math.sqrt(distance))
        else:
            return Collider.generateManifold(self, other)
    
    def supportPoint(self, direction):
        return self.pos + direction.normalized()


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

    attrs = ["enabled", "pos", "size"]

    def __init__(self, transform):
        super(AABBoxCollider, self).__init__(transform)
        size = self.transform.scale * 2
        self.SetSize(size, Vector3.zero())

    def SetSize(self, size, offset):
        """
        Sets the size of the collider.

        Parameters
        ----------
        min : Vector3
            The corner with the lowest coordinates.
        max : Vector3
            The corner with the highest coordinates.

        """
        self.size = size
        self.offset = offset
    
    @property
    def min(self):
        return self.pos - self.size / 2
    
    @property
    def max(self):
        return self.pos + self.size / 2

    def collidingWith(self, other):
        return Collider.generateManifold(self, other)
    
    def supportPoint(self, direction):
        maxDistance = -infinity
        min, max = self.min, self.max
        for x in (min.x, max.x):
            for y in (min.y, max.y):
                for z in (min.z, max.z):
                    distance = Vector3(x, y, z).dot(direction)
                    if distance > maxDistance:
                        maxDistance = distance
                        maxVertex = Vector3(x, y, z)
        return maxVertex

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

    attrs = ["enabled", "mass", "velocity", "rotVel", "torque", "physicMaterial", "gravity", "force"]

    def __init__(self, transform, dummy=False):
        super(Rigidbody, self).__init__(transform, dummy)
        self.mass = 100
        self.velocity = Vector3.zero()
        self.rotVel = Quaternion.identity()
        self.physicMaterial = PhysicMaterial()
        self.force = Vector3.zero()
        self.torque = Quaternion.identity()
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
        if self.gravity:
            self.force += config.gravity
        self.velocity += self.force * (1 / self.mass)
        # self.velocity *= 0.999
        self.transform.position += self.velocity * dt

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
        self.transform.position += offset

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
        self.dummyRigidbody.mass = infinity
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
                        m = colliderA.collidingWith(colliderB)
                        if m:
                            e = self.GetRestitution(rbA, rbB)
                            normal = m.normal.copy()
                            self.ResolveCollisions(rbA, rbB, e, normal, m.penetration)

    def ResolveCollisions(a, b, restitution, normal, penetration):
        pass

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
