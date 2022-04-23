# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

import re
import sys
import platform
import pkgutil
from ._version import __version__

TITLE_WIDTH = 30

if "--version" in sys.argv or "-v" in sys.argv:
    print("#" * TITLE_WIDTH)
    print("VERSION INFO".center(TITLE_WIDTH))
    print("#" * TITLE_WIDTH)

    vstr = "v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}"
    print("PyUnity version: v" + __version__)
    print("Python version:", vstr.format(sys.version_info))
    print("Operating system:", platform.system(), platform.machine())
    print("Architecture:", platform.architecture()[0])

    if sys.version_info >= (3, 8):
        from importlib.metadata import requires, version, PackageNotFoundError
    elif pkgutil.find_loader("importlib_metadata") is not None:
        from importlib_metadata import requires, version, PackageNotFoundError
    else:
        requires = None

    if requires is not None:
        print("Requirements:")
        for item in requires("pyunity"):
            name = re.split(" |;", item)[0]
            try:
                print("-", name, "version:", version(name))
            except PackageNotFoundError:
                # python_version or sys.platform used
                print("-", name, "version:", None)
    else:
        print("Python version less than 3.8 but no importlib_metadata found")
else:
    from . import examples
    examples.show()
