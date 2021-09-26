from ..scenes import SceneManager
from .. import Logger
import sys
import os
import glob
import importlib

SceneManager.KeyboardInterruptKill = True
broken = []
directory = os.path.dirname(os.path.abspath(__file__))

def load_example(i):
    module = importlib.import_module(f".example{i}", __name__)
    module.main()
    SceneManager.RemoveAllScenes()

def show(num=None):
    if len(broken):
        Logger.LogLine(Logger.WARN, "Currently broken examples: " +
                       ", ".join(map(str, broken)))
    if num is None:
        if len(sys.argv) == 1:
            num = 0
        else:
            num = int(sys.argv[1])
    if num == 0:
        for i in range(1, len(glob.glob(os.path.join(directory, "example*"))) + 1):
            if i in broken:
                continue
            Logger.Log("\nExample", i)
            load_example(i)
    else:
        load_example(num)
