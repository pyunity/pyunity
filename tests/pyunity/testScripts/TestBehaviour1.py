## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

from pyunity import Behaviour

class TestBehaviour1(Behaviour):
    def Start(self):
        print(self.gameObject.name)
