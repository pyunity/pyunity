from ...errors import *
import os
import sys
import pkgutil
import importlib.util

def checkModule(name):
    if os.getenv("PYUNITY_TESTING") is not None:
        return sys.modules[name]
    spec = importlib.util.find_spec(name)
    if spec is None:
        raise ImportError
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules[name] = module
    return module

_loaded = False
_names = [x.name for x in pkgutil.iter_modules(__path__)]

def getProviders():
    global _loaded
    if not _loaded:
        _loaded = True
    return _names
