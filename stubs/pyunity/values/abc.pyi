## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

__all__ = ["ABCException", "ABCMeta", "abstractmethod", "abstractproperty"]

from typing import (
    Callable, Optional, Type, List, Tuple, Any, NoReturn, Mapping,
    Generic, TypeVar, TYPE_CHECKING)
from typing_extensions import ParamSpec
import inspect

if TYPE_CHECKING:
    _T = TypeVar("_T")
    _P = ParamSpec("_P")

class ABCException(Exception): ...

class abstractmethod(Generic[_P, _T]):
    func: Callable[_P, _T]
    args: List[Tuple[str, inspect._ParameterKind]]
    def __init__(self, func: Callable[_P, _T]) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __get__(self, instance: Any, owner: Optional[Type[abstractmethod]] = ...) -> object: ...
    @staticmethod
    def getargs(func: Callable[_P, _T]) -> List[Tuple[str, inspect._ParameterKind]]: ...

class abstractproperty(abstractmethod):
    def __get__(self, instance: Any, owner: Optional[Type[abstractmethod]] = ...) -> object: ...
    def __set__(self, instance: Any, value: object) -> NoReturn: ...
    def __eq__(self, other: object) -> bool: ...

class ABCMeta(type):
    _trigger: bool = ...
    def __init__(cls, name: str, bases: Tuple[type, ...], attrs: dict[str, Any], **kwds: Any) -> None: ...
