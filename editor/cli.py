from pathlib import Path
from .locale import locale
from .menu import Runner
import argparse
import os

parser = argparse.ArgumentParser(
    prog="editor",
    description=locale.cli.description)

parser.add_argument("-n", "--new", action="store_true", help=locale.cli.new)
parser.add_argument("path", help=locale.cli.path)

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
