from lib.core.commands.base_command import BaseCommand


class FunctionCommand(BaseCommand):
    def execute(self, args, executor):
        """
        FUNCTION <function_name>
        """
        executor.variable_manager.push_local_scope()
        executor.in_function_scope = True