from pyunity import *
# from pyunity import config
# config.faceCulling = False
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

    points = []
    indices = []
    texcoords = []
    for i in range(detail // 2 + 1):
        sin1 = math.sin(i / detail * math.pi * 2)
        cos1 = math.cos(i / detail * math.pi * 2)
        for j in range(detail):
            base = i * (detail + 1) + j
            base2 = (i + 1) * (detail + 1) + j
            sin2 = math.sin(j / detail * math.pi * 2)
            cos2 = math.cos(j / detail * math.pi * 2)
            points.append(Vector3(sin2 * cos1, cos2, sin1 * sin2))
            texcoords.append([i / detail * 2, -cos2 / 2 + 0.5])
            if j > detail // 2:
                indices.append([base, base + 1, base2 + 1])
                indices.append([base, base2 + 1, base2])
            else:
                indices.append([base, base2 + 1, base + 1])
                indices.append([base, base2, base2 + 1])
        points.append(Vector3(0, 1, 0))
        texcoords.append([i / detail * 2, 1])
    del indices[-2 * detail:]

    normals = points.copy()
    # texcoords = list(map(texcoord, points))
    return Mesh(points, indices, normals, texcoords)

class Rotator(Behaviour):
    def Update(self, dt):
        self.transform.eulerAngles += Vector3(0, 90, 0) * dt

Loader.SaveMesh(gen_cylinder(60), "cylinder")
Loader.SaveObj(gen_cylinder(60), "cylinder")
Loader.SaveMesh(gen_sphere(20), "sphere")
Loader.SaveObj(gen_sphere(20), "sphere")

scene = SceneManager.AddScene("Scene")

# scene.mainCamera.transform.localPosition = Vector3(0, 2.5, -5)
# scene.mainCamera.transform.eulerAngles = Vector3(25, 0, 0)
scene.mainCamera.transform.localPosition = Vector3(0, 0, -7.5)

# mesh = Loader.LoadMesh("cylinder.mesh")
# cylinder = GameObject("Cylinder")
# cylinder.AddComponent(Rotator)
# renderer = cylinder.AddComponent(MeshRenderer)
# renderer.mesh = mesh
# renderer.mat = Material(Color(255, 255, 255), Texture2D("..\\..\\pyunity.png"))
# scene.Add(cylinder)

mesh = Loader.LoadMesh("sphere.mesh")
sphere = GameObject("sphere")
sphere.AddComponent(Rotator)
renderer = sphere.AddComponent(MeshRenderer)
renderer.mesh = mesh
renderer.mat = Material(Color(255, 255, 255), Texture2D("..\\..\\pyunity.png"))
scene.Add(sphere)

SceneManager.LoadScene(scene)
