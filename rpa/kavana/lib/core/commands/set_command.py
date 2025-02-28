from typing import List
from lib.core.commands.base_command import BaseCommand
from lib.core.datatypes.token_type import TokenType
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.token import Token

class SetCommand(BaseCommand):
    def execute(self, args:List[Token], executor):
        """
        SET <varname> = <expression> [GLOBAL]
        """
        if len(args) < 3 or args[1].value != "=":
            raise SyntaxError("Invalid SET command format. Expected: SET <varname> = <expression> [GLOBAL]")

        var_name = args[0].value
        expression = args[2:]  # 수식 부분
        local_flag = executor.in_function_scope  # ✅ 함수 내부면 자동으로 Local

        # GLOBAL 키워드가 붙으면 전역 변수 강제 설정
        if args[-1].type == TokenType.GLOBAL:
            local_flag = False
            expression = args[2:-1]  # GLOBAL 제거

        # 수식 평가
        exprEvaluator = ExprEvaluator(executor.variable_manager)
        value = exprEvaluator.evaluate(expression)

        # 변수 저장
        executor.variable_manager.set_variable(var_name, value, local=local_flag)
