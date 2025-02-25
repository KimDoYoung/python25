from typing import List
from lib.core.command_parser import CommandParser

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
        self.local_var_manager = VariableManager()  # ✅ 지역 변수 관리
        self.arg_values = arg_values # 실제 값
        self.global_var_manager = global_var_manager  # ✅ 전역 변수 관리

        for name, value in zip(self.arg_names, self.arg_values):
            value = self.convert_value(value)
            self.global_var_manager.set_variable(name, value, local=True)  # ✅ 인수를 지역 변수로 설정    
    
    def convert_value(self,value):
        """TRUE, FALSE, NULL 값을 변환"""
        value_upper = str(value).upper()
        if value_upper == "TRUE":
            return True
        elif value_upper == "FALSE":
            return False
        elif value_upper == "NULL":
            return None
        elif value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        elif '.' in value:  # 실수로 변환 가능하면 실수로 변환
            return float(value)
        else:
            return int(value)
        return value

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
        
        # parsing
        script_lines = self.func_body
        parser = CommandParser(script_lines)
        parser.ignore_main_check = True  # ✅ main 함수 체크 무시
        parsed_commands = parser.parse()
        # 실행
        for line in parsed_commands:
            executor.execute(line)
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
