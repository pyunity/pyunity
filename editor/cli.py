from pathlib import Path
from .menu import Runner
import argparse
import os

parser = argparse.ArgumentParser(
    prog="editor",
    description="Open a PyUnity project in the command-line editor")

parser.add_argument("-n", "--new", action="store_true", help="create a new project")
parser.add_argument("path", help="path to project")

def main():
    args = parser.parse_args()

    from .commands.project import NewProjectMenu, OpenProjectMenu
    if args.new:
        initial = NewProjectMenu
    else:
        initial = OpenProjectMenu

    os.environ["PROJECT_PATH"] = str(Path(args.path).absolute())
    runner = Runner()
    runner.run(initial)

if __name__ == "__main__":
    main()
