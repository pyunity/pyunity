# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import Logger
from . import SceneTestCase
import contextlib
import io

class TestLevel(SceneTestCase):
    def testInit(self):
        l = Logger.Level("A")
        assert l.abbr == "A"
        assert l == Logger.Level("A")
        assert l != Logger.Level("B")
        assert l != "A"

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

    def testError(self):
        stream = io.StringIO()
        with contextlib.redirect_stderr(stream):
            Logger.LogLine(Logger.ERROR, "Error")
        assert stream.getvalue() == "Error\n"

        stream = io.StringIO()
        try:
            raise Exception
        except Exception as e:
            with contextlib.redirect_stderr(stream):
                Logger.LogException(e)
        text = stream.getvalue()
        assert text.endswith("Exception\n")
        assert text.startswith("Traceback (most recent call last):\n  ")

        with self.assertRaises(Exception) as exc:
            Logger.TempRedirect().get()
        assert exc.value == "Context manager not used"

    def testMultiline(self):
        with Logger.TempRedirect(silent=True) as r:
            Logger.Log("Test\n\nTest2")
        assert r.get() == "Test\n\nTest2\n"
