from argparse import SUPPRESS, ArgumentParser
from ..menu import ExitMenu
from ..locale import locale

def index(l, items):
    for item in items:
        if item in l:
            return l.index(item)
    return -1

class BaseCommand:
    name = locale.commands.base.name
    description = locale.commands.base.description
    flags = []
    positionals = []

    def __init__(self, menu):
        self.menu = menu
        self.parser = ArgumentParser(
            prog=self.name,
            description=self.description,
            exit_on_error=False,
            add_help=False)
        self.parser.add_argument("-h", "--help", help=locale.commands.base.help,
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
    name = locale.commands.help.name
    description = locale.commands.help.description

    positionals = [
        ("cmd", locale.commands.help.cmd)
    ]

    def run(self, ctx, args):
        if hasattr(args, "cmd"):
            if args.cmd not in ctx.menu.commands:
                print(f"{args.cmd}: {locale.notfound}")
                return
            ctx.menu.commands[args.cmd].parser.print_help()
            print()
            return
        else:
            cmds = list(ctx.menu.commands)

        for cmd in cmds:
            cmdobj = ctx.menu.commands[cmd]
            print(locale.commands.help.title.format(cmd=cmd))
            cmdobj.parser.print_usage()
            print(cmdobj.parser.description)
            print()

class ExitCommand(BaseCommand):
    name = locale.commands.exit.name
    description = locale.commands.exit.description

    def run(self, ctx, args):
        raise ExitMenu
