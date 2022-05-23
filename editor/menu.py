from .context import CommandContext
import shlex

class MenuFlow(Exception):
    pass

class CommandStop(MenuFlow):
    pass

class ExitMenu(MenuFlow):
    pass

class CommandMenu:
    prompt = "%> "
    cmds = {}

    def __init__(self):
        self.commands = {}
        for name, item in type(self).cmds.items():
            self.commands[name] = item(self)
        self.ctx = None

    def run(self, ctx):
        while True:
            cmd = input(self.prompt)
            args = shlex.split(cmd)
            cmdname = args[0]
            args = args[1:]
            if cmdname not in self.commands:
                print(f"{cmdname}: command not found")
                continue

            command = self.commands[cmdname]
            try:
                command.run(ctx, args)
            except CommandStop as e:
                if len(e.args):
                    print("Error:", *e.args)
                continue
            except ExitMenu as e:
                if len(e.args):
                    return e.args[0]
                return None

class Runner:
    def __init__(self):
        pass

    def run(self, initialcontext):
        self.ctx = CommandContext()
        stack = [initialcontext()]
        while len(stack):
            nextcontext = stack[-1].run(self.ctx)
            if nextcontext is not None:
                stack.append(nextcontext())
            else:
                stack.pop()
