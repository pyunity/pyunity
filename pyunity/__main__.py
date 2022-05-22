# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

import re
import os
import sys
import platform
import pkgutil
from ._version import __version__
from . import Logger

TITLE_WIDTH = 30

if "--version" in sys.argv or "-v" in sys.argv:
    Logger.Log("#" * TITLE_WIDTH)
    Logger.Log("VERSION INFO".center(TITLE_WIDTH))
    Logger.Log("#" * TITLE_WIDTH)

    vstr = "v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}"
    Logger.Log("PyUnity version: v" + __version__)
    Logger.Log("Python version:", vstr.format(sys.version_info))
    Logger.Log("Operating system:", platform.system(), platform.release())
    Logger.Log("Machine:", platform.machine())
    Logger.Log("Python architecture:", platform.architecture()[0])

    if sys.version_info >= (3, 8):
        from importlib.metadata import requires, version, PackageNotFoundError
    elif pkgutil.find_loader("importlib_metadata") is not None:
        from importlib_metadata import requires, version, PackageNotFoundError
    else:
        Logger.LogLine(Logger.WARN,
                       "Python version less than 3.8 but no importlib_metadata found")

    if requires is not None:
        try:
            requirements = requires("pyunity")
        except PackageNotFoundError:
            Logger.LogLine(Logger.WARN,
                           "PyUnity not ran as an installed package")
            requirements = []
        if not len(requirements):
            if os.path.isfile("requirements.txt"):
                with open("requirements.txt") as f:
                    requirements = f.read().rstrip().split("\n")
            else:
                Logger.LogLine(Logger.WARN,
                               "No requirements.txt file found")

        Logger.Log("Dependencies:")
        for item in requirements:
            name = re.split(" |;", item)[0]
            try:
                Logger.Log("-", name, "version:", version(name))
            except PackageNotFoundError:
                # python_version or sys.platform used
                Logger.Log("-", name, "version:", None)
else:
    from . import examples
    examples.show()
