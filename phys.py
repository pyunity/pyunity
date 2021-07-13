from pyunity import *
from pyunity.physics.core import CollManager

a = GameObject("a").AddComponent(AABBoxCollider)
b = GameObject("b").AddComponent(AABBoxCollider)
b.pos = Vector3(2, 0, 0)
m = CollManager.epa(a, b)
print(m.points if m is not None else None)
