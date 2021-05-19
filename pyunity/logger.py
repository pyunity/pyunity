"""
Utility functions to log output of PyUnity.

This will be imported as ``pyunity.Logger``.

"""

import os
import platform
import shutil
import importlib
import traceback
from time import strftime

if platform.platform().startswith("Windows"):
    folder = os.path.join(os.getenv("appdata"), "PyUnity", "Logs")
else:
    folder = os.path.join("/tmp", "pyunity", "logs")
if not os.path.isdir(folder):
    os.makedirs(folder, exist_ok=True)

timestamp = strftime("%Y-%m-%d %H-%M-%S")

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

    def __init__(self, abbr, name):
        self.abbr = abbr
        self.name = name


OUTPUT = Level("O", "")
INFO = Level("I", None)
DEBUG = Level("D", "")
ERROR = Level("E", "")
WARN = Level("W", "Warning: ")

def Log(*message):
    """
    Logs a message with level OUTPUT.

    """
    LogLine(OUTPUT, *message)

def LogLine(level, *message):
    """
    Logs a line in `latest.log` found in these two locations:
    Windows: ``%appdata%\\PyUnity\\Logs\\latest.log``
    Other: ``/tmp/pyunity/logs/latest.log``

    Parameters
    ----------
    level : Level
        Level or severity of log.

    """
    msg = (level.name if level.name is not None else "") + " ".join(map(str, message))
    if os.environ["PYUNITY_DEBUG_MODE"] == "1":
        if level.name is not None:
            print(level.name + msg)
    with open(os.path.join(folder, "latest.log"), "a") as f:
        f.write(strftime("%Y-%m-%d %H:%M:%S") + f" |{level.abbr}| {msg}\n")

def LogException(e):
    exception = traceback.format_exception(type(e), e, e.__traceback__)
    for line in exception:
        for line2 in line.split("\n"):
            if line2:
                LogLine(ERROR, line2)

def Save():
    """
    Saves a new log file with a timestamp
    of initializing PyUnity for the first time.

    """
    LogLine(INFO, "Saving new log at", os.path.join(folder, timestamp + ".log"))

    with open(os.path.join(folder, "latest.log")) as f:
        with open(os.path.join(folder, timestamp + ".log"), "w+") as f2:
            f2.write(f.read())