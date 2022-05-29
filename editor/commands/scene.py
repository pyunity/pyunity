from .base import ExitCommand, HelpCommand
from ..menu import CommandMenu

class SceneMenu(CommandMenu):
    cmds = {
        "help": HelpCommand,
        "exit": ExitCommand,
    }

    def run(self, ctx):
        assert ctx.scene is not None
        super().run(ctx)

    def quit(self, ctx):
        ctx.scene = None
