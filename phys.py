from pyunity import *

from pyunity.physics.core import CollManager
a = GameObject("A").AddComponent(BoxCollider)
b = GameObject("B").AddComponent(BoxCollider)
b.pos = Vector3(2.0, 0, 0)

points = CollManager.gjk(a, b)
print(points)

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

distances = []
normals = []
for i in range(4):
    perm = points.copy()
    perm.pop(i)

    normal = (perm[1] - perm[0]).cross(perm[2] - perm[0]).normalized()
    dist = normal.dot(-perm[0])
    normals.append(normal)
    distances.append((i, dist))

distances.sort(key=lambda x: x[1], reverse=True)
print(distances)
idx, dist = distances[0]

triangle = points.copy()
triangle.pop(idx)
if dist != 0:
    point = triangle[0] + dist * normals[idx]
else:
    point = Vector3(0, 0, 0)
print([triangle[0].original[0], triangle[1].original[0], triangle[2].original[0]])
print(point, normals[idx])

u, v, w = barycentric(point, *triangle)
print(u, v, w)
print(
    u * triangle[0].original[0] + \
    v * triangle[1].original[0] + \
    w * triangle[2].original[0]
)

# m = CollManager.epa(a, b)
# if m is not None:
#     print(m.point)
#     print(m.normal)
#     print(m.penetration)
