from .base import BaseCommand, ExitCommand, HelpCommand
from ..menu import CommandMenu, CommandStop
from colorama import Fore, Style

class ListCommand(BaseCommand):
    name = "list"
    description = "List GameObjects according to certain filters."
    flags = [
        (("-n", "--name"), "List GameObjects according to their name", 1),
        (("-t", "--tag"), "List GameObjects according to their tag number", 1),
        (("-l", "--long"), "Display extra information"),
        (("-r", "--recursive"), "Display all GameObjects, not just root GameObjects")
    ]

    def run(self, ctx, args):
        if args.recursive:
            objects = ctx.scene.gameObjects
        else:
            objects = ctx.scene.rootGameObjects

        if not len(objects):
            print("Scene is empty")
            return

        if args.name is not None:
            objects = [o for o in objects if o.name == args.name]
        if args.tag is not None:
            try:
                num = int(args.tag)
            except ValueError:
                raise CommandStop(f"Invalid integer: {args.scene!r}")
            objects = [o for o in objects if o.tag.tag == num]

        if not len(objects):
            print("No matching GameObjects")
            return

        for object in objects:
            if not args.long:
                print(object.transform.FullPath())
            else:
                print("Path:", object.transform.FullPath())
                print("ID:", ctx.project._ids[object])
                print("Components:", [type(x).__name__ for x in object.components])
                print("Children:", [x.gameObject.name for x in object.transform.children])
                print()

class SceneMenu(CommandMenu):
    name = "Scene"
    cmds = {
        "help": HelpCommand,
        "exit": ExitCommand,
        "list": ListCommand,
    }

    def prompt(self, ctx):
        return " ".join([
            f"{Style.BRIGHT}{Fore.BLUE}{self.name}{Style.RESET_ALL}",
            f"{Fore.BLUE}({Fore.GREEN}{ctx.project.name}{Fore.BLUE})",
            f"({Fore.RED}Scene {ctx.scene.name!r}{Fore.BLUE})",
            f"{Style.RESET_ALL}%> "
        ])

    def run(self, ctx):
        assert ctx.scene is not None
        super().run(ctx)

    def quit(self, ctx):
        ctx.scene = None
