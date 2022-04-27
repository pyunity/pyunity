# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import Logger
from . import SceneTestCase

class TestLogger(SceneTestCase):
    def testLog(self):
        with Logger.TempRedirect(silent=True) as r:
            Logger.Log("Test")
        assert r.get() == "Test\n"

        with Logger.TempRedirect(silent=True) as r:
            Logger.LogLine(Logger.WARN, "Test")
        assert r.get() == "Warning: Test\n"

        with Logger.TempRedirect() as r:
            Logger.Log("Test")
        assert r.get() == f"Changed stream to {r.stream}\nTest\n"
