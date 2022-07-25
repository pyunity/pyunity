## Copyright (c) 2020-2022 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

__all__ = ["TestCase", "almostEqual", "SceneTestCase"]
from .. import TestCase, almostEqual

import os
import pytest
from pyunity import SceneManager

class SceneTestCase(TestCase):
    def setUp(self):
        if "full" not in os.environ:
            pytest.skip("GLM not loaded; scene creation will fail")

    def tearDown(self):
        SceneManager.RemoveAllScenes()

# self\.assertEqual\((.*?), (.*?)\)
# assert $1 == $2

# self\.assertIsInstance\((.*?), (.*?)\)
# assert isinstance($1, $2)

# self\.assertIs\((.*?), (.*?)\)
# assert $1 is $2
