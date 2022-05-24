from .menu import Runner
from .commands.project import ProjectMenu

runner = Runner()
runner.run(ProjectMenu)
