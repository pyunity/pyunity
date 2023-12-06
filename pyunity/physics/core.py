## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""
Core classes of the PyUnity
physics engine.

"""

__all__ = ["PhysicMaterial", "Collider", "SphereCollider", "Manifold",
           "BoxCollider", "Rigidbody", "Infinity"]

from ..core import Component, ShowInInspector, addFields
from ..errors import PyUnityException
from ..values import ABCMeta, IgnoredMixin, Quaternion, Vector3, abstractmethod
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

    def _setattrException(self, name, value):
        raise PyUnityException(
            "Cannot modify properties of PhysicMaterial: it is immutable")

    def __init__(self, restitution=0.75, friction=1, immutable=False):
        self.restitution = restitution
        self.friction = friction
        self.combine = -1
        if immutable:
            self.__setattr__ = self._setattrException

class Manifold:
    """
    Class to store collision data.

    Parameters
    ----------
    a : Collider
        The first collider
    b : Collider
        The second collider
    point : Vector3
        The collision point
    normal : Vector3
        The collision normal
    penetration : float
        How much the two colliders overlap

    """

    def __init__(self, a, b, point, normal, penetration):
        self.a = a
        self.b = b
        self.point = point
        self.normal = normal
        self.penetration = penetration

    def __str__(self):
        return f"<Manifold point={self.point} normal={self.normal} penetration={self.penetration}>"

class Collider(Component, metaclass=ABCMeta):
    """
    Collider base class.

    Attributes
    ----------
    offset : Vector3
        The offset from the centre of the Collider

    """

    offset = ShowInInspector(Vector3)

    @abstractmethod
    def supportPoint(self, direction):
        pass

    @property
    def pos(self):
        return self.transform.position

    @pos.setter
    def pos(self, value):
        self.transform.position = value

    @property
    def rot(self):
        return self.transform.rotation

    @rot.setter
    def rot(self, value):
        self.transform.rotation = value

class SphereCollider(Collider):
    """
    A spherical collider that cannot be
    deformed.

    Attributes
    ----------
    radius : Vector3
        The radius of the SphereCollider

    """

    radius = ShowInInspector(float, 0)

    def __init__(self):
        super(SphereCollider, self).__init__()
        self.SetSize(max(self.transform.scale.abs()), Vector3.zero())

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

    @property
    def min(self):
        return self.pos - self.radius

    @property
    def max(self):
        return self.pos + self.radius

    def collidingWith(self, other):
        if isinstance(other, SphereCollider):
            radii = (self.radius + other.radius) ** 2
            distance = self.pos.getDistSqrd(other.pos)
            if distance < radii:
                relative = (other.pos - self.pos).normalized()
                dist = self.radius + other.radius - math.sqrt(distance)
                return Manifold(self, other,
                                (self.pos + other.pos) / 2,
                                relative, dist)
        else:
            return CollManager.epa(self, other)

    def supportPoint(self, direction):
        return self.pos + direction.normalized() * self.radius

class BoxCollider(Collider):
    """
    An axis-aligned box collider that
    cannot be deformed.

    Attributes
    ----------
    size : Vector3
        The distance between two farthest
        vertices of the collider

    """

    size = ShowInInspector(Vector3)

    def __init__(self):
        super(BoxCollider, self).__init__()
        self.SetSize(self.transform.scale * 2, Vector3.zero())

    def SetSize(self, size, offset):
        """
        Sets the size of the collider.

        Parameters
        ----------
        size : Vector3
            The dimensions of the collider.
        offset : Vector3
            Offset of the collider.

        """
        self.size = size
        self.offset = offset

    @property
    def min(self):
        return self.pos - self.rot.RotateVector(self.size / 2)

    @property
    def max(self):
        return self.pos + self.rot.RotateVector(self.size / 2)

    def collidingWith(self, other):
        return CollManager.epa(self, other)

    def supportPoint(self, direction):
        def sign(a):
            return -1 if a < 0 else 1
        newdir = self.transform.rotation.conjugate.RotateVector(direction)
        point = newdir._o1(sign) * self.size / 2
        res = self.transform.rotation.RotateVector(point)
        return res + self.transform.position

@addFields(
    mass=ShowInInspector(float, 100),
    inertia=ShowInInspector(float, 200 / 3))
class Rigidbody(Component):
    """
    Class to let a GameObject follow physics
    rules.

    Attributes
    ----------
    velocity : Vector3
        Velocity of the Rigidbody
    rotVel : Vector3
        Rotational velocity of the Rigidbody
    force : Vector3
        Force acting on the Rigidbody. Reset every
        frame.
    torque : Vector3
        Rotational force acting on the Rigidbody.
        Reset every frame.
    physicMaterial : PhysicMaterial
        Physics material of the Rigidbody

    """

    velocity = ShowInInspector(Vector3)
    rotVel = ShowInInspector(Vector3, None, "Rotational Velocity")
    force = ShowInInspector(Vector3)
    torque = ShowInInspector(Vector3)
    gravity = ShowInInspector(bool, True)
    physicMaterial = ShowInInspector(
        PhysicMaterial, PhysicMaterial(immutable=True))

    def __init__(self):
        super(Rigidbody, self).__init__()
        self.mass = 100
        self.velocity = Vector3.zero()
        self.rotVel = Vector3.zero()
        self.force = Vector3.zero()
        self.torque = Vector3.zero()

    @property
    def mass(self):
        """Mass of the Rigidbody. Defaults to 100"""
        if self.invMass == 0:
            return Infinity
        return 1 / self.invMass

    @mass.setter
    def mass(self, val):
        if val == Infinity or val == 0:
            self.invMass = 0
        else:
            self.invMass = 1 / val
        self.inertia = 2 / 3 * self.mass # (1/6 ms^2)

    @property
    def inertia(self):
        if self.invInertia == 0:
            return Infinity
        return 1 / self.invInertia

    @inertia.setter
    def inertia(self, val):
        if val == Infinity or val == 0:
            self.invInertia = 0
        self.invInertia = 1 / val

    @property
    def pos(self):
        return self.transform.position

    @pos.setter
    def pos(self, val):
        self.transform.position = val

    @property
    def rot(self):
        return self.transform.rotation

    @rot.setter
    def rot(self, val):
        self.transform.rotation = val

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
        if self.gravity and self.invMass > 0:
            self.force += config.gravity * self.mass
        self.velocity += self.force * self.invMass * dt
        self.pos += self.velocity * dt

        self.rotVel += self.torque * self.invInertia
        rotation = self.rotVel * dt
        angle = rotation.length
        if angle != 0:
            rotation /= angle
        rotQuat = Quaternion.FromAxis(math.degrees(angle), rotation)
        self.rot *= rotQuat

        self.force = Vector3.zero()
        self.torque = Vector3.zero()

    def MovePos(self, offset):
        """
        Moves the rigidbody and its colliders
        by an offset.

        Parameters
        ----------
        offset : Vector3
            Offset to move

        """
        self.pos += offset

    def AddForce(self, force, point=Vector3.zero()):
        """
        Apply a force to the center of the Rigidbody.

        Parameters
        ----------
        force : Vector3
            Force to apply
        point : Vector3, optional
            Point relative to center of mass in local space
            to apply force at

        Notes
        -----
        A force is a gradual change in velocity, whereas
        an impulse is just a jump in velocity.

        """
        self.force += force
        self.torque += point.cross(force)

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

class SupportPoint(IgnoredMixin):
    def __init__(self, point, original):
        self.point = point
        self.original = original

class Triangle(IgnoredMixin):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        ab = b.point - a.point
        ac = c.point - a.point
        self.normal = (ab).cross(ac).normalized()

class CollManager(IgnoredMixin):
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
        self.dummyRigidbody.mass = Infinity
        self.steps = 1

    @staticmethod
    def supportPoint(a, b, direction):
        supportA = a.supportPoint(direction)
        supportB = b.supportPoint(-direction)
        support = supportA - supportB
        return SupportPoint(support, (supportA, supportB))

    @staticmethod
    def nextSimplex(args):
        length = len(args[0])
        if length == 2:
            return CollManager.lineSimplex(args)
        if length == 3:
            return CollManager.triSimplex(args)
        if length == 4:
            return CollManager.tetraSimplex(args)
        return False

    @staticmethod
    def lineSimplex(args):
        a, b = [x.point for x in args[0]]
        ab = b - a
        ao = -a
        if ab.dot(ao) > 0:
            args[1] = ao - ab / 2
        else:
            args[0] = [args[0][0]]
            args[1] = ao
        return False

    @staticmethod
    def triSimplex(args):
        a, b, c = [x.point for x in args[0]]
        ab = b - a
        ac = c - a
        ao = -a
        abc = ab.cross(ac)
        if abc.cross(ac).dot(ao) > 0:
            if ac.dot(ao) > 0:
                args[0] = [args[0][0], args[0][2]]
                args[1] = ao - ac / 2
            else:
                args[0] = [args[0][0], args[0][1]]
                return CollManager.lineSimplex(args)
        elif ab.cross(abc).dot(ao) > 0:
            args[0] = [args[0][0], args[0][1]]
            return CollManager.lineSimplex(args)
        else:
            if abc.dot(ao) > 0:
                args[1] = abc
            else:
                args[0] = [args[0][0], args[0][2], args[0][1]]
                args[1] = -abc
        return False

    @staticmethod
    def tetraSimplex(args):
        a, b, c, d = [x.point for x in args[0]]
        ab = b - a
        ac = c - a
        ad = d - a
        ao = -a
        abc = ab.cross(ac)
        acd = ac.cross(ad)
        adb = ad.cross(ab)
        if abc.dot(ao) > 0:
            args[0] = [args[0][0], args[0][1], args[0][2]]
            return CollManager.triSimplex(args)
        if acd.dot(ao) > 0:
            args[0] = [args[0][0], args[0][2], args[0][3]]
            return CollManager.triSimplex(args)
        if adb.dot(ao) > 0:
            args[0] = [args[0][0], args[0][3], args[0][1]]
            return CollManager.triSimplex(args)
        return True

    @staticmethod
    def gjk(a, b):
        ab = a.pos - b.pos
        c = Vector3(ab.z, ab.z, -ab.x - ab.y)
        if c == Vector3.zero():
            c = Vector3(-ab.y - ab.z, ab.x, ab.x)

        support = CollManager.supportPoint(a, b, ab.cross(c))
        points = [support]
        direction = -support.point
        maxIter = 50
        i = 0
        while True:
            if i >= maxIter:
                return None
            i += 1
            support = CollManager.supportPoint(a, b, direction)
            if support.point.dot(direction) <= 0:
                return None
            points.insert(0, support)
            args = [points, direction]
            if CollManager.nextSimplex(args):
                return args[0]
            points, direction = args

    @staticmethod
    def epa(a, b):
        # https://blog.winter.dev/2020/epa-algorithm/
        points = CollManager.gjk(a, b)
        if points is None:
            return None
        p0, p1, p2, p3 = points
        triangles = []
        edges = []
        threshold = 1e-8
        limit = 50
        cur = 0

        triangles.append(Triangle(p0, p1, p2))
        triangles.append(Triangle(p0, p2, p3))
        triangles.append(Triangle(p0, p3, p1))
        triangles.append(Triangle(p1, p3, p2))

        while True:
            if cur >= limit:
                return None
            cur += 1

            results = [(t, abs(t.normal.dot(t.a.point))) for t in triangles]
            results.sort(key=lambda x: x[1])
            results = [r for r in results if abs(r[1] - results[0][1]) < 0.001]

            curTriangle = None
            for result, dst in results:
                minSupport = CollManager.supportPoint(a, b, result.normal)
                if result.normal.dot(minSupport.point) - dst < threshold:
                    curTriangle = result

            if curTriangle is not None:
                break

            i = 0
            while i < len(triangles):
                triangle = triangles[i]
                if triangle.normal.dot(minSupport.point - triangle.a.point) > 0:
                    CollManager.AddEdge(edges, triangle.a, triangle.b)
                    CollManager.AddEdge(edges, triangle.b, triangle.c)
                    CollManager.AddEdge(edges, triangle.c, triangle.a)
                    triangles.remove(triangle)
                    continue
                i += 1

            for edge in edges:
                triangles.append(Triangle(minSupport, edge[0], edge[1]))

            edges.clear()

        penetration = curTriangle.normal.dot(curTriangle.a.point)
        u, v, w = CollManager.barycentric(
            curTriangle.normal * penetration,
            curTriangle.a.point,
            curTriangle.b.point,
            curTriangle.c.point)

        if abs(u) > 1 or abs(v) > 1 or abs(w) > 1:
            return None
        elif math.isnan(u + v + w):
            return None

        point = Vector3(
            u * curTriangle.a.original[0] +
            v * curTriangle.b.original[0] +
            w * curTriangle.c.original[0])
        normal = -curTriangle.normal
        return Manifold(a, b, point, normal, penetration)

    @staticmethod
    def AddEdge(edges, a, b):
        if (b, a) in edges:
            edges.remove((b, a))
        else:
            edges.append((a, b))

    @staticmethod
    def barycentric(p, a, b, c):
        v0 = b - a
        v1 = c - a
        v2 = p - a
        d00 = v0.dot(v0)
        d01 = v0.dot(v1)
        d11 = v1.dot(v1)
        d20 = v2.dot(v0)
        d21 = v2.dot(v1)
        denom = d00 * d11 - d01 * d01
        if denom == 0:
            print(p, a, b, c)
        v = (d11 * d20 - d01 * d21) / denom
        w = (d00 * d21 - d01 * d20) / denom
        u = 1 - v - w
        return u, v, w

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
            rb = gameObject.GetComponent(Rigidbody)
            if rb is None:
                dummies.extend(colliders)
                continue
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
        manifolds = {}
        for x, rbA in zip(range(0, len(self.rigidbodies) - 1), list(self.rigidbodies.keys())[:-1]):
            for rbB in list(self.rigidbodies.keys())[x + 1:]:
                for colliderA in self.rigidbodies[rbA]:
                    for colliderB in self.rigidbodies[rbB]:
                        m = colliderA.collidingWith(colliderB)
                        if m is not None:
                            manifolds[rbA, rbB] = m

        for rbA, rbB in manifolds:
            m = manifolds[rbA, rbB]
            e = self.GetRestitution(rbA, rbB)
            self.ResolveCollisions(
                rbA, rbB,
                m.point, e, m.normal, m.penetration)

    def ResolveCollisions(self, a, b, point, restitution, normal, penetration):
        # rv = b.velocity - a.velocity
        # vn = rv.dot(normal)
        # if vn < 0:
        #     return

        if b is self.dummyRigidbody:
            ap = point - a.pos
            vab = a.velocity + a.rotVel.cross(ap)
            top = -(1 + restitution) * vab.dot(normal)
            apCrossN = ap.cross(normal)
            inertiaAcoeff = apCrossN.dot(apCrossN) * a.invInertia
            bottom = a.invMass + inertiaAcoeff
            j = top / bottom
            a.velocity += j * normal * a.invMass
            a.rotVel += (point.cross(j * normal)) * a.invInertia
            return

        ap = point - a.pos
        bp = point - b.pos

        vab = a.velocity + a.rotVel.cross(ap) - b.velocity - b.rotVel.cross(bp)
        apCrossN = ap.cross(normal)
        bpCrossN = bp.cross(normal)
        inertiaAcoeff = apCrossN.dot(apCrossN) * a.invInertia
        inertiaBcoeff = bpCrossN.dot(bpCrossN) * b.invInertia

        top = -(1 + restitution) * vab.dot(normal)
        bottom = a.invMass + b.invMass + inertiaAcoeff + inertiaBcoeff
        j = top / bottom

        a.velocity += j * normal * a.invMass
        b.velocity -= j * normal * b.invMass
        a.rotVel += (ap.cross(j * normal)) * a.invInertia
        b.rotVel -= (bp.cross(j * normal)) * b.invInertia

        # Positional correction

        percent = 0.6
        slop = 0.01
        correction = max(penetration - slop, 0) / (a.invMass + b.invMass) * percent * normal
        a.pos += a.invMass * correction
        b.pos -= b.invMass * correction

    def correctInf(self, a, b, correction, target):
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
                rb.Move(dt)
        self.CheckCollisions()
