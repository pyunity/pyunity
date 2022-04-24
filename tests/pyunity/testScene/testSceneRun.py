import os
from pyunity import (
    SceneManager)
from . import SceneTestCase

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
