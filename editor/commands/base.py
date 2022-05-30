from argparse import SUPPRESS, ArgumentParser
from ..menu import ExitMenu

def index(l, items):
    for item in items:
        if item in l:
            return l.index(item)
    return -1

class BaseCommand:
    name = "BaseCommand"
    description = "Base command to inherit from."
    flags = []
    positionals = []

    def __init__(self, menu):
        self.menu = menu
        self.parser = ArgumentParser(
            prog=self.name,
            description=self.description,
            exit_on_error=False,
            add_help=False)
        self.parser.add_argument("-h", "--help", help="show this help message and exit",
                                 action="store_true")

        for flag in self.flags:
            if len(flag) > 2:
                action = "store"
            else:
                action = "store_true"
            self.parser.add_argument(*flag[0], help=flag[1], action=action)
        for arg in self.positionals:
            self.parser.add_argument(arg[0], help=arg[1], nargs="?", default=SUPPRESS)

    def run(self, ctx, args):
        pass

class HelpCommand(BaseCommand):
    name = "help"
    description = "Gets help with a command."

    positionals = [
        ("cmd", "")
    ]

    def run(self, ctx, args):
        if hasattr(args, "cmd"):
            if args.cmd not in ctx.menu.commands:
                print(f"{args.cmd}: command not found")
                return
            ctx.menu.commands[args.cmd].parser.print_help()
            print()
            return
        else:
            cmds = list(ctx.menu.commands)

        for cmd in cmds:
            cmdobj = ctx.menu.commands[cmd]
            print(f"Help on command {cmd}:")
            cmdobj.parser.print_usage()
            print(cmdobj.parser.description)
            print()

class ExitCommand(BaseCommand):
    name = "exit"
    description = "Exits the current menu."

    def run(self, ctx, args):
        raise ExitMenu
