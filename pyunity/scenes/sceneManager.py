"""
Module that manages creation and deletion
of Scenes.

"""

from ..core import *
from ..window import GetWindowProvider
from .. import config
from ..errors import *
from .scene import Scene
from .. import logger as Logger
from .. import render
import os
import copy

config.windowProvider = GetWindowProvider()

scenesByIndex = []
scenesByName = {}
windowObject = None
__running_scenes = []

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
        If there already exists a scene called `sceneName`

    """
    if sceneName in scenesByName:
        raise PyUnityException("SceneManager already contains scene \"" +
                               sceneName + "\"")
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
        If there already exists a scene called `sceneName`

    """
    if sceneName in scenesByName:
        raise PyUnityException("SceneManager already contains scene \"" +
                               sceneName + "\"")
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
        Specified scene at index `index`

    Raises
    ------
    IndexError
        If there is no scene at the specified index

    """
    if len(scenesByIndex) <= index:
        raise IndexError("There is no scene at index " + str(index))
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
        Specified scene with name of `name`

    Raises
    ------
    KeyError
        If there is no scene called `name`

    """
    if name not in scenesByName:
        raise KeyError("There is no scene called " + name)
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
        raise TypeError("The provided scene is not of type Scene")
    if scene not in scenesByIndex:
        raise PyUnityException(
            "Scene \"%s\" is not part of the SceneManager" % scene.name)
    scenesByIndex.remove(scene)
    scenesByName.pop(scene.name)

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
        raise TypeError("\"%r\" is not a string" % name)
    if name not in scenesByName:
        raise PyUnityException("There is no scene named \"%s\"" % name)
    __loadScene(copy.deepcopy(scenesByName[name]))

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
        raise TypeError("\"%r\" is not an integer" % index)
    if index >= len(scenesByIndex):
        raise PyUnityException("There is no scene at index \"%d\"" % index)
    __loadScene(copy.deepcopy(scenesByIndex[index]))

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
        When the scene is not of type `Scene`
    PyUnityException
        When the scene is not part of the SceneManager.
        This is checked because the SceneManager
        has to make some checks before the scene
        can be run.

    """
    if not isinstance(scene, Scene):
        raise TypeError(
            "The provided Scene \"%s\" is not an integer" % scene.name)
    if scene not in scenesByIndex:
        raise PyUnityException(
            "The provided scene is not part of the SceneManager")
    __loadScene(copy.deepcopy(scene))

def __loadScene(scene):
    global windowObject
    __running_scenes.append(scene)
    if not windowObject and os.environ["PYUNITY_INTERACTIVE"] == "1":
        windowObject = config.windowProvider.Window(
            scene.name, scene.mainCamera.Resize)
        render.compile_shaders()
        scene.Start()
        try:
            windowObject.start(scene.update)
        except KeyboardInterrupt:
            Logger.LogLine(Logger.INFO, "Stopping main loop")
            Logger.Save()
            windowObject.quit()
            if KeyboardInterruptKill:
                exit()
        except Exception as e:
            Logger.LogException(e)
            Logger.LogLine(Logger.INFO, "Shutting PyUnity down")
            Logger.Save()
            windowObject.quit()
        else:
            Logger.LogLine(Logger.INFO, "Shutting PyUnity down")
            Logger.Save()
        windowObject = None
    else:
        scene.Start()
        if os.environ["PYUNITY_INTERACTIVE"] == "1":
            windowObject.update_func = scene.update
        else:
            scene.no_interactive()
    scene.clean_up()
    __running_scenes.pop()

def CurrentScene():
    """Gets the current scene being run"""
    if len(__running_scenes) == 0:
        return None
    return __running_scenes[-1]
