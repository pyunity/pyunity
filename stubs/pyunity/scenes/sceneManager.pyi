## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""
Module that manages creation and deletion
of Scenes.

"""

__all__ = ["RemoveScene", "GetSceneByName", "LoadSceneByIndex", "AddBareScene",
           "LoadSceneByName", "CurrentScene", "AddScene", "LoadScene",
           "RemoveAllScenes", "GetSceneByIndex", "KeyboardInterruptKill"]

from .runner import Runner
from .scene import Scene
from typing import Dict, List

scenesByIndex: List[Scene] = ...
scenesByName: Dict[str, Scene] = ...
runner: Runner = ...
KeyboardInterruptKill: bool = ...

def AddScene(sceneName: str) -> Scene: ...
def AddBareScene(sceneName: str) -> Scene: ...
def GetSceneByIndex(index: int) -> Scene: ...
def GetSceneByName(name: str) -> Scene: ...
def RemoveScene(scene: Scene) -> None: ...
def RemoveAllScenes() -> None: ...
def LoadSceneByName(name: str) -> None: ...
def LoadSceneByIndex(index: int) -> None: ...
def LoadScene(scene: Scene) -> None: ...
def stopWindow() -> None: ...
def __loadScene(scene: Scene) -> None: ...
def CurrentScene() -> Scene: ...
