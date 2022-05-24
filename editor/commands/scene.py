from .base import ExitCommand
from ..menu import CommandMenu

class SceneMenu(CommandMenu):
    cmds = {
        "exit": ExitCommand
    }

    def run(self, ctx):
        assert ctx.scene is not None
        super().run(ctx)

    def quit(self, ctx):
        ctx.scene = None
