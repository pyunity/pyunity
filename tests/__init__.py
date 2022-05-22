# Copyright (c) 2020-2022 The PyUnity Team
# This file is licensed under the MIT License.
# See https://docs.pyunity.x10.bz/en/latest/license.html

__all__ = ["TestCase", "almostEqual"]
from .util import TestCase, almostEqual

import os
import sys
from unittest.mock import Mock

if "full" not in os.environ:
    sys.modules["sdl2"] = Mock()
    sys.modules["sdl2.sdlmixer"] = Mock()
    sys.modules["sdl2.ext"] = Mock()
    sys.modules["sdl2.video"] = Mock()
    sys.modules["glfw"] = Mock()
    sys.modules["PIL"] = Mock()
    sys.modules["OpenGL"] = Mock()
    sys.modules["OpenGL.GL"] = Mock()
    sys.modules["OpenGL.GLUT"] = Mock()
    os.environ["PYUNITY_INTERACTIVE"] = "0"
else:
    os.environ["PYUNITY_CHECK_WINDOW"] = "1"
