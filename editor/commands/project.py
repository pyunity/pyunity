from ..menu import CommandStop, ExitMenu, CommandMenu
from .scene import SceneMenu
from .base import BaseCommand, ExitCommand
from pyunity import SceneManager, Loader
import os

class OpenCommand(BaseCommand):
    name = "open"
    description = "Opens a scene."
    flags = [
        (("-n", "--num"), "specify scene by index not name")
    ]
    positionals = [
        ("scene", "either scene name or scene index (see --num)")
    ]

    def run(self, ctx, args):
        idx = False
        if args.num:
            idx = True

            if not hasattr(args, "scene"):
                raise CommandStop("Please provide a scene index.")
        elif not hasattr(args, "scene"):
            raise CommandStop("Please provide a scene name.")

        if idx:
            try:
                item = int(args.scene)
            except ValueError:
                raise CommandStop(f"Invalid integer: {args.scene!r}")
            scene = SceneManager.GetSceneByIndex(item)
        else:
            scene = SceneManager.GetSceneByName(args.scene)
        ctx.scene = scene
        print(f"Loaded scene {scene.name!r}")
        raise ExitMenu(SceneMenu)

class ProjectMenu(CommandMenu):
    cmds = {
        "exit": ExitCommand,
        "open": OpenCommand
    }

class NewProjectMenu(ProjectMenu):
    def run(self, ctx):
        SceneManager.RemoveAllScenes()
        SceneManager.AddScene("Scene")
        ctx.project = Loader.GenerateProject(os.environ["PROJECT_PATH"])
        super().run(ctx)

class OpenProjectMenu(ProjectMenu):
    def run(self, ctx):
        ctx.project = Loader.LoadProject(os.environ["PROJECT_PATH"])
        super().run(ctx)
