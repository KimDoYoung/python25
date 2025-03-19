from lib.core.commands.base_command import BaseCommand
from lib.core.expr_evaluator import ExprEvaluator


class JustCommand(BaseCommand):
    ''' just command expression만 해석한다'''
    def execute(self, args, executor):
            if len(args) < 1 :
                return
            expression = args # 수식 부분

            # 수식 평가
            exprEvaluator = ExprEvaluator(executor)
            exprEvaluator.evaluate(expression)
            return
