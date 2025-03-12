from lib.core.commands.base_command import BaseCommand
from lib.core.expr_evaluator import ExprEvaluator


class ReturnCommand(BaseCommand):
    def execute(self, args, executor):
        if len(args) < 1 :
            # 그냥 return_value에 None을 설정
            executor.variable_manager.set_variable("$$return_value$$", None, local=True)
            return
        expression = args # 수식 부분
        local_flag = executor.in_function_scope  # ✅ 함수 내부면 자동으로 Local

        # 수식 평가
        exprEvaluator = ExprEvaluator(executor)
        value = exprEvaluator.evaluate(expression)

        # 변수 저장
        executor.variable_manager.set_variable("$$return_value$$", value, local=local_flag)