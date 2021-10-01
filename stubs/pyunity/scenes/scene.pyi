from typing import Dict, List as _List, Type, TypeVar
from ..render import Camera
from ..core import GameObject, Light, MeshRenderer
from ..audio import AudioListener

disallowed_chars: str = ...

class Scene:
    name: str
    mainCamera: Camera
    gameObjects: _List[GameObject]
    lights: _List[Light]
    ids: Dict[str, int]
    id: str
    audioListener: AudioListener
    physics: bool
    lastFrame: float
    def __init__(self, name: str) -> None: ...
    @staticmethod
    def Bare(name: str) -> Scene: ...
    @property
    def rootGameObjects(self) -> _List[GameObject]: ...
    def Add(self, gameObject: GameObject) -> None: ...
    def Remove(self, gameObject: GameObject) -> None: ...
    def Has(self, gameObject: GameObject) -> bool: ...
    def RegisterLight(self, light: Light) -> None: ...
    def List(self) -> None: ...
    def FindGameObjectsByName(self, name: str) -> _List[GameObject]: ...
    def FindGameObjectsByTagName(self, name: str) -> _List[GameObject]: ...
    def FindGameObjectsByTagNumber(self, num: int) -> _List[GameObject]: ...
    T = TypeVar("T", bound=Scene)
    def FindComponentByType(self, component: Type[T]) -> T: ...
    def FindComponentsByType(self, component: Type[T]) -> _List[T]: ...
    def inside_frustrum(self, renderer: MeshRenderer) -> bool: ...
    def start_scripts(self) -> None: ...
    def Start(self) -> None: ...
    def update_scripts(self) -> None: ...
    def no_interactive(self) -> None: ...
    def update(self) -> None: ...
    def Render(self) -> None: ...
    def clean_up(self) -> None: ...