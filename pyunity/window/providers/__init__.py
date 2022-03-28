from ...errors import *
import os
import sys
import importlib.util

def checkModule(name):
    if os.getenv("PYUNITY_TESTING") is not None:
        return sys.modules[name]
    spec = importlib.util.find_spec(name)
    if spec is None:
        raise PyUnityException
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules[name] = module
    return module
