import os
import platform
import shutil
from time import strftime

if platform.platform().startswith("Windows"):
    folder = os.path.join(os.getenv("appdata"), "pyunity", "logs")
else:
    folder = os.path.join("/tmp", "pyunity", "logs")
if not os.path.isdir(folder):
    os.makedirs(folder, exist_ok=True)

timestamp = strftime("%Y-%m-%d %H-%M-%S")

with open(os.path.join(folder, "latest.log"), "w+") as f:
    f.write("Timestamp |(I)nfo / (D)ebug / (E)rror / (W)arning| Message\n")
    f.write(strftime("%Y-%m-%d %H:%M:%S") + " |I| Started logger\n")

class Level:
    """
    Represents a level or severity to log. You
    should never instantiate this directly, instead
    use one of `Logging.INFO`, `Logging.DEBUG`,
    `Logging.ERROR` or `Logging.WARNING`.

    """
    
    def __init__(self, abbr, name):
        self.abbr = abbr
        self.name = name


INFO = Level("I", None)
DEBUG = Level("D", "")
ERROR = Level("E", None)
WARNING = Level("W", "Warning: ")

def LogLine(level, *message):
    """
    Logs a line in `latest.log` found in these two locations:
    Windows: ``%appdata%\\pyunity\\logs\\latest.log``
    Other: ``/tmp/pyunity/logs/latest.log``

    Parameters
    ----------
    level : Level
        Level or severity of log.
    
    """
    msg = (level.name if level.name is not None else "") + " ".join(message)
    if os.environ["PYUNITY_DEBUG_MODE"] == "1":
        if level.name is not None:
            print(level.name + msg)
    with open(os.path.join(folder, "latest.log"), "w+") as f:
        f.write(strftime("%Y-%m-%d %H:%M:%S") + f" |{level.abbr}| {msg}\n")
