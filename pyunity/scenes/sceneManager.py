# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

"""
Module that manages creation and deletion
of Scenes.

"""

__all__ = ["RemoveScene", "GetSceneByName", "LoadSceneByIndex", "AddBareScene", "LoadSceneByName",
           "CurrentScene", "AddScene", "LoadScene", "RemoveAllScenes", "GetSceneByIndex"]

from .. import config, settings
from ..errors import PyUnityException, PyUnityExit
from .scene import Scene
from .. import logger as Logger
from .. import render
import os
import copy
# import threading

scenesByIndex = []
scenesByName = {}
windowObject = None
__runningScenes = []

FirstScene = True
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
        If there already exists a scene called ``sceneName``

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
        Specified scene at index ``index``

    Raises
    ------
    IndexError
        If there is no scene at the specified index

    """
    if len(scenesByIndex) <= index:
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
    KeyError
        If there is no scene called ``name``

    """
    if name not in scenesByName:
        raise KeyError(f"There is no scene called {name}")
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
        When the scene is not of type :class:`Scene`
    PyUnityException
        When the scene is not part of the SceneManager.
        This is checked because the SceneManager
        has to make some checks before the scene
        can be run.

    """
    if not isinstance(scene, Scene):
        raise TypeError(
            "The provided Scene \"%s\" is not of type \"Scene\"" % scene.name)
    if scene not in scenesByIndex:
        raise PyUnityException(
            "The provided scene is not part of the SceneManager")
    __loadScene(copy.deepcopy(scene))

def __loadScene(scene):
    global windowObject, FirstScene
    __runningScenes.append(scene)
    if not FirstScene:
        Logger.Save()
        FirstScene = False
    if not windowObject:
        hasClosed = False
        if os.environ["PYUNITY_INTERACTIVE"] == "1":
            try:
                os.environ["PYUNITY_GL_CONTEXT"] = "1"
                Logger.LogLine(Logger.DEBUG, "Launching window manager")
                windowObject = config.windowProvider(
                    scene.name, scene.mainCamera.Resize)

                Logger.LogSpecial(Logger.INFO, Logger.ELAPSED_TIME)
                windowObject.refresh()
                render.fillScreen()
                windowObject.refresh()
                render.fillScreen() # double buffering

                # done = False
                # def loop():
                #     while not done:
                #         windowObject.refresh()
                # t = threading.Thread(target=loop)
                # t.daemon = True
                # t.start()

                Logger.LogLine(Logger.DEBUG, "Compiling objects")

                Logger.LogLine(Logger.INFO, "Compiling shaders")
                render.compileShaders()
                Logger.LogSpecial(Logger.INFO, Logger.ELAPSED_TIME)

                Logger.LogLine(Logger.INFO, "Loading skyboxes")
                render.compileSkyboxes()
                Logger.LogSpecial(Logger.INFO, Logger.ELAPSED_TIME)

                # done = True
                # t.join()
            except PyUnityExit:
                hasClosed = True
            except Exception:
                if "windowProvider" in settings.db:
                    Logger.LogLine(Logger.WARN, "Detected settings.json entry")
                    if "windowCache" in settings.db:
                        Logger.LogLine(Logger.WARN, "windowCache entry has been set,",
                                       "indicating window checking happened on this import")
                    Logger.LogLine(
                        Logger.WARN, "settings.json entry may be faulty, removing")
                    settings.db.pop("windowProvider")
                raise

        if os.environ["PYUNITY_INTERACTIVE"] != "1" and config.fps == 0:
            config.fps = 60
            Logger.LogLine(Logger.WARN, "FPS cannot be 0 in non-interactive mode")
        Logger.LogLine(Logger.DEBUG, "Starting scene")
        scene.Start()
        try:
            if hasClosed:
                raise PyUnityExit
            if os.environ["PYUNITY_INTERACTIVE"] == "1":
                windowObject.start(scene.update)
            else:
                scene.noInteractive()
        except (KeyboardInterrupt, PyUnityExit):
            Logger.LogLine(Logger.INFO, "Stopping main loop")
            if os.environ["PYUNITY_INTERACTIVE"] == "1":
                windowObject.quit()
            Logger.LogLine(Logger.INFO, "Shutting PyUnity down")
            if KeyboardInterruptKill:
                exit()
        except Exception:
            Logger.LogLine(Logger.INFO, "Stopping main loop")
            if os.environ["PYUNITY_INTERACTIVE"] == "1":
                windowObject.quit()
            Logger.LogLine(Logger.INFO, "Shutting PyUnity down")
            raise
        else:
            Logger.LogLine(Logger.INFO, "Stopping main loop")
        del os.environ["PYUNITY_GL_CONTEXT"]
        render.resetShaders()
        Logger.LogLine(Logger.INFO, "Reset shaders")
        render.resetSkyboxes()
        Logger.LogLine(Logger.INFO, "Reset skyboxes")
        windowObject = None
    else:
        scene.Start()
        if os.environ["PYUNITY_INTERACTIVE"] == "1":
            windowObject.updateFunc = scene.update
    scene.cleanUp()
    __runningScenes.pop()

def CurrentScene():
    """Gets the current scene being run"""
    if len(__runningScenes) == 0:
        return None
    return __runningScenes[-1]
