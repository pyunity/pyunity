"""
Utility functions to log output of PyUnity.

This will be imported as ``pyunity.Logger``.

"""

__all__ = ["ResetStream", "LogException", "LogTraceback", "LogSpecial",
           "SetStream", "Log", "LogLine", "Save", "Level", "Special"]

import os
import sys
import platform
import traceback
import re
import atexit
from time import strftime, time

def getTmp():
    if os.getenv("ANDROID_DATA") == "/data" and os.getenv("ANDROID_ROOT") == "/system":
        pattern = re.compile(r"/data/(data|user/\d+)/(.+)/files")
        for path in sys.path:
            if pattern.match(path):
                result = path.split("/files")[0]
                break
        else:
            raise OSError("Cannot find path to android app folder")
        folder = os.path.join(result, "files", "pyunity", "logs")
    elif platform.platform().startswith("Windows"):
        folder = os.path.join(os.environ["appdata"], "PyUnity", "Logs")
    else:
        folder = os.path.join("/tmp", "pyunity", "logs")
    return folder

folder = getTmp()
if not os.path.isdir(folder):
    os.makedirs(folder, exist_ok=True)

stream = sys.stdout
timestamp = strftime("%Y-%m-%d %H-%M-%S")
start = time()

with open(os.path.join(folder, "latest.log"), "w+") as f:
    f.write("Timestamp |(O)utput / (I)nfo / (D)ebug / (E)rror / (W)arning| Message\n")
    f.write(strftime("%Y-%m-%d %H:%M:%S") + " |I| Started logger\n")

class Level:
    """
    Represents a level or severity to log. You
    should never instantiate this directly, instead
    use one of `Logging.OUTPUT`, `Logging.INFO`,
    `Logging.DEBUG`, `Logging.ERROR` or
    `Logging.WARN`.

    """

    def __init__(self, abbr):
        self.abbr = abbr

    def __eq__(self, other):
        if isinstance(other, Level):
            return self.abbr == other.abbr
        return False

OUTPUT = Level("O")
INFO = Level("I")
DEBUG = Level("D")
ERROR = Level("E")
WARN = Level("W")

class Special:
    """
    Class to represent a special line to log.
    You should never instantiate this class,
    instead use one of `Logger.RUNNING_TIME`.

    """

    def __init__(self, name, func):
        self.name = name
        self.func = func

class Elapsed:
    def __init__(self):
        self.time = time()

    def tick(self):
        old = self.time
        self.time = time()
        return self.time - old

elapsed = Elapsed()
RUNNING_TIME = Special("RUNNING_TIME", lambda: str(time() - start))
ELAPSED_TIME = Special("ELAPSED_TIME", lambda: str(elapsed.tick()))

def Log(*message):
    """
    Logs a message with level OUTPUT.

    """
    LogLine(OUTPUT, *message)

def LogLine(level, *message, silent=False):
    """
    Logs a line in `latest.log` found in these two locations:
    Windows: ``%appdata%\\PyUnity\\Logs\\latest.log``
    Other: ``/tmp/pyunity/logs/latest.log``

    Parameters
    ----------
    level : Level
        Level or severity of log.

    """
    time = strftime("%Y-%m-%d %H:%M:%S")
    msg = " ".join(map(lambda a: str(a).rstrip(), message))
    if level == WARN:
        msg = "Warning: " + msg
    if msg.count("\n") > 0:
        for line in msg.split("\n"):
            if not line.isspace():
                LogLine(level, line, silent=silent)
        return time, msg
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
            else:
                stream.write(msg + "\n")
    with open(os.path.join(folder, "latest.log"), "a") as f:
        f.write(f"{time} |{level.abbr}| {msg}\n")
    return time, msg

def LogException(e, silent=False):
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
                LogLine(ERROR, line2, silent=silent)

def LogTraceback(exctype, value, tb):
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
                LogLine(ERROR, line2)

sys.excepthook = LogTraceback

def LogSpecial(level, type):
    """
    Log a line of level `level` with a
    special line that is generated at
    runtime.

    Parameters
    ----------
    level : Level
        Level of log
    type : Special
        The special line to log

    """
    LogLine(level, "(" + type.name + ")", type.func())

@atexit.register
def Save():
    """
    Saves a new log file with a timestamp
    of initializing PyUnity for the first time.

    """
    LogLine(INFO, "Saving new log at",
            os.path.join(folder, timestamp + ".log"))

    with open(os.path.join(folder, "latest.log")) as f:
        with open(os.path.join(folder, timestamp + ".log"), "w+") as f2:
            f2.write(f.read())

    # Upload to ftp
    try:
        import urllib.request
        url = "https://ftp.pyunity.repl.co/upload?confirm=1"
        with urllib.request.urlopen(url):
            pass
    except Exception as e:
        LogException(e, silent=True)

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
