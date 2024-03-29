## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""Module for all exceptions and warnings related to PyUnity."""

__all__ = ["ComponentException", "GameObjectException",
           "ProjectParseException", "PyUnityException", "PyUnityExit",
           "WindowProviderException"]

class PyUnityException(Exception): ...
class ComponentException(PyUnityException): ...
class GameObjectException(PyUnityException): ...
class ProjectParseException(PyUnityException): ...
class PyUnityExit(PyUnityException): ...
class WindowProviderException(PyUnityException): ...
