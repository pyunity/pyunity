from .menu import CommandMenu, ExitMenu, CommandStop
from pyunity import SceneManager, Loader
import sys

def index(l, items):
    for item in items:
        if item in l:
            return l.index(item)
    return -1

class BaseCommand:
    def __init__(self, menu):
        self.menu = menu

    def run(self, ctx, args):
        pass

class ExitCommand(BaseCommand):
    def run(self, ctx, args):
        raise ExitMenu

class OpenCommand(BaseCommand):
    def run(self, ctx, args):
        if "-h" in args or "--help" in args:
            print("usage: open [-h/--help] [-n/--num] SCENE")
            print()
            print("Opens a scene.")
            print()
            print("options:")
            print(" -h, --help   show this help message and exit")
            print(" -n, --num    specify scene by index not name")
            print(" SCENE        either scene name or scene index (see --num)")
            raise CommandStop

        idx = False
        if "-n" in args or "--num" in args:
            args.pop(index(args, ["-n", "--num"]))
            idx = True

            if not len(args):
                raise CommandStop("Please provide a scene index.")
        elif not len(args):
            raise CommandStop("Please provide a scene name.")

        if idx:
            try:
                item = int(args[0])
            except ValueError:
                raise CommandStop(f"Invalid integer: {args[0]!r}")
            scene = SceneManager.LoadSceneByIndex(item)
        else:
            scene = SceneManager.LoadSceneByName(args[0])
        ctx.scene = scene
        print(f"Loaded scene {scene.name!r}")

class BaseMenu(CommandMenu):
    cmds = {
        "exit": ExitCommand,
        "open": OpenCommand
    }

    def run(self, ctx):
        ctx.project = Loader.LoadProject(sys.argv[1])
        super().run(ctx)
