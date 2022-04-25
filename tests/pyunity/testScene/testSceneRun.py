import os
from pyunity import (
    Behaviour, SceneManager, AudioListener, Logger, GameObject)
from . import SceneTestCase

class TestBehaviour1(Behaviour):
    def Start(self):
        Logger.Log("Start")

class TestSceneRun:
    class TestStartScripts:
        class TestAudioListeners(SceneTestCase):
            def setUp(self):
                super().setUp()
                os.environ["PYUNITY_INTERACTIVE"] = "0"

            def testCase1(self):
                scene = SceneManager.AddScene("Scene")
                scene.startScripts()
                assert scene.audioListener is not None

            def testCase2(self):
                scene = SceneManager.AddScene("Scene")
                scene.mainCamera.RemoveComponent(AudioListener)

                with Logger.TempRedirect(silent=True) as r:
                    scene.startScripts()
                assert r.get() == "Warning: No AudioListeners found, audio is disabled\n"
                assert scene.audioListener is None

            def testCase3(self):
                scene = SceneManager.AddScene("Scene")
                gameObject = GameObject("Listener")
                gameObject.AddComponent(AudioListener)
                scene.Add(gameObject)

                with Logger.TempRedirect(silent=True) as r:
                    scene.startScripts()
                assert r.get() == "Warning: Ambiguity in AudioListeners, 2 found\n"
                assert scene.audioListener is None

        class TestBehaviours(SceneTestCase):
            def setUp(self):
                super().setUp()
                os.environ["PYUNITY_INTERACTIVE"] = "0"

            def testCase1(self):
                scene = SceneManager.AddScene("Scene")
                gameObject = GameObject("Test")
                gameObject.AddComponent(TestBehaviour1)
                scene.Add(gameObject)

                with Logger.TempRedirect(silent=True) as r:
                    scene.startScripts()
                assert r.get() == "Start\n"
