## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

from . import Loader, SceneManager, examples
from .errors import PyUnityException
from .info import printInfo
import os
import argparse

parser = argparse.ArgumentParser(description="Load PyUnity examples, PyUnity projects or display information about the PyUnity installation")
parser.add_argument("-v", "--version", action="store_true",
                    help="Display information about the PyUnity installation")
parser.add_argument("project", nargs="?", default="0",
                    help="Project or example number to load")

def main():
    args = parser.parse_args()
    if args.version:
        printInfo()
    elif args.project.isdecimal():
        examples.show()
    elif os.path.isdir(args.project):
        project = Loader.LoadProject(args.project)
        SceneManager.LoadSceneByIndex(project.firstScene)
    else:
        raise PyUnityException(f"invalid project: {args.project}")

if __name__ == "__main__":
    main()
