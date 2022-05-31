from .base import BaseCommand, ExitCommand, HelpCommand
from ..menu import CommandMenu, CommandStop
from colorama import Fore, Style
from pyunity import SceneManager, Behaviour

class SaveCommand(BaseCommand):
    name = "save"
    description = "Save the opened Scene."

    def run(self, ctx, args):
        ctx.project.ImportAsset(ctx.scene)

class RunCommand(BaseCommand):
    name = "run"
    description = "Run the opened Scene."

    def run(self, ctx, args):
        SceneManager.LoadScene(ctx.scene)

class ListCommand(BaseCommand):
    name = "list"
    description = "List GameObjects according to certain filters."
    flags = [
        (("-n", "--name"), "List GameObjects according to their name", 1),
        (("-t", "--tag"), "List GameObjects according to their tag number", 1),
        (("-l", "--long"), "Display extra information"),
        (("-r", "--recursive"), "Display all GameObjects, not just root GameObjects")
    ]
    positionals = [
        ("parent", "ID of GameObject to list children")
    ]

    def run(self, ctx, args):
        if hasattr(args, "parent"):
            if args.parent not in ctx.project._idMap:
                raise CommandStop(f"{args.parent}: ID not in scene")

            objects = []
            if args.recursive:
                transforms = ctx.project._idMap[args.parent].transform.GetDescendants()
            else:
                transforms = ctx.project._idMap[args.parent].transform.children

            for transform in transforms:
                objects.append(transform.gameObject)
        else:
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
                print(ctx.project._ids[object] + "\t" + object.transform.FullPath())
            else:
                print("Path:", object.transform.FullPath())
                print("ID:", ctx.project._ids[object])
                print("Components:", [type(x).__name__ for x in object.components])
                print("Children:", [x.gameObject.name for x in object.transform.children])
                print()

class SelectCommand(BaseCommand):
    name = "select"
    description = "Selects a GameObject for further operations, or get the current selected."
    positionals = [
        ("id", "ID of the GameObject to select (optional)")
    ]

    def run(self, ctx, args):
        if hasattr(args, "id"):
            if args.id not in ctx.project._idMap:
                raise CommandStop(f"{args.id}: ID not in scene")

            if ctx.gameObject is not None:
                lastId = ctx.project._ids[ctx.gameObject]
                lastPath = ctx.gameObject.transform.FullPath()
                print(f"Previously selected GameObject: {lastId} ({lastPath})")

            ctx.gameObject = ctx.project._idMap[args.id]
            path = ctx.gameObject.transform.FullPath()
            print(f"Selected GameObject {args.id} ({path})")
        else:
            if ctx.gameObject is not None:
                lastId = ctx.project._ids[ctx.gameObject]
                lastPath = ctx.gameObject.transform.FullPath()
                print(f"Selected GameObject: {lastId} ({lastPath})")
            else:
                print("No selected GameObject")

class ComponentCommand(BaseCommand):
    name = "cpnt"
    description = "Get information about or modify the selected GameObject's components"

    flags = [
        (("-l", "--list"), "List components on the selected GameObject"),
        (("-i", "--info"), "List attributes on a specific Component by index", 1),
    ]

    def run(self, ctx, args):
        if ctx.gameObject is None:
            raise CommandStop("No GameObject selected")

        names = ["list", "info"]
        cmd = None
        for name in names:
            if getattr(args, name, False):
                if cmd is not None:
                    raise CommandStop("Expected one of --list, --info")
                cmd = name

        if cmd is None:
            raise CommandStop("Expected one of --list, --info")

        if cmd == "list":
            indexLength = len(str(len(ctx.gameObject.components)))
            for i, component in enumerate(ctx.gameObject.components):
                cpntId = ctx.project._ids[component]
                name = type(component).__name__
                if isinstance(component, Behaviour):
                    name += "(Behaviour)"
                else:
                    name += "(Component)"
                print(f"{str(i).ljust(indexLength)} {cpntId}\t{name}")
        elif cmd == "info":
            try:
                num = int(args.info)
            except ValueError:
                raise CommandStop(f"invalid integer: {args.info!r}")

            if num < 0 or num > len(ctx.gameObject.components) - 1:
                raise CommandStop(f"invalid index: {num}")

            cpnt = ctx.gameObject.components[num]
            typename = type(cpnt).__name__
            if isinstance(cpnt, Behaviour):
                typename += "(Behaviour)"
            else:
                typename += "(Component)"

            print("ID:", ctx.project._ids[cpnt])
            print("Type:", typename)

class SceneMenu(CommandMenu):
    name = "Scene"
    cmds = {
        "help": HelpCommand,
        "exit": ExitCommand,
        "save": SaveCommand,
        "run": RunCommand,
        "list": ListCommand,
        "select": SelectCommand,
        "cpnt": ComponentCommand,
    }

    def prompt(self, ctx):
        if ctx.modified:
            modify = f" {Fore.YELLOW}*"
        else:
            modify = ""

        return " ".join([
            f"{Style.BRIGHT}{Fore.BLUE}{self.name}{Style.RESET_ALL}",
            f"{Fore.BLUE}({Fore.GREEN}{ctx.project.name}{Fore.BLUE})",
            f"({Fore.RED}Scene {ctx.scene.name!r}{modify}{Fore.BLUE})",
            f"{Style.RESET_ALL}%> "
        ])

    def run(self, ctx):
        assert ctx.scene is not None
        ctx.modified = False
        super().run(ctx)

    def quit(self, ctx):
        if ctx.modified:
            if input("Do you want to save your changes? (Y/n) ").lower() != "n":
                ctx.project.ImportAsset(ctx.scene)
        ctx.scene = None
        ctx.gameObject = None
