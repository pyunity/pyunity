"""
Core classes of the PyUnity
physics engine.

"""

__all__ = ["PhysicMaterial", "Collider", "SphereCollider",
           "AABBoxCollider", "Rigidbody", "CollManager", "Infinity"]

from ..vector3 import *
from ..quaternion import *
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

    def __init__(self, a, b, point, normal, penetration):
        self.a = a
        self.b = b
        self.normal = normal
        self.point = point
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
                relative = (other.pos - self.pos).normalized()
                return Manifold(self, other,
                    [self.pos + relative * self.radius,
                     other.pos - relative * other.radius],
                    relative, math.sqrt(distance))
        else:
            return CollManager.epa(self, other)
    
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
        return self.pos - self.rot.RotateVector(self.size / 2)
    
    @property
    def max(self):
        return self.pos + self.rot.RotateVector(self.size / 2)

    def collidingWith(self, other):
        return CollManager.epa(self, other)
    
    def supportPoint(self, direction):
        maxDistance = -Infinity
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
        self.inertia = 2/3 * self.mass # (1/6 ms^2)
        self.velocity = Vector3.zero()
        self.rotVel = Vector3.zero()
        self.physicMaterial = PhysicMaterial()
        self.force = Vector3.zero()
        self.torque = Vector3.zero()
        self.gravity = True
    
    @property
    def mass(self):
        if self.inv_mass == 0:
            return Infinity
        return 1 / self.inv_mass
    
    @mass.setter
    def mass(self, val):
        if val == Infinity or val == 0:
            self.inv_mass = 0
        self.inv_mass = 1 / val

    @property
    def inertia(self):
        if self.inv_inertia == 0:
            return Infinity
        return 1 / self.inv_inertia
    
    @inertia.setter
    def inertia(self, val):
        if val == Infinity or val == 0:
            self.inv_inertia = 0
        self.inv_inertia = 1 / val

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
        if self.gravity:
            self.force += config.gravity / self.inv_mass
        self.velocity += self.force * self.inv_mass
        self.pos += self.velocity * dt

        self.rotVel += self.torque * self.inv_inertia
        rotation = self.rotVel * dt
        angle = rotation.normalize_return_length()
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
        self.steps = 1
    
    @staticmethod
    def supportPoint(a, b, direction):
        supportA = a.supportPoint(direction)
        supportB = b.supportPoint(-direction)
        support = supportA - supportB
        support.original = [supportA, supportB]
        return support

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
        a, b = args[0]
        ab = b - a
        ao = -a
        if ab.dot(ao) > 0 and a.cross(b) != Vector3.zero():
            args[1] = ab.cross(ao).cross(ab)
        else:
            args[0] = [a]
            args[1] = ao
    
    @staticmethod
    def triSimplex(args):
        a, b, c = args[0]
        ab = b - a
        ac = c - a
        ao = -a
        abc = ab.cross(ac)
        if abc.cross(ac).dot(ao) > 0:
            if ac.dot(ao) > 0 and a.cross(c) != Vector3.zero():
                args[0] = [a, c]
                args[1] = ac.cross(ao).cross(ac)
            else:
                args[0] = [a, b]
                return CollManager.lineSimplex(args)
        elif ab.cross(abc).dot(ao) > 0:
            args[0] = [a, b]
            return CollManager.lineSimplex(args)
        else:
            if abc.dot(ao) > 0:
                args[1] = abc
            else:
                args[0] = [a, c, b]
                args[1] = -abc
        return False
    
    @staticmethod
    def tetraSimplex(args):
        a, b, c, d = args[0]
        ab = b - a
        ac = c - a
        ad = d - a
        ao = -a
        abc = ab.cross(ac)
        acd = ac.cross(ad)
        adb = ad.cross(ab)
        if abc.dot(ao) > 0:
            args[0] = [a, b, c]
            return CollManager.triSimplex(args)
        if acd.dot(ao) > 0:
            args[0] = [a, c, d]
            return CollManager.triSimplex(args)
        if adb.dot(ao) > 0:
            args[0] = [a, d, b]
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
        direction = -support
        while True:
            support = CollManager.supportPoint(a, b, direction)
            if support.dot(direction) <= 0:
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
        faces = [0, 1, 2, 0, 3, 1, 0, 2, 3, 1, 3, 2]
        normals, minFace = CollManager.getFaceNormals(points, faces)
        minDistance = Infinity
        while minDistance == Infinity:
            minNormal = normals[minFace][0]
            minDistance = normals[minFace][1]
            support = CollManager.supportPoint(a, b, minNormal)
            sDistance = minNormal.dot(support)
            if abs(sDistance - minDistance) > 0.001:
                minDistance = Infinity
                uniqueEdges = []
                i = 0
                while i < len(normals):
                    if normals[i][0].dot(support) > 0:
                        f = i * 3
                        CollManager.addIfUniqueEdge(uniqueEdges, faces, f, f + 1)
                        CollManager.addIfUniqueEdge(uniqueEdges, faces, f + 1, f + 2)
                        CollManager.addIfUniqueEdge(uniqueEdges, faces, f + 2, f)
                        faces[f + 2] = faces[-1]; faces.pop()
                        faces[f + 1] = faces[-1]; faces.pop()
                        faces[f] = faces[-1]; faces.pop()
                        normals[i] = normals[-1]; normals.pop()
                        i -= 1
                    i += 1
                newFaces = []
                for edgeIndex1, edgeIndex2 in uniqueEdges:
                    newFaces.append(edgeIndex1)
                    newFaces.append(edgeIndex2)
                    newFaces.append(len(points))
                points.append(support)
                newNormals, newMinFace = CollManager.getFaceNormals(points, newFaces)
                oldMinDistance = Infinity
                for i in range(len(normals)):
                    if normals[i][1] < oldMinDistance:
                        oldMinDistance = normals[i][1]
                        minFace = i
                if newNormals[newMinFace][1] < oldMinDistance:
                    minFace = newMinFace + len(normals)
                faces += newFaces
                normals += newNormals
        minFace *= 3
        u, v, w = CollManager.barycentric(
            minNormal * (minDistance + 0.001),
            points[faces[minFace]],
            points[faces[minFace + 1]],
            points[faces[minFace + 2]])
        point = u * points[faces[minFace]].original[0] + \
            v * points[faces[minFace + 1]].original[0] + \
            w * points[faces[minFace + 2]].original[0]
        return Manifold(a, b, point, minNormal, minDistance + 0.001)
    
    @staticmethod
    def getFaceNormals(points, faces):
        normals = []
        minDistance = -Infinity
        minTriangle = 0
        for i in range(0, len(faces), 3):
            a = points[faces[i]]
            b = points[faces[i + 1]]
            c = points[faces[i + 2]]
            normal = (b - a).cross(c - a).normalized()
            distance = normal.dot(a)
            if distance < 0:
                normal *= -1
                distance *= -1
            normals.append([normal, distance])
            if distance < minDistance:
                minTriangle = i // 3
                minDistance = distance
        return normals, minTriangle
    
    @staticmethod
    def addIfUniqueEdge(edges, faces, a, b):
        if (faces[b], faces[a]) in edges:
            edges.remove((faces[b], faces[a]))
        else:
            edges.append((faces[a], faces[b]))
    
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
            for rbB in list(self.rigidbodies.keys())[x + 1:]:
                for colliderA in self.rigidbodies[rbA]:
                    for colliderB in self.rigidbodies[rbB]:
                        m = CollManager.epa(colliderA, colliderB)
                        if m:
                            e = self.GetRestitution(rbA, rbB)
                            normal = m.normal.copy()
                            self.ResolveCollisions(rbA, rbB, (rbA.pos + rbB.pos) / 2, e, normal, m.penetration)

    def ResolveCollisions(self, a, b, point, restitution, normal, penetration):
        ap = point - a.pos
        bp = point - b.pos

        vab = a.velocity + a.rotVel.cross(ap) - b.velocity - b.rotVel.cross(bp)
        apCrossN = ap.cross(normal)
        bpCrossN = bp.cross(normal)
        inertiaAcoeff = apCrossN.dot(apCrossN) * a.inv_inertia
        inertiaBcoeff = bpCrossN.dot(bpCrossN) * b.inv_inertia

        top = -(1 + restitution) * vab.dot(normal)
        bottom = a.inv_mass + b.inv_mass + inertiaAcoeff + inertiaBcoeff
        j = top / bottom

        print(j)
        a.velocity += j * normal * a.inv_mass
        b.velocity -= j * normal * b.inv_mass
        a.rotVel += (point.cross(j * normal)) * a.inv_inertia
        b.rotVel -= (point.cross(j * normal)) * b.inv_inertia

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
