# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import Scripts, PyUnityException, Logger
from pathlib import Path
from . import TestCase
import sys

currentdir = Path(__file__).absolute().parent

class TestScripts(TestCase):
    def testCheckScript(self):
        with open(currentdir / "file1.py") as f:
            assert Scripts.CheckScript(f.read().split("\n"))

        with open(currentdir / "file2.py") as f:
            assert not Scripts.CheckScript(f.read().split("\n"))

    def testLoadScript(self):
        sys.modules["PyUnityScripts"] = 0
        with Logger.TempRedirect(silent=True) as r:
            Scripts.GenerateModule()
        assert r.get() == "Warning: PyUnityScripts is already a package\n"
        sys.modules.pop("PyUnityScripts")
        module = Scripts.GenerateModule()
        assert module is Scripts.GenerateModule()

        file = currentdir / "TestBehaviour1.py"
        module = Scripts.LoadScript(file)
        assert hasattr(module, "__pyunity__")
        assert module.__pyunity__
        assert __import__("PyUnityScripts") is module
        assert str(file) in module._lookup
        assert "TestBehaviour1" in Scripts.var
        assert "TestBehaviour1" in module.__all__
        assert hasattr(module, "TestBehaviour1")
        assert hasattr(module, "TestBehaviour1")

    def testLoadScriptFails(self):
        with self.assertRaises(PyUnityException) as exc:
            Scripts.LoadScript("DoesNotExist.py")
        assert exc.value == "The specified file does not exist: 'DoesNotExist.py'"

        file = currentdir / "file1.py"
        with self.assertRaises(PyUnityException) as exc:
            Scripts.LoadScript(file)
        assert exc.value == f"Cannot find class 'file1' in {str(file)!r}"

        file = currentdir / "file2.py"
        with Logger.TempRedirect(silent=True) as r:
            Scripts.LoadScript(file)
        assert r.get() == f"Warning: {str(file)!r} is not a valid PyUnity script\n"
