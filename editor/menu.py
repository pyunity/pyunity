from .context import CommandContext
from .locale import locale
from colorama import init as colorama_init, Fore, Style
import readline
import traceback
import shlex
import sys
import argparse

colorama_init()
readline.set_auto_history(True)

def error(*msg, sep=" ", end="\n", flush=False):
    print(*msg, sep=sep, end=end, flush=flush, file=sys.stderr)

class MenuFlow(Exception):
    pass

class CommandStop(MenuFlow):
    pass

class ExitMenu(MenuFlow):
    pass

class CommandMenu:
    name = locale.menu.base.name
    cmds = {}

    def __init__(self):
        self.commands = {}
        for name, item in type(self).cmds.items():
            self.commands[name] = item(self)

    def prompt(self, ctx):
        return " ".join([
            f"{Style.BRIGHT}{Fore.BLUE}{self.name}{Style.RESET_ALL}",
            f"{Fore.BLUE}({Fore.GREEN}{ctx.project.name}{Fore.BLUE})",
            f"{Style.RESET_ALL}%> "
        ])

    def run(self, ctx):
        ctx.menu = self
        while True:
            try:
                cmd = input(self.prompt(ctx))
            except KeyboardInterrupt:
                print("^C")
                continue
            except EOFError:
                print("exit")
                self.quit(ctx)
                raise ExitMenu
            args = shlex.split(cmd)
            if len(args) == 0:
                continue
            cmdname = args[0]
            args = args[1:]
            if cmdname not in self.commands:
                error(f"{cmdname}: {locale.notfound}")
                continue

            command = self.commands[cmdname]

            try:
                args, unknown = command.parser.parse_known_args(args)
            except argparse.ArgumentError as e:
                command.parser.print_usage()
                error(f"{command.name}: {locale.error}:", str(e))
                continue

            if args.help:
                command.parser.print_help()
                continue
            if len(unknown):
                command.parser.print_usage()
                error(f"{command.name}: {locale.error}: {locale.unrecognized}: {', '.join(unknown)}")
                continue

            try:
                command.run(ctx, args)
            except CommandStop as e:
                if len(e.args):
                    command.parser.print_usage()
                    error(f"{command.name}: {locale.error}:", *e.args)
                continue
            except ExitMenu as e:
                self.quit(ctx)
                raise
            except Exception as e:
                error("\n".join(traceback.format_exception(e)))

    def quit(self, ctx):
        pass

class Runner:
    def __init__(self):
        pass

    def run(self, initialmenu):
        self.ctx = CommandContext()
        stack = [initialmenu()]
        while len(stack):
            current = stack.pop()
            try:
                current.run(self.ctx)
            except ExitMenu as e:
                if len(e.args):
                    stack.append(current)
                    stack.append(e.args[0]())
