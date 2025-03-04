from lib.core.token import Token
from lib.core.datatypes.list_type import ListType
from lib.core.datatypes.kavana_datatype import String
from lib.core.exceptions.kavana_exception import CommandExecutionError

class AppendCommand:
    def execute(self, args, executor):
        """APPEND 명령어 실행"""
        if len(args) < 2:
            raise CommandExecutionError("APPEND requires at least two arguments.")

        var_name = args[0].data.value
        value_token = args[1]

        target_variable = executor.variable_manager.get_variable(var_name)
        if not target_variable:
            raise CommandExecutionError(f"Variable '{var_name}' not defined.")

        if isinstance(target_variable.data, ListType):
            target_variable.data.append(value_token.data)
        elif isinstance(target_variable.data, String):
            target_variable.data.value += str(value_token.data)
        else:
            raise CommandExecutionError(f"Cannot APPEND to type {type(target_variable.data)}")
