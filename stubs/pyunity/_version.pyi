## Copyright (c) 2020-2022 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""
Master version for PyUnity.

"""

__all__ = ["versionInfo"]

from .values import IgnoredMixin, IncludeInstanceMixin

class VersionInfo(IgnoredMixin, IncludeInstanceMixin):
    major: int
    minor: int
    micro: int
    releaselevel: str
    def __init__(self, major: int, minor: int, micro: int, releaselevel: str) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

versionInfo: VersionInfo
__version__: str
