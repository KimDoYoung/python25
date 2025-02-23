from typing import List
from lib.core.command_executor import CommandExecutor
from lib.core.function_registry import FunctionRegistry
from lib.core.variable_manager import VariableManager


class FunctionExecutor:
    def __init__(self, function_name: str, func_body: List[str], param_names: List[str], local_vars: dict, global_var_manager: VariableManager):
        """
        사용자 정의 함수를 실행하는 실행기
        """
        self.function_name = function_name
        self.func_body = func_body
        self.param_names = param_names
        self.local_var_manager = VariableManager()  # ✅ 지역 변수 관리
        self.local_var_manager.variables.update(local_vars)  # ✅ 지역 변수 설정
        self.global_var_manager = global_var_manager  # ✅ 전역 변수 관리

    def execute(self):
        """
        함수 본문을 실행하고 결과를 반환한다.
        """
        executor = CommandExecutor()  # ✅ 명령어 실행기 생성
        executor.variable_manager = self.local_var_manager  # ✅ 지역 변수로 설정
        executor.in_function_scope = True  # ✅ 함수 내부 실행 중 표시

        result = None
        for line in self.func_body:
            tokens = executor.tokenize(line)
            if not tokens:
                continue

            command = {"cmd": tokens[0].upper(), "args": tokens[1:]}
            result = executor.execute(command)

            if command["cmd"] == "RETURN":
                break  # ✅ RETURN이 나오면 함수 종료

        return result
