from pyunity import *
import math

def gen_cylinder(detail):
    points = []

    for i in range(detail):
        x, y = math.sin(math.radians(i * 360 / detail)), math.cos(math.radians(i * 360 / detail))
        points.append([x, y])
    points.append([0, 1])

    points2 = []
    indices2 = []
    normals2 = []
    texcoords2 = []
    for i in range(detail):
        j = i + 1
        quad = [
            Vector3(points[i][0], 1, points[i][1]),
            Vector3(points[i][0], -1, points[i][1]),
        ]
        points2.extend(quad)
        normals2.extend([Vector3(points[i][0], 0, points[i][1]), Vector3(points[i][0], 0, points[i][1])])
        indices2.extend([[i * 2, j * 2 + 1, j * 2], [i * 2, i * 2 + 1, j * 2 + 1]])
        texcoords2.extend([[i / detail * 3, 0], [i / detail * 3, 1]])
    points2.extend([Vector3(points[0][0], 1, points[0][1]), Vector3(points[0][0], -1, points[0][1])])
    normals2.extend([Vector3(points[0][0], 0, points[0][1]), Vector3(points[0][0], 0, points[0][1])])
    texcoords2.extend([[3, 0], [3, 1]])

    points3 = []
    indices3 = []
    normals3 = []
    texcoords3 = []
    for i in range(detail):
        index2 = detail * 2 if i == detail - 1 else detail * 2 + i + 1
        points3.append(Vector3(points[i][0], 1, points[i][1]))
        indices3.append([detail * 2 + i + 2, index2 + 2, detail * 4 + 2])
        normals3.append(Vector3(0, 1, 0))
        texcoords3.append([points[i][0] / 2 + 0.5, points[i][1] / 2 + 0.5])

    points4 = []
    indices4 = []
    normals4 = []
    texcoords4 = []
    for i in range(detail):
        index2 = detail * 3 if i == detail - 1 else detail * 3 + i + 1
        points4.append(Vector3(points[i][0], -1, points[i][1]))
        indices4.append([detail * 3 + i + 2, detail * 3 + 1 + 2, index2 + 2])
        normals4.append(Vector3(0, -1, 0))
        texcoords4.append([points[i][0] / 2 + 0.5, points[i][1] / 2 + 0.5])

    points4.append(Vector3(0, 1, 0))
    normals4.append(Vector3(0, 1, 0))
    texcoords4.append([0.5, 0.5])
    points4.append(Vector3(0, -1, 0))
    normals4.append(Vector3(0, -1, 0))
    texcoords4.append([0.5, 0.5])

    final_points = points2 + points3 + points4
    final_indices = indices2 + indices3 + indices4
    final_normals = normals2 + normals3 + normals4
    final_texcoords = texcoords2 + texcoords3 + texcoords4

    return Mesh(final_points, final_indices, final_normals, final_texcoords)

def gen_sphere(detail):
    def texcoord(vec):
        return [math.atan2(vec.x, vec.z) / math.pi, -vec.y / 2 - 0.5]

    t = (1 + math.sqrt(5)) / 2
    points1 = [Vector3(a, b, 0).normalized() for b in (t, -t) for a in (-1, 1)]
    points2 = [Vector3(0, a, b).normalized() for b in (t, -t) for a in (-1, 1)]
    points3 = [Vector3(b, 0, a).normalized() for b in (t, -t) for a in (-1, 1)]
    points = points1 + points2 + points3

    indices = [
        [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
        [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
        [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
        [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1],
    ]

    for i in range(detail):
        indices2 = []
        for tri in indices:
            points.append(((points[tri[0]] + points[tri[1]]) / 2).normalized())
            points.append(((points[tri[1]] + points[tri[2]]) / 2).normalized())
            points.append(((points[tri[2]] + points[tri[0]]) / 2).normalized())
            indices2.append([tri[0], len(points) - 3, len(points) - 1])
            indices2.append([tri[1], len(points) - 2, len(points) - 3])
            indices2.append([tri[2], len(points) - 1, len(points) - 2])
            indices2.append([len(points) - 3, len(points) - 2, len(points) - 1])
        indices = indices2.copy()

    normals = points.copy()
    texcoords = list(map(texcoord, points))
    return Mesh(points, indices, normals, texcoords)

class Rotator(Behaviour):
    def Update(self, dt):
        self.transform.eulerAngles += Vector3(0, 90, 0) * dt

Loader.SaveMesh(gen_cylinder(60), "cylinder")
Loader.SaveObj(gen_cylinder(60), "cylinder")
Loader.SaveMesh(gen_sphere(4), "sphere")
Loader.SaveObj(gen_sphere(4), "sphere")

scene = SceneManager.AddScene("Scene")

# scene.mainCamera.transform.localPosition = Vector3(0, 2.5, -5)
# scene.mainCamera.transform.eulerAngles = Vector3(25, 0, 0)
scene.mainCamera.transform.localPosition = Vector3(0, 0, -7.5)

# mesh = Loader.LoadMesh("cylinder.mesh")
# cylinder = GameObject("Cylinder")
# cylinder.AddComponent(Rotator)
# renderer = cylinder.AddComponent(MeshRenderer)
# renderer.mesh = mesh
# renderer.mat = Material(Color(255, 255, 255), Texture2D("..\\pyunity.png"))
# scene.Add(cylinder)

mesh = Loader.LoadMesh("sphere.mesh")
sphere = GameObject("sphere")
sphere.AddComponent(Rotator)
renderer = sphere.AddComponent(MeshRenderer)
renderer.mesh = mesh
renderer.mat = Material(Color(255, 255, 255), Texture2D("..\\..\\pyunity.png"))
scene.Add(sphere)

SceneManager.LoadScene(scene)
