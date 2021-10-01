from typing import Any, Dict, Tuple
from .meshes import Mesh
from .files import Skybox
from .values import Color, Vector2, Vector3, Quaternion
from .core import SingleComponent, Transform

float_size: int =...

def gen_buffers(mesh: Mesh) -> Tuple[int, int]: ...
def gen_array() -> int: ...

class Shader:
    vertex: str
    frag: str
    compiled: bool
    name: str
    def __init__(self, vertex: str, frag: str, name: str) -> None: ...
    def compile(self) -> None: ...
    @staticmethod
    def fromFolder(path: str, name: str) -> Shader: ...
    def setVec3(self, var: bytes, val: Any) -> None: ...
    def setMat4(self, var: bytes, val: Any) -> None: ...
    def setInt(self, var: bytes, val: int) -> None: ...
    def setFloat(self, var: bytes, val: float) -> None: ...
    def use(self) -> None: ...

__dir: str = ...
shaders: Dict[str, Shader] = ...
skyboxes: Dict[str, Skybox] = ...

def compile_shaders() -> None: ...

class Camera(SingleComponent):
    near: float = ...
    far: float = ...
    clearColor: Color = ...
    shader: Shader = ...
    skyboxEnabled: bool = ...
    skybox: Skybox = ...
    size: Vector2
    guiShader: Shader
    skyboxShader: Shader
    viewMat: object
    lastPos: Vector3
    lastRot: Quaternion
    renderPass: bool

    def __init__(self, transform: Transform) -> None: ...