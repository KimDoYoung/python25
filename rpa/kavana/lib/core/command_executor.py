
from lib.core.commands.endfunction_command import EndFunctionCommand
from lib.core.commands.function_command import FunctionCommand
from lib.core.commands.print_command import PrintCommand
from lib.core.commands.set_command import SetCommand
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.variable_manager import VariableManager


class CommandExecutor:
    """
    CommandExecutor는 Kavana 스크립트에서 파싱된 명령을 실행한다.
    """
    def __init__(self):
        self.variable_manager = VariableManager()
        self.in_function_scope = False  # ✅ 함수 내부 여부 추적
        self.command_map = {
            "SET": SetCommand(),
            "PRINT": PrintCommand(),
            "FUNCTION": FunctionCommand(),
            "END_FUNCTION": EndFunctionCommand(),
        }

    def execute(self, command: dict):
        """
        주어진 명령을 실행한다.
        :param command: {"cmd": "SET", "args": ["var_name", "=", "expression"]}
        """
        cmd = command["cmd"]
        args = command["args"]

        # ✅ 명령어 실행
        if cmd in self.command_map:
            self.command_map[cmd].execute(args, self)  # 명령어 객체에 실행 위임
        else:
            raise ValueError(f"Unknown command: {cmd}")

