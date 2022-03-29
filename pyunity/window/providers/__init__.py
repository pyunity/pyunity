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
_names = []

def sort(x):
    module = importlib.import_module(f".{x}", __name__)
    if hasattr(module, "prio"):
        return module.prio
    return 0

def getProviders():
    global _names, _loaded
    if not _loaded:
        _names = [x.name for x in pkgutil.iter_modules(__path__)]
        _names.sort(key=sort, reversed=True)
        _loaded = True
    return _names
