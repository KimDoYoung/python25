from typing import List
from lib.core.datatypes.kavana_datatype import Float, Integer, String
from lib.core.token import Token
from lib.core.token_util import TokenUtil
from lib.core.variable_manager import VariableManager
class FunctionExecutor:
    def __init__(self, func_info, global_var_manager: VariableManager, arg_values: List[Token] ):
        """
        사용자 정의 함수를 실행하는 실행기
        """
        self.function_type = func_info["type"]
        self.function_name = func_info["name"]
        self.func_body = func_info["func"]
        self.arg_names = func_info["arg_names"]
        self.arg_values = arg_values # 실제 값
        self.global_var_manager = global_var_manager  # ✅ 전역 변수 관리

        for name, token in zip(self.arg_names, self.arg_values):
            self.global_var_manager.set_variable(name, token, local=True)  # ✅ 인수를 지역 변수로 설정    

    def execute(self):
        if self.function_type == "builtin":
            return self.builtin_execute()
        else:
            return self.user_execute()    

    def user_execute(self):
        """
        함수 본문을 실행하고 결과를 반환한다.
        """
        from lib.core.command_executor import CommandExecutor
        executor = CommandExecutor()  # ✅ 명령어 실행기 생성
        executor.variable_manager = self.global_var_manager  # ✅ 지역 변수로 설정
        executor.in_function_scope = True  # ✅ 함수 내부 실행 중 표시        
        
        # ✅ 저장된 `commands` 가져오기 (이미 `CommandParser.parse()`를 거친 상태)
        script_commands = self.func_body  # ✅ `commands` 리스트가 저장됨

        # ✅ 이미 파싱된 `commands`을 바로 실행, function 정의 1번째줄 제외
        for command in script_commands:
            executor.execute(command)

        result = self.global_var_manager.get_variable("$$return_value$$")
        return result
    
    def builtin_execute(self):
        """
        내장 함수를 실행하고 결과를 반환한다.
        """
        func = self.func_body
        if self.function_name in {"TYPE_OF", "IS_TYPE", "GET_ATTR", "DUMP_ATTRS"}: # kavana type으로 넘겨야할 함수들
            converted_args = [arg.data for arg in self.arg_values]    
            return func(*converted_args)
        
        # converted_args = [arg.data.value for arg in self.arg_values]    
        converted_args = [TokenUtil.token_to_python_primitive(token) for token in self.arg_values]    
        return func(*converted_args)
    
