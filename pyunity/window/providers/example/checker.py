# Default imports, do not modify
# Keep all other imports inside check function
from pyunity.errors import *
from pyunity.window.providers import checkModule

# Modify the below variables and function

name = "example"
prio = -1

def check():
    raise PyUnityException("Example window provider cannot be loaded")
