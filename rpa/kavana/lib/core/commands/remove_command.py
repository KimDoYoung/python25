from lib.core.token import Token
from lib.core.datatypes.list_type import ListType
from lib.core.datatypes.kavana_datatype import String
from lib.core.exceptions.kavana_exception import CommandExecutionError

class RemoveCommand:
    def execute(self, args, executor):
        """REMOVE 명령어 실행"""
        if len(args) < 2:
            raise CommandExecutionError("REMOVE requires at least two arguments.")

        var_name = args[0].data.value
        value_token = args[1]

        target_variable = executor.variable_manager.get_variable(var_name)
        if not target_variable:
            raise CommandExecutionError(f"Variable '{var_name}' not defined.")

        if isinstance(target_variable.data, ListType):
            if isinstance(value_token.data, int):  # 인덱스 삭제
                target_variable.data.remove_at(value_token.data)
            else:  # 값 삭제
                target_variable.data.remove(value_token.data)
        elif isinstance(target_variable.data, String):
            target_variable.data.value = target_variable.data.value.replace(str(value_token.data), "")
        else:
            raise CommandExecutionError(f"Cannot REMOVE from type {type(target_variable.data)}")
