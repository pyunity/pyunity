## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""
Master version for PyUnity.

"""

__all__ = ["versionInfo"]

from .values import IgnoredMixin, IncludeInstanceMixin

class VersionInfo(IgnoredMixin, IncludeInstanceMixin):
    """
    Class to hold version information for PyUnity.
    It should only be used in ``_version.py``.

    Parameters
    ----------
    major : int
        Major version
    minor : int
        Minor version
    micro : int
        Micro version
    releaselevel : str
        Release level ("a" for alpha, "b" for beta, "rc" for
        release candidate and "final" for a released version)

    """
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

versionInfo = VersionInfo(0, 9, 0, "b")
__version__ = str(versionInfo)
