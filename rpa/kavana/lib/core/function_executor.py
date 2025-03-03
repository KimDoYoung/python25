from typing import List
# from lib.core.command_parser import CommandParser

from lib.core.command_parser import CommandParser
from lib.core.datatypes.kavana_datatype import Boolean, Float, Integer, NoneType, String
from lib.core.token import Token
from lib.core.token_type import TokenType
from lib.core.variable_manager import VariableManager
class FunctionExecutor:
    def __init__(self, func_info, global_var_manager: VariableManager,arg_values: List):
        """
        사용자 정의 함수를 실행하는 실행기
        """
        self.function_type = func_info["type"]
        self.function_name = func_info["name"]
        self.func_body = func_info["func"]
        self.arg_names = func_info["arg_names"]
        # self.local_var_manager = VariableManager()  # ✅ 지역 변수 관리
        self.arg_values = arg_values # 실제 값
        self.global_var_manager = global_var_manager  # ✅ 전역 변수 관리

        for name, value in zip(self.arg_names, self.arg_values):
            token = self.convert_value(value)
            self.global_var_manager.set_variable(name, token, local=True)  # ✅ 인수를 지역 변수로 설정    

    # TODO 이 부분 즉 함수의 인자로 넘어오는 것이 express 즉 산술식으로 해석되어야할 듯.    
    def convert_value(self,value):
        """TRUE, FALSE, NULL 값을 변환"""
        value_upper = str(value).upper()
        if value_upper == "TRUE":
            return Token(Boolean(True), TokenType.BOOLEAN)
        elif value_upper == "FALSE":
            return Token(Boolean(False), TokenType.BOOLEAN)
        elif value_upper == "NONE":
            return Token(NoneType(None), TokenType.NONE)
        elif value.startswith('"') and value.endswith('"'):
            return Token(String(value[1:-1]), TokenType.STRING)
        elif '.' in value:  # 실수로 변환 가능하면 실수로 변환
            return Token(Float(float(value)), TokenType.FLOAT)
        else:
            return Token(Integer(int(value)), TokenType.INTEGER)

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

        result = self.global_var_manager.get_variable("return_value")
        return result
    
    def builtin_execute(self):
        """
        내장 함수를 실행하고 결과를 반환한다.
        """
        func = self.func_body
        # print(f"self.arg_values: {self.arg_values}")

        converted_args = [self.argument_evaluation(arg) for arg in self.arg_values]
        # print(f"converted_args: {converted_args}")
        return func(*converted_args)
    
    def argument_evaluation(self, arg):
        from lib.core.expr_evaluator import ExprEvaluator
        """
        함수 인수를 평가한다.
        """
        argEvaluator = ExprEvaluator(arg, self.global_var_manager)
        return argEvaluator.evaluate()
