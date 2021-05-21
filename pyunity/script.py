from types import ModuleType
from .core import Component
from types import ModuleType
import glob
import os

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
    for line in text:
        print(line)
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
    files = glob.glob(os.path.join(path, "*.py"))
    behaviours = {}
    for file in files:
        print(files)
        with open(file) as f:
            text = f.read().rstrip().splitlines()

        name = os.path.basename(file[:-3])
        if CheckScript(text):
            a = exec("\n".join(text), {})
            print(type(a))
            behaviours[name] = eval(name)

    return behaviours
