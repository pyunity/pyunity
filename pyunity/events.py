## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

__all__ = ["Event", "EventLoopManager", "EventLoop", "WaitFor", "WaitForSeconds",
           "WaitForEventLoop", "WaitForUpdate", "WaitForFixedUpdate",
           "WaitForRender", "StartCoroutine"]

from . import Logger, config
from .core import Component, GameObject
from .errors import PyUnityException
from .values import Clock, SavableStruct, StructEntry
import sys
import time
import signal
import asyncio
import inspect
import functools
import threading

# TODO: support kwargs=StructEntry(dict, required=True)
# see issue #72 in github
@SavableStruct(
    component=StructEntry(Component, required=True),
    name=StructEntry(str, required=True),
    args=StructEntry(tuple, required=True))
class Event:
    """
    Class used for PyUnity events. Used to set callback
    events of certain :class:`Component`\s, for example
    :class:`GuiComponent`.

    Arguments
    ---------
    func : Callable
        Function to call. Must be a method of a Component
        that is added to a GameObject
    args : tuple, optional
        Positional arguments for the callback
    kwargs : dict, optional
        Keyword arguments for the callback

    """

    def __init__(self, func, args=(), kwargs={}):
        if not hasattr(func, "__self__"):
            raise PyUnityException(
                "Cannot create event from callback that is not attached to a Component")
        if not isinstance(func.__self__, Component):
            raise PyUnityException(
                "Cannot create event from callback that is not attached to a Component")
        if not isinstance(func.__self__.gameObject, GameObject):
            raise PyUnityException(
                "Provided callback component does not belong to a GameObject")

        functools.update_wrapper(self, func)

        self.component = func.__self__
        self.name = func.__name__

        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.isAsync = inspect.iscoroutinefunction(func)

    def trigger(self):
        return self.func(*self.args, **self.kwargs)

    def callSoon(self):
        if self.isAsync:
            loop = asyncio.get_running_loop()
            loop.create_task(self.trigger())
        else:
            if EventLoopManager.current is None:
                raise PyUnityException("No EventLoopManager running")
            EventLoopManager.current.pending.append(self)

    @classmethod
    def _factoryWrapper(cls, factory):
        def wrapper(component, method, args=(), kwargs={}):
            func = getattr(component, method)
            return factory(func, args, kwargs)
        return wrapper

def wrap(func):
    @functools.wraps(func)
    def inner(loop):
        return func()
    return inner

class EventLoopManager:
    current = None
    exceptions = []
    exceptionLock = threading.RLock()
    waitingLock = threading.RLock()

    def __init__(self):
        self.threads = []
        self.loops = []
        self.separateLoops = []
        self.waiting = {}
        self.pending = []
        self.updates = []
        self.mainLoop = None
        self.mainWaitFor = None
        self.running = False

    def schedule(self, *funcs, main=False, ups=None, waitFor=None):
        functions = list(funcs)
        for i in range(len(functions)):
            sig = inspect.signature(functions[i])
            if "loop" not in sig.parameters:
                functions[i] = wrap(functions[i])

        if main:
            self.updates.extend(functions)
            self.mainWaitFor = waitFor
        else:
            if ups is None:
                raise PyUnityException("ups argument is required if main is False")

            self.waiting[waitFor] = []
            loop = EventLoop()
            self.loops.append(loop)

            def inner():
                clock = Clock()
                clock.Start(ups)
                while self.running:
                    with EventLoopManager.waitingLock:
                        for waiter in self.waiting[waitFor]:
                            waiter.loop.call_soon_threadsafe(waiter.event.set)

                    for func in functions:
                        try:
                            func(loop)
                        except Exception as e:
                            with EventLoopManager.exceptionLock:
                                EventLoopManager.exceptions.append(e)
                            break
                        loop.call_soon(loop.stop)
                        loop.run_forever()
                    clock.Maintain()

            t = threading.Thread(target=inner, daemon=True)
            self.threads.append(t)

    def addLoop(self, loop):
        def inner():
            while self.running:
                loop.call_soon(loop.stop)
                loop.run_forever()

        self.loops.append(loop)
        self.separateLoops.append(loop)
        t = threading.Thread(target=inner, daemon=True)
        self.threads.append(t)

    def start(self):
        self.setup()
        while self.running:
            self.update()

    def setup(self):
        if EventLoopManager.current is not None:
            raise PyUnityException("Only one EventLoopManager can be running")
        EventLoopManager.current = self

        self.waiting[self.mainWaitFor] = []

        for loop in self.separateLoops:
            loop.call_soon(loop.stop)
            loop.run_forever() # Run until awaits are encountered
        self.separateLoops.clear()

        self.running = True
        for thread in self.threads:
            thread.start()

        self.mainLoop = EventLoop()
        asyncio.set_event_loop(self.mainLoop)

    @classmethod
    def handleExceptions(cls):
        with cls.exceptionLock:
            if len(cls.exceptions):
                from . import SceneManager
                from .scenes.runner import ChangeScene
                if isinstance(cls.exceptions[0], ChangeScene):
                    exc = cls.exceptions.pop()
                    cls.exceptions.clear()
                    raise exc
                elif config.exitOnError:
                    Logger.LogLine(Logger.ERROR,
                                   f"Exception in Scene: {SceneManager.CurrentScene().name!r}")
                    exc = cls.exceptions.pop()
                    cls.exceptions.clear()
                    raise exc
                else:
                    for exception in cls.exceptions:
                        Logger.LogLine(Logger.ERROR,
                                       f"Exception ignored in Scene: {SceneManager.CurrentScene().name!r}")
                        Logger.LogException(exception)
                    cls.exceptions.clear()

    def updateEvents(self):
        with EventLoopManager.waitingLock:
            for waiter in self.waiting[self.mainWaitFor]:
                waiter.loop.call_soon_threadsafe(waiter.event.set)

        for func in self.updates:
            func(self.mainLoop)

        for event in self.pending:
            event.trigger()
        self.pending.clear()

    def update(self):
        EventLoopManager.handleExceptions()
        self.updateEvents()
        self.mainLoop.call_soon(self.mainLoop.stop)
        self.mainLoop.run_forever()

    def quit(self):
        self.running = False
        for thread in self.threads:
            thread.join() # Will wait until this iteration has finished

        self.threads = []
        self.loops = []
        self.separateLoops = []
        self.waiting = {}
        self.pending = []
        self.updates = []
        self.mainLoop = None

        EventLoopManager.current = None

class EventLoop(asyncio.SelectorEventLoop):
    def __init__(self, selector=None):
        super(EventLoop, self).__init__(selector)
        self.set_exception_handler(EventLoop.handleException)

        if sys.platform != "win32":
            # SelectorEventLoop defines add_signal_handler
            signals = (signal.SIGTERM, signal.SIGINT)
            for s in signals:
                self.add_signal_handler(
                    s, lambda sig=s: asyncio.create_task(self.shutdown(sig)))

    async def shutdown(self, signal=None):
        if signal is not None:
            Logger.LogLine(Logger.INFO, f"Received exit signal {signal.name}")
        tasks = [t for t in asyncio.all_tasks(self) if t is not
                 asyncio.current_task()]
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        self.stop()

    def handleException(self, context):
        if "exception" in context:
            with EventLoopManager.exceptionLock:
                EventLoopManager.exceptions.append(context["exception"])

def StartCoroutine(coro):
    loop = asyncio.get_running_loop()
    if not isinstance(loop, EventLoop):
        Logger.LogLine(Logger.ERROR,
                       f"Expected loop of type EventLoop, got {type(loop).__name__}")
    loop.create_task(coro)

class WaitFor:
    pass

class WaitForSeconds(WaitFor):
    def __init__(self, length):
        self.length = length

    def __await__(self):
        start = time.perf_counter()
        sleep = asyncio.sleep(self.length)
        yield from sleep.__await__()
        return time.perf_counter() - start

class WaitForEventLoop(WaitFor):
    def __init__(self):
        self.event = asyncio.Event()
        self.loop = asyncio.get_running_loop()
        with EventLoopManager.waitingLock:
            EventLoopManager.current.waiting[type(self)].append(self)

    def __await__(self):
        start = time.perf_counter()
        yield from self.event.wait().__await__()
        with EventLoopManager.waitingLock:
            EventLoopManager.current.waiting[type(self)].remove(self)
        return time.perf_counter() - start

class WaitForUpdate(WaitForEventLoop):
    pass

class WaitForFixedUpdate(WaitForEventLoop):
    pass

class WaitForRender(WaitForEventLoop):
    pass
