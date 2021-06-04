"""
Module to manage loading scripts from files.

"""

from .core import Component
from . import Logger
from types import ModuleType
import glob
import os
import sys

class Behaviour(Component):
    """
    Base class for behaviours that can be scripted.

    Attributes
    ----------
    gameObject : GameObject
        GameObject that the component belongs to.
    transform : Transform
        Transform that the component belongs to.

    """

    def Start(self):
        """
        Called every time a scene is loaded up.

        """
        pass

    def Update(self, dt):
        """
        Called every frame.

        Parameters
        ----------
        dt : float
            Time since last frame, sent by the scene 
            that the Behaviour is in.

        """
        pass

def CheckScript(text):
    """
    Check if ``text`` is a valid script for PyUnity.

    Parameters
    ----------
    text : list
        List of lines

    Returns
    -------
    bool
        If script is valid or not.
    
    Notes
    -----
    This function checks each line to see if it matches at
    least one of these criteria:

    1. The line is an ``import`` statement
    #. The line is just whitespace or blank
    #. The line is just a comment preceded by whitespace or nothing
    #. The line is a class definition
    #. The line has an indentation at the beginning

    These checks are essential to ensure no malicious code is run to
    break the PyUnity engine.

    """
    for line in text:
        if line.startswith("import") or \
                (line.startswith("from") and " import " in line):
            continue
        elif line.isspace() or line == "":
            continue
        elif "#" in line:
            if line.split("#")[0].isspace():
                continue
        elif line.startswith("class "):
            continue
        elif line.startswith(" ") or line.startswith("\t"):
            continue
        return False
    return True

def LoadScripts(path):
    """
    Loads all scripts found in ``path``.

    Parameters
    ----------
    path : Pathlike
        A path to a folder containing all the scripts

    Returns
    -------
    ModuleType
        A module that contains all the imported scripts
    
    Notes
    -----
    This function will add a module to ``sys.modules`` that
    is called ``PyUnityScripts``, and can be imported like any
    other module. The module will also have a variable called
    ``__pyunity__`` which shows that it is from PyUnity and not
    a real module. If an existing module named ``PyUnityScripts``
    is present and does not have the ``__pyunity__`` variable set,
    then a warning will be issued and it will be replaced.

    """
    files = glob.glob(os.path.join(path, "*.py"))
    a = {}

    if "PyUnityScripts" in sys.modules and hasattr(sys.modules["PyUnityScripts"], "__pyunity__"):
        module = sys.modules["PyUnityScripts"]
    else:
        if "PyUnityScripts" in sys.modules:
            Logger.LogLine(Logger.WARN, "PyUnityScripts is already a package!")
        module = ModuleType("PyUnityScripts", None)
        module.__pyunity__ = True
        module.__all__ = []
        sys.modules["PyUnityScripts"] = module

    for file in files:
        with open(file) as f:
            text = f.read().rstrip().splitlines()

        name = os.path.basename(file[:-3])
        if CheckScript(text):
            exec("\n".join(text), a)
            setattr(module, name, a[name])
            module.__all__.append(name)

    return module
