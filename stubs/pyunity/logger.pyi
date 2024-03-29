## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

"""
Utility functions to log output of PyUnity.

This will be imported as ``pyunity.Logger``.

"""

__all__ = ["DEBUG", "ELAPSED_TIME", "ERROR", "Elapsed", "INFO", "Level",
           "Log", "LogException", "LogLine", "LogSpecial", "LogTraceback",
           "OUTPUT", "RUNNING_TIME", "ResetStream", "Save", "SetStream",
           "Special", "TIME_FORMAT", "TempRedirect", "WARN"]

from types import TracebackType
from typing import IO, Type, Tuple, Union, Callable
from pathlib import Path
import atexit

TIME_FORMAT: str = ...

def getDataFolder() -> Path: ...

folder: Path = ...
stream: IO[str] = ...
timestamp: str = ...
start: float = ...

class Level:
    abbr: str
    name: str
    def __init__(self, abbr: str) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...

OUTPUT: Level = ...
INFO: Level = ...
DEBUG: Level = ...
ERROR: Level = ...
WARN: Level = ...

class Special:
    func: Callable[[None], str]
    def __init__(self, name: str, func: Callable[[], str]) -> None: ...

class Elapsed:
    def __init__(self) -> None: ...
    def tick(self) -> float: ...

elapsed: Elapsed = ...
RUNNING_TIME: Special = ...
ELAPSED_TIME: Special = ...

def Log(*mesage: str, stacklevel: int = ...) -> None: ...
def LogLine(level: Level, *message: str, stacklevel: int = ..., silent: bool =...) -> Tuple[float, str]: ...
def LogException(e: Exception, stacklevel: int = ..., silent: bool =...) -> None: ...
def LogTraceback(exctype: Type[BaseException], value: Union[BaseException, None], tb: Union[TracebackType, None], stacklevel: int = ...) -> None: ...
def LogSpecial(level: Level, type: Special, stacklevel: int = ...) -> None: ...
@atexit.register
def Save() -> None: ...

class TempRedirect:
    def __init__(self, *, silent: bool = ...) -> None: ...
    def get(self) -> str: ...
    def __enter__(self) -> TempRedirect: ...
    def __exit__(self, exctype: Type[BaseException], value: Union[BaseException, None], tb: Union[TracebackType, None]) -> None: ...

def SetStream(s: IO[str]) -> None: ...
def ResetStream() -> None: ...
