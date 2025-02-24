from lib.core.commands.base_command import BaseCommand
from lib.core.expr_evaluator import ExprEvaluator

class SetCommand(BaseCommand):
    def execute(self, args, executor):
        """
        SET <varname> = <expression> [GLOBAL]
        """
        if len(args) < 3 or args[1] != "=":
            raise SyntaxError("Invalid SET command format. Expected: SET <varname> = <expression> [GLOBAL]")

        var_name = args[0]
        expression = " ".join(args[2:])  # 수식 부분
        local_flag = executor.in_function_scope  # ✅ 함수 내부면 자동으로 Local

        # GLOBAL 키워드가 붙으면 전역 변수 강제 설정
        if args[-1].upper() == "GLOBAL":
            local_flag = False
            expression = " ".join(args[2:-1])  # GLOBAL 제거

        # 수식 평가
        exprEvaluator = ExprEvaluator(expression, executor.variable_manager)
        value = exprEvaluator .evaluate()

        # 변수 저장
        executor.variable_manager.set_variable(var_name, value, local=local_flag)
