# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

from ..scenes import SceneManager
from ..errors import PyUnityException
from .. import Logger
import pkgutil
import sys
import importlib

SceneManager.KeyboardInterruptKill = True
broken = []

def loadExample(i):
    if pkgutil.find_loader(__name__ + f".example{i}") is None:
        raise PyUnityException(f"Invalid example: {i!r}")
    module = importlib.import_module(f".example{i}", __name__)
    Logger.Log("\nExample", i)
    module.main()
    SceneManager.RemoveAllScenes()

def show(num=None):
    if len(broken):
        Logger.LogLine(Logger.WARN, "Currently broken examples: " +
                       ", ".join(map(str, broken)))
    if num is None:
        if len(sys.argv) == 1:
            num = "0"
        else:
            num = sys.argv[1]
    if num == "0":
        for i in range(1, len(list(pkgutil.iter_modules(__path__))) + 1):
            if i in broken:
                continue
            loadExample(i)
    else:
        loadExample(num)
