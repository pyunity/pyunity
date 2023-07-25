## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

import os
import sys
import pkgutil
import importlib.util

_loaded = False
_names = []

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

def getPriority(name):
    module = importlib.import_module(f".{name}.checker", __name__)
    if hasattr(module, "prio"):
        return module.prio
    return 0

def getProviders():
    global _names, _loaded
    if not _loaded:
        _names = [x.name for x in pkgutil.iter_modules(__path__)]
        _names.sort(key=getPriority, reverse=True)
        _loaded = True
    return _names
