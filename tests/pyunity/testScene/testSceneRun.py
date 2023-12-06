## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import (AudioListener, Behaviour, Collider, GameObject, Logger,
                     Rigidbody, SceneManager, config)
from . import SceneTestCase
import pytest
import os

class TestBehaviour1(Behaviour):
    def Start(self):
        Logger.Log("Start")

class TestSceneRun:
    class TestStartScripts:
        class TestAudioListeners(SceneTestCase):
            def setUp(self):
                super().setUp()
                os.environ["PYUNITY_INTERACTIVE"] = "0"
                config.audio = True

            def testCase1(self):
                scene = SceneManager.AddScene("Scene")
                scene.startScripts()
                assert scene.audioListener is not None

            def testCase2(self):
                scene = SceneManager.AddScene("Scene")
                scene.mainCamera.RemoveComponent(AudioListener)

                with Logger.TempRedirect(silent=True) as r:
                    scene.startScripts()
                assert r.get() == "Warning: No enabled AudioListeners found, audio is disabled\n"
                assert scene.audioListener is None

            def testCase3(self):
                scene = SceneManager.AddScene("Scene")
                gameObject = GameObject("Listener")
                gameObject.AddComponent(AudioListener)
                scene.Add(gameObject)

                with Logger.TempRedirect(silent=True) as r:
                    scene.startScripts()
                assert r.get() == "Warning: Ambiguity in AudioListeners, 2 enabled\n"
                assert scene.audioListener is None

        class TestBehaviours(SceneTestCase):
            def setUp(self):
                super().setUp()
                os.environ["PYUNITY_INTERACTIVE"] = "0"
                pytest.skip("Scene loading requires a Runner")

            def testCase1(self):
                scene = SceneManager.AddScene("Scene")
                gameObject = GameObject("Test")
                gameObject.AddComponent(TestBehaviour1)
                scene.Add(gameObject)

                with Logger.TempRedirect(silent=True) as r:
                    scene.startScripts()
                assert r.get() == "Start\n"

        class TestMeshBuffers(SceneTestCase):
            def setUp(self):
                super().setUp()
                os.environ["PYUNITY_INTERACTIVE"] = "1"

        class TestCameraBuffers(SceneTestCase):
            def setUp(self):
                super().setUp()
                os.environ["PYUNITY_INTERACTIVE"] = "1"

        class TestCollManager(SceneTestCase):
            def setUp(self):
                super().setUp()
                os.environ["PYUNITY_INTERACTIVE"] = "0"

            def testRigidbodies(self):
                scene = SceneManager.AddScene("Scene")
                gameObject1 = GameObject("With Rigidbody")
                rb = gameObject1.AddComponent(Rigidbody)
                coll1 = gameObject1.AddComponent(Collider)
                coll2 = gameObject1.AddComponent(Collider)
                scene.Add(gameObject1)

                gameObject2 = GameObject("Without Rigidbody")
                coll3 = gameObject2.AddComponent(Collider)
                scene.Add(gameObject2)

                scene.startScripts()

                assert hasattr(scene, "physics")
                assert scene.physics
                assert hasattr(scene, "collManager")
                assert scene.collManager.rigidbodies[rb] == [coll1, coll2]
                assert scene.collManager.rigidbodies[scene.collManager.dummyRigidbody] == [coll3]
