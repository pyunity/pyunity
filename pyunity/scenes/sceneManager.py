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

from .. import logger as Logger
from .. import settings
from ..errors import PyUnityException, PyUnityExit
from .runner import newRunner
from .scene import Scene

scenesByIndex = []
scenesByName = {}
runner = newRunner()
KeyboardInterruptKill = False

def AddScene(sceneName):
    """
    Add a scene to the SceneManager. Pass
    in a scene name to create a scene.

    Parameters
    ----------
    sceneName : str
        Name of the scene

    Returns
    -------
    Scene
        Newly created scene

    Raises
    ------
    PyUnityException
        If there already exists a scene called ``sceneName``

    """
    if sceneName in scenesByName:
        raise PyUnityException(
            f"SceneManager already contains scene {sceneName!r}")
    scene = Scene(sceneName)
    scenesByIndex.append(scene)
    scenesByName[sceneName] = scene
    return scene

def AddBareScene(sceneName):
    """
    Add a scene to the SceneManager. Pass
    in a scene name to create a scene.

    Parameters
    ----------
    sceneName : str
        Name of the scene

    Returns
    -------
    Scene
        Newly created scene

    Raises
    ------
    PyUnityException
        If there already exists a scene called ``sceneName``

    """
    if sceneName in scenesByName:
        raise PyUnityException(
            f"SceneManager already contains scene {sceneName!r}")
    scene = Scene.Bare(sceneName)
    scenesByIndex.append(scene)
    scenesByName[sceneName] = scene
    return scene

def GetSceneByIndex(index):
    """
    Get a scene by its index.

    Parameters
    ----------
    index : int
        Index of the scene

    Returns
    -------
    Scene
        Specified scene at index ``index``

    Raises
    ------
    IndexError
        If there is no scene at the specified index

    """
    if len(scenesByIndex) <= index or len(scenesByIndex) < 0:
        raise IndexError(f"There is no scene at index {index}")
    return scenesByIndex[index]

def GetSceneByName(name):
    """
    Get a scene by its name.

    Parameters
    ----------
    name : str
        Name of the scene

    Returns
    -------
    Scene
        Specified scene with name of ``name``

    Raises
    ------
    PyUnityException
        If there is no scene called ``name``

    """
    if name not in scenesByName:
        raise PyUnityException(f"There is no scene called {name!r}")
    return scenesByName[name]

def RemoveScene(scene):
    """
    Removes a scene from the SceneManager.

    Parameters
    ----------
    scene : Scene
        Scene to remove

    Raises
    ------
    TypeError
        If the provided scene is not type Scene
    PyUnityException
        If the scene is not part of the SceneManager

    """
    if not isinstance(scene, Scene):
        raise TypeError(f"Expected Scene, got {type(scene).__name__}")
    if scene not in scenesByIndex:
        raise PyUnityException(
            f"Scene {scene.name!r} is not part of the SceneManager")
    scenesByIndex.remove(scene)
    scenesByName.pop(scene.name)

def RemoveAllScenes():
    """
    Removes all scenes from the SceneManager.

    """
    for scene in scenesByIndex:
        scenesByName.pop(scene.name)
    scenesByIndex.clear()

def LoadSceneByName(name):
    """
    Loads a scene by its name.

    Parameters
    ----------
    name : str
        Name of the scene

    Raises
    ------
    TypeError
        When the provided name is not a string
    PyUnityException
        When there is no scene named ``name``

    """
    if not isinstance(name, str):
        raise TypeError(f"Expected str, got {type(name).__name__}")
    if name not in scenesByName:
        raise PyUnityException(f"There is no scene named {name!r}")
    __loadScene(scenesByName[name])

def LoadSceneByIndex(index):
    """
    Loads a scene by its index of when it was added
    to the SceneManager.

    Parameters
    ----------
    index : int
        Index of the scene

    Raises
    ------
    TypeError
        When the provided index is not an integer
    PyUnityException
        When there is no scene at index ``index``

    """
    if not isinstance(index, int):
        raise TypeError(f"Expected int, got {type(index).__name__}")
    if index >= len(scenesByIndex):
        raise PyUnityException(f"There is no scene at index {index}")
    __loadScene(scenesByIndex[index])

def LoadScene(scene):
    """
    Load a scene by a reference.

    Parameters
    ----------
    scene : Scene
        Scene to be loaded

    Raises
    ------
    TypeError
        When the scene is not of type :class:`Scene`
    PyUnityException
        When the scene is not part of the SceneManager.
        This is checked because the SceneManager
        has to make some checks before the scene
        can be run.

    """
    if not isinstance(scene, Scene):
        raise TypeError(f"Expected Scene, got {type(scene).__name__}")
    if scene not in scenesByIndex:
        raise PyUnityException(
            "The provided scene is not part of the SceneManager")
    __loadScene(scene)

def stopWindow():
    Logger.LogLine(Logger.INFO, "Stopping main loop")
    runner.quit()

def __loadScene(scene):
    if not runner.opened:
        runner.setScene(scene)
        try:
            runner.open()
        except PyUnityExit:
            stopWindow()
            return
        except Exception:
            Logger.LogLine(Logger.ERROR,
                           "Exception while launching window manager")
            if "windowProvider" in settings.db:
                Logger.LogLine(Logger.WARN, "Detected settings.json entry")
                if "windowCache" in settings.db:
                    Logger.LogLine(Logger.WARN, "windowCache entry has been set,",
                                   "indicating window checking happened on this import")
                Logger.LogLine(Logger.WARN, "settings.json entry may be faulty, removing")
                settings.db.pop("windowProvider")
            raise
        runner.setup()
    else:
        runner.setNext(scene)
    runner.load()

    try:
        runner.start()
    except (SystemExit, KeyboardInterrupt, PyUnityExit) as e:
        stopWindow()
        if isinstance(e, KeyboardInterrupt) and KeyboardInterruptKill:
            exit()
    except Exception:
        stopWindow()
        raise

def CurrentScene():
    """Gets the current scene being run"""
    return runner.scene
