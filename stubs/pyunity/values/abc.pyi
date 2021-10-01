from typing import Callable, Optional, Type, List, Tuple, Any
import inspect

class ABCException(Exception): ...
class ABCMessage(ABCException): ...

class abstractmethod:
    func: Callable
    args: List[Tuple[str, inspect._ParameterKind]]
    def __init__(self, func: Callable) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __get__(self, instance: abstractmethod, owner: Type[abstractmethod]) -> Callable: ...
    @staticmethod
    def getargs(func: Callable) -> List[Tuple[str, inspect._ParameterKind]]: ...

class abstractproperty(abstractmethod):
    def __eq__(self, other: object) -> bool: ...

class ABCMeta(type):
    def __init__(cls, fullname: str, bases: Tuple[type, ...], attrs: dict[str, Any], message: str =...) -> None: ...
    def __new__(cls: Type[Any], fullname: str, bases: Tuple[type, ...], attrs: dict[str, Any], message: Optional[str] =...) -> ABCMeta: ...