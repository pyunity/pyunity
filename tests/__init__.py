# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

__all__ = ["TestCase", "almostEqual"]
from .util import TestCase, almostEqual

import os
import sys
import math
from unittest.mock import Mock

if "full" not in os.environ:
    def atan(*args):
        if len(args) == 2:
            return math.atan2(*args)
        else:
            return math._atan(*args)

    def pi():
        return math._pi

    math._atan = math.atan
    math.atan = atan
    math._pi = math.pi
    math.pi = pi

    sys.modules["sdl2"] = Mock()
    sys.modules["sdl2.sdlmixer"] = Mock()
    sys.modules["sdl2.ext"] = Mock()
    sys.modules["sdl2.video"] = Mock()
    sys.modules["glfw"] = Mock()
    sys.modules["glm"] = math
    sys.modules["PIL"] = Mock()
    sys.modules["OpenGL"] = Mock()
    sys.modules["OpenGL.GL"] = Mock()
    sys.modules["OpenGL.GLUT"] = Mock()
    os.environ["PYUNITY_INTERACTIVE"] = "0"
else:
    os.environ["PYUNITY_CHECK_WINDOW"] = "1"
