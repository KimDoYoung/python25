from typing import List
from lib.core.commands.base_command import BaseCommand
from lib.core.token_type import TokenType
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.token import Token

class SetCommand(BaseCommand):
    def execute(self, args:List[Token], executor):
        """
        SET <varname> = <expression> [GLOBAL]
        """
        if len(args) < 3 or args[1].data.value != "=":
            raise SyntaxError("Invalid SET command format. Expected: SET <varname> = <expression> [GLOBAL]")

        var_name = args[0].data.value
        expression = args[2:]  # 수식 부분
        local_flag = executor.in_function_scope  # ✅ 함수 내부면 자동으로 Local

        # GLOBAL 키워드가 붙으면 전역 변수 강제 설정
        if args[-1].type == TokenType.GLOBAL:
            local_flag = False
            expression = args[2:-1]  # GLOBAL 제거

        # 수식 평가
        exprEvaluator = ExprEvaluator(executor.variable_manager)
        value_token = exprEvaluator.evaluate(expression)
        # 변수 저장
        if args[0].type == TokenType.LIST_INDEX: # SET list[0] = 10
            # 리스트 요소 대입
            var_name = args[0].data.value
            list_index_token = executor.variable_manager.get_variable(var_name)
            row_express = args[0].row_express
            col_express = args[0].column_express
            row = ExprEvaluator(executor.variable_manager).evaluate(row_express).data.value
            col = None
            if col_express:
                col = ExprEvaluator(executor.variable_manager).evaluate(col_express).data.value
            list_index_token.data.set(row,col, value_token)
        else:
            executor.variable_manager.set_variable(var_name, value_token, local=local_flag)
