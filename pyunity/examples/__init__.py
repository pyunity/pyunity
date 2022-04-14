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
broken = [3]

def load_example(i):
    try:
        module = importlib.import_module(f".example{i}", __name__)
    except ImportError:
        raise PyUnityException(f"Invalid example: {i!r}")
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
            load_example(i)
    else:
        load_example(num)
