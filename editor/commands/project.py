from ..menu import CommandStop, ExitMenu, CommandMenu
from ..locale import locale
from .scene import SceneMenu
from .base import BaseCommand, ExitCommand, HelpCommand
from pyunity import SceneManager, Loader
import os

class OpenCommand(BaseCommand):
    name = locale.commands.project.open.name
    description = locale.commands.project.open.description
    flags = [
        (("-n", "--num"), locale.commands.project.open.num)
    ]
    positionals = [
        ("scene", locale.commands.project.open.scene)
    ]

    def run(self, ctx, args):
        idx = False
        if args.num:
            idx = True

            if not hasattr(args, "scene"):
                raise CommandStop(locale.commands.project.open.noindex)
        elif not hasattr(args, "scene"):
            raise CommandStop(locale.commands.project.open.noname)

        if idx:
            try:
                item = int(args.scene)
            except ValueError:
                raise CommandStop(f"{locale.commands.noint}: {args.scene!r}")
            scene = SceneManager.GetSceneByIndex(item)
        else:
            scene = SceneManager.GetSceneByName(args.scene)
        ctx.scene = scene
        print(locale.commands.project.open.loaded.format(name=repr(scene.name)))
        raise ExitMenu(SceneMenu)

class ListCommand(BaseCommand):
    name = locale.commands.project.list.name
    description = locale.commands.project.list.description

    def run(self, ctx, args):
        for i, scene in enumerate(SceneManager.scenesByIndex):
            print(f"{i}\t{scene.name!r}")

class ProjectMenu(CommandMenu):
    name = locale.menu.project.name
    cmds = {
        "help": HelpCommand,
        "exit": ExitCommand,
        "open": OpenCommand,
        "list": ListCommand,
    }

class NewProjectMenu(ProjectMenu):
    def run(self, ctx):
        SceneManager.RemoveAllScenes()
        SceneManager.AddScene(locale.defaultscene)
        ctx.project = Loader.GenerateProject(os.environ["PROJECT_PATH"])
        super().run(ctx)

class OpenProjectMenu(ProjectMenu):
    def run(self, ctx):
        ctx.project = Loader.LoadProject(os.environ["PROJECT_PATH"])
        super().run(ctx)
