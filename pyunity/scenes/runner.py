__all__ = ["ChangeScene", "Runner", "WindowRunner", "NonInteractiveRunner", "newRunner"]

from .. import config, render, Logger
from ..events import EventLoopManager, WaitForUpdate, WaitForFixedUpdate, WaitForRender
from ..errors import PyUnityException
import copy
import os

class ChangeScene(Exception):
    pass

class Runner:
    def __init__(self):
        self.scene = None
        self.next = None
        self.opened = False

    def setScene(self, scene):
        if self.opened:
            raise PyUnityException("Cannot set scene after opening runner")
        self.scene = copy.deepcopy(scene)

    def setNext(self, scene):
        if self.scene is None:
            raise PyUnityException("Cannot set next before first scene")
        self.next = copy.deepcopy(scene)
        raise ChangeScene

    def open(self):
        if self.scene is None:
            raise PyUnityException("Cannot open runner before setting a scene")
        if self.opened:
            Logger.Save()
        self.opened = True

    def setup(self):
        pass

    def load(self, updates):
        if self.scene is None:
            raise PyUnityException("Cannot load runner before setting a scene")
        Logger.LogLine(Logger.DEBUG, "Starting scene")
        self.eventLoopManager = EventLoopManager()
        self.eventLoopManager.schedule(*updates, ups=config.fps, waitFor=WaitForUpdate)
        self.eventLoopManager.schedule(self.scene.updateFixed, ups=50, waitFor=WaitForFixedUpdate)
        self.eventLoopManager.addLoop(self.scene.startScripts())

    def start(self):
        while True:
            try:
                self.eventLoopManager.start()
                break
            except ChangeScene:
                if self.next is None:
                    raise
                self.eventLoopManager.quit()
                self.scene.cleanUp()
                self.scene = self.next
                self.next = None
                self.load()

    def quit(self):
        self.eventLoopManager.quit()
        self.scene.cleanUp()

        self.scene = None
        self.opened = False

class WindowRunner(Runner):
    def open(self):
        super(WindowRunner, self).open()
        os.environ["PYUNITY_GL_CONTEXT"] = "1"

        self.window = config.windowProvider(self.scene.name)
        # front buffer
        self.window.refresh()
        render.fillScreen()
        # back buffer
        self.window.refresh()
        render.fillScreen()

    def setup(self):
        Logger.LogSpecial(Logger.INFO, Logger.ELAPSED_TIME)
        Logger.LogLine(Logger.DEBUG, "Compiling objects")

        Logger.LogLine(Logger.INFO, "Compiling shaders")
        render.compileShaders()
        Logger.LogSpecial(Logger.INFO, Logger.ELAPSED_TIME)

        Logger.LogLine(Logger.INFO, "Loading skyboxes")
        render.compileSkyboxes()
        Logger.LogSpecial(Logger.INFO, Logger.ELAPSED_TIME)

    def load(self):
        super(WindowRunner, self).load([self.scene.updateScripts, self.window.updateFunc])
        self.eventLoopManager.schedule(
            self.scene.Render, self.window.refresh,
            main=True, waitFor=WaitForRender)
        if self.scene.mainCamera is not None:
            self.window.setResize(self.scene.mainCamera.Resize)
        self.scene.startOpenGL()
        self.scene.startLoop()

    def start(self):
        super(WindowRunner, self).start()

    def quit(self):
        super(WindowRunner, self).quit()
        del self.window

        del os.environ["PYUNITY_GL_CONTEXT"]
        render.resetShaders()
        Logger.LogLine(Logger.INFO, "Reset shaders")
        render.resetSkyboxes()
        Logger.LogLine(Logger.INFO, "Reset skyboxes")

class NonInteractiveRunner(Runner):
    def load(self):
        super(NonInteractiveRunner, self).load([self.scene.updateScripts])
        self.scene.startLoop()

def newRunner():
    if os.environ["PYUNITY_INTERACTIVE"] == "1":
        return WindowRunner()
    else:
        return NonInteractiveRunner()