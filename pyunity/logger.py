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

from pathlib import Path
import io
import os
import re
import sys
import time
import atexit
import inspect
import platform
import threading
import traceback

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

def getDataFolder():
    if os.getenv("ANDROID_DATA") == "/data" and os.getenv("ANDROID_ROOT") == "/system":
        # Android (p4a, termux etc)
        pattern = re.compile(r"/data/(data|user/\d+)/(.+)/files")
        for path in sys.path:
            if pattern.match(path):
                result = path.split("/files")[0]
                break
        else:
            raise OSError("Cannot find path to android app folder")
        folder = Path(result) / "files/usr/local/pyunity"
    elif platform.system().startswith("Windows"):
        # Windows
        folder = Path(os.environ["appdata"]) / "PyUnity"
    elif platform.system().startswith("Darwin"):
        # MacOS
        folder = Path.home() / "Library/Application Support/PyUnity"
    else:
        # Linux
        folder = Path("/tmp/pyunity")
    return folder

folder = getDataFolder() / "Logs"
if not folder.is_dir():
    folder.mkdir(parents=True, exist_ok=True)

stream = sys.stdout
timestamp = time.strftime(TIME_FORMAT.replace(":", "-")) # No : allowed in path
start = time.perf_counter()

with open(folder / "latest.log", "w+") as f:
    f.write("YYYY-MM-DD HH:MM:SS Module:Line |(O)utput / (I)nfo / (D)ebug / (E)rror / (W)arning| Message\n")
    lineno = inspect.getframeinfo(inspect.currentframe()).lineno
    f.write(time.strftime(TIME_FORMAT) + f" {__name__}:{lineno + 1} |I| Started logger\n")

class Level:
    """
    Represents a level or severity to log. You
    should never instantiate this directly, instead
    use one of ``Logging.OUTPUT``, ``Logging.INFO``,
    ``Logging.DEBUG``, ``Logging.ERROR`` or
    ``Logging.WARN``.

    """

    def __init__(self, abbr):
        self.abbr = abbr

    def __eq__(self, other):
        if isinstance(other, Level):
            return self.abbr == other.abbr
        return False

    def __hash__(self):
        return hash(self.abbr)

OUTPUT = Level("O")
INFO = Level("I")
DEBUG = Level("D")
ERROR = Level("E")
WARN = Level("W")

class Special:
    """
    Class to represent a special line to log.
    You should never instantiate this class,
    instead use one of ``Logger.RUNNING_TIME``
    or ``Logger.ELAPSED_TIME``.

    """

    def __init__(self, name, func):
        self.name = name
        self.func = func

class Elapsed:
    def __init__(self):
        self.time = time.time()

    def tick(self):
        old = self.time
        self.time = time.time()
        return self.time - old

elapsed = Elapsed()
RUNNING_TIME = Special("RUNNING_TIME", lambda: str(time.perf_counter() - start))
ELAPSED_TIME = Special("ELAPSED_TIME", lambda: str(elapsed.tick()))

def Log(*message, stacklevel=1):
    """
    Logs a message with level OUTPUT.

    """
    LogLine(OUTPUT, *message, stacklevel=stacklevel + 1)

def LogLine(level, *message, stacklevel=1, silent=False):
    """
    Logs a line in ``latest.log`` found in these two locations:
    Windows: ``%appdata%\\PyUnity\\Logs\\latest.log``
    Other: ``/tmp/pyunity/logs/latest.log``

    Parameters
    ----------
    level : Level
        Level or severity of log.

    """
    try:
        stack = inspect.stack()
        if len(stack) <= stacklevel:
            module = "sys"
            lineno = 1
        else:
            frameinfo = inspect.stack()[stacklevel]
            module = frameinfo.frame.f_globals.get("__name__", "<string>")
            lineno = frameinfo.lineno
    except ValueError:
        # call stack is not deep enough
        module = "sys"
        lineno = 1
    location = f"{module}:{lineno}"

    stamp = time.strftime(TIME_FORMAT)
    msg = " ".join(str(a).rstrip() for a in message)
    if level == WARN:
        msg = f"Warning: " + msg
    if msg.count("\n") > 0:
        for line in msg.split("\n"):
            if not line.isspace():
                LogLine(level, line, stacklevel=stacklevel + 1, silent=silent)
        return stamp, msg
    if not silent:
        output = False
        if level == DEBUG:
            if os.environ["PYUNITY_DEBUG_MODE"] != "0":
                output = True
        elif level != INFO:
            output = True
        if output:
            if level == ERROR:
                sys.stderr.write(msg + "\n")
            elif stream is not None:
                stream.write(msg + "\n")
    with open(folder / "latest.log", "a") as f:
        f.write(f"{stamp} {location} |{level.abbr}| {msg}\n")
    return stamp, msg

def LogException(e, stacklevel=1, silent=False):
    """
    Log an exception.

    Parameters
    ----------
    e : Exception
        Exception to log

    """
    exception = traceback.format_exception(type(e), e, e.__traceback__)
    for line in exception:
        for line2 in line.split("\n"):
            if line2:
                LogLine(ERROR, line2, stacklevel=stacklevel + 1, silent=silent)

def LogTraceback(exctype, value, tb, stacklevel=1):
    """
    Log an exception.

    Parameters
    ----------
    exctype : type
        Type of exception that is to be raised
    value : Any
        Value of the exception contents
    tb : traceback
        Traceback object to log

    Notes
    -----
    This function is not meant to be used by general users.

    """
    exception = traceback.format_exception(exctype, value, tb)
    for line in exception:
        for line2 in line.split("\n"):
            if line2:
                LogLine(ERROR, line2, stacklevel=stacklevel + 1)

sys.excepthook = LogTraceback

def LogSpecial(level, type, stacklevel=1):
    """
    Log a line of level ``level`` with a
    special line that is generated at
    runtime.

    Parameters
    ----------
    level : Level
        Level of log
    type : Special
        The special line to log

    """
    LogLine(level, "(" + type.name + ")", type.func(), stacklevel=stacklevel + 1)

@atexit.register
def Save():
    """
    Saves a new log file with a timestamp
    of initializing PyUnity for the first time.

    """
    LogLine(INFO, "Saving new log at", folder / (timestamp + ".log"))

    with open(folder / "latest.log") as f:
        with open(folder / (timestamp + ".log"), "w+") as f2:
            f2.write(f.read())

class TempRedirect:
    def __init__(self, *, silent=False):
        self.silent = silent
        self.stream = None

    def get(self):
        if self.stream is None:
            raise Exception("Context manager not used")
        return self.stream.getvalue()

    def __enter__(self):
        global stream
        self.stream = io.StringIO()
        if self.silent:
            stream = self.stream
        else:
            SetStream(self.stream)
        return self

    def __exit__(self, exctype, value, tb):
        global stream
        if self.silent:
            stream = sys.stdout
        else:
            ResetStream()

def SetStream(s):
    global stream
    stream = s
    stream.write(f"Changed stream to {s}\n")
    LogLine(INFO, f"Changed stream to {s}")

def ResetStream():
    global stream
    stream = sys.stdout
    stream.write("Changed stream back to stdout\n")
    LogLine(INFO, "Changed stream back to stdout")
