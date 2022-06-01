from ..menu import CommandMenu, CommandStop
from ..locale import locale
from .base import BaseCommand, ExitCommand, HelpCommand
from colorama import Fore, Style
from pyunity import SceneManager, Behaviour

class SaveCommand(BaseCommand):
    name = locale.commands.scene.save.name
    description = locale.commands.scene.save.description

    def run(self, ctx, args):
        ctx.project.ImportAsset(ctx.scene)

class RunCommand(BaseCommand):
    name = locale.commands.scene.run.name
    description = locale.commands.scene.run.description

    def run(self, ctx, args):
        SceneManager.LoadScene(ctx.scene)

class ListCommand(BaseCommand):
    name = locale.commands.scene.list.name
    description = locale.commands.scene.list.description
    flags = [
        (("-n", "--name"), locale.commands.scene.list.namearg, 1),
        (("-t", "--tag"), locale.commands.scene.list.tag, 1),
        (("-l", "--long"), locale.commands.scene.list.long),
        (("-r", "--recursive"), locale.commands.scene.list.recursive)
    ]
    positionals = [
        ("parent", locale.commands.scene.list.parent)
    ]

    def run(self, ctx, args):
        if hasattr(args, "parent"):
            if args.parent not in ctx.project._idMap:
                raise CommandStop(f"{args.parent}: {locale.commands.scene.list.noid}")

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
            print(locale.commands.scene.list.empty)
            return

        if args.name is not None:
            objects = [o for o in objects if o.name == args.name]
        if args.tag is not None:
            try:
                num = int(args.tag)
            except ValueError:
                raise CommandStop(f"{locale.commands.scene.list.noint}: {args.scene!r}")
            objects = [o for o in objects if o.tag.tag == num]

        if not len(objects):
            print(locale.commands.scene.list.noobj)
            return

        for object in objects:
            if not args.long:
                print(ctx.project._ids[object] + "\t" + object.transform.FullPath())
            else:
                components = [type(x).__name__ for x in object.components]
                children = [x.gameObject.name for x in object.transform.children]
                print(f"{locale.commands.scene.list.path}:", object.transform.FullPath())
                print(f"{locale.commands.scene.list.id}:", ctx.project._ids[object])
                print(f"{locale.commands.scene.list.components}:", components)
                print(f"{locale.commands.scene.list.children}:", children)
                print()

class SelectCommand(BaseCommand):
    name = locale.commands.scene.select.name
    description = locale.commands.scene.select.description
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
