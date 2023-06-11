## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

__all__ = ["Event", "EventLoop", "EventLoopManager", "StartCoroutine",
           "WaitFor", "WaitForEventLoop", "WaitForFixedUpdate",
           "WaitForRender", "WaitForSeconds", "WaitForUpdate"]

from .core import Component
from typing import (
    TypeVar, Callable, Any, Sequence, Mapping, Optional, Type, Union,
    List, Dict, Awaitable, Generator, Generic, TYPE_CHECKING)
import threading
import asyncio
import signal

if TYPE_CHECKING:
    T = TypeVar("T")
    AT = TypeVar("AT")

class Event(Generic[T]):
    component: Component
    name: str
    func: Callable[..., T]
    args: Sequence[Any]
    kwargs: Mapping[str, Any]
    isAsync: bool
    def __init__(self, func: Callable[..., T], args: Sequence[Any] = ..., kwargs: Mapping[str, Any] = ...) -> None: ...
    def trigger(self) -> T: ...
    def callSoon(self) -> None: ...
    @classmethod
    def _factoryWrapper(cls, factory: Callable[..., Event]) -> Callable[..., Event]: ...

class EventLoopManager:
    current: Union[EventLoopManager, None] = ...
    exceptions: List[Exception] = ...
    exceptionLock: threading.RLock = ...
    waitingLock: threading.RLock = ...
    threads: List[threading.Thread]
    loops: List[EventLoop]
    separateLoops: List[EventLoop]
    waiting: Dict[Type[WaitForEventLoop], List[WaitForEventLoop]]
    pending: List[Event]
    updates: List[Callable[[EventLoop], None]]
    mainLoop: EventLoop
    mainWaitFor: Type[WaitForEventLoop]
    running: bool
    def __init__(self) -> None: ...
    def schedule(self, *funcs: List[Callable[[EventLoop], None]], main: bool = ..., ups: Optional[float] = ..., waitFor: Optional[Type[WaitForEventLoop]] = ...) -> None: ...
    def addLoop(self, loop: EventLoop) -> None: ...
    def start(self) -> None: ...
    def quit(self) -> None: ...

class EventLoop(asyncio.SelectorEventLoop):
    def __init__(self, selector: Optional[Any] = ...) -> None: ...
    async def shutdown(self, signal: Optional[signal.Signals] = ...) -> None: ...
    def handleException(self, context: Mapping[str, Any]) -> None: ...

def StartCoroutine(coro: Awaitable[None]) -> None: ...

class WaitFor: ...

class WaitForSeconds(WaitFor):
    def __init__(self, length: float) -> None: ...
    def __await__(self) -> Generator[Any, None, float]: ...

class WaitForEventLoop(WaitFor):
    def __init__(self) -> None: ...
    def __await__(self) -> Generator[Any, None, float]: ...

class WaitForUpdate(WaitForEventLoop): ...
class WaitForFixedUpdate(WaitForEventLoop): ...
class WaitForRender(WaitForEventLoop): ...
