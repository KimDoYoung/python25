from typing import List
from lib.core.commands.base_command import BaseCommand
from lib.core.exceptions.kavana_exception import CommandExecutionError
from lib.core.token_type import TokenType
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.token import Token

class ConstCommand(BaseCommand):
    def execute(self, args:List[Token], executor):
        """
        CONST <varname> = <expression>
        """
        if len(args) < 3 or args[1].data.value != "=":
            raise CommandExecutionError("Invalid CONST command format. Expected: SET <varname> = <expression> [GLOBAL]")

        var_name = args[0].data.value
        expression = args[2:]  # 수식 부분

        # 수식 평가
        exprEvaluator = ExprEvaluator(executor)
        result_token = exprEvaluator.evaluate(expression)
        
        # 변수 저장
        executor.variable_manager.set_const(var_name, result_token)
