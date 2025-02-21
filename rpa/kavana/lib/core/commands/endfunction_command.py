from lib.core.commands.base_command import BaseCommand


class EndFunctionCommand(BaseCommand):
    def execute(self, args, executor):
        executor.end_function()