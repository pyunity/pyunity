## Copyright (c) 2020-2022 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""
Master version for PyUnity.

"""

__all__ = ["versionInfo"]

class VersionInfo:
    def __init__(self, major, minor, micro, releaselevel):
        self.major = major
        self.minor = minor
        self.micro = micro
        self.releaselevel = releaselevel

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.micro}"

    def __repr__(self):
        return "VersionInfo(" + ", ".join(map(str, [
            self.major, self.minor, self.micro, self.releaselevel])) + ")"

versionInfo = VersionInfo(0, 9, 0, "beta")
__version__ = str(versionInfo)
