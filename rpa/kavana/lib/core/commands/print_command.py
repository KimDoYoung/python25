import re
from lib.core.commands.base_command import BaseCommand
from lib.core.expr_evaluator import ExprEvaluator

class PrintCommand(BaseCommand):
    def execute(self, args, executor):
        if not args:
            raise SyntaxError("PRINT command requires at least one argument.")

        # ✅ 여러 인자를 공백으로 결합
        output = " ".join(args)

        # ✅ 따옴표 제거 (예: PRINT "Hello" → Hello)
        if output.startswith('"') and output.endswith('"'):
            output = output[1:-1]

        # ✅ `{}` 내부 표현을 평가하는 함수
        def evaluate_match(match):
            expression = match.group(1)  # `{}` 내부 표현식
            evaluator = ExprEvaluator(expression, executor.variable_manager)
            return str(evaluator.evaluate())  # 평가 후 문자열 반환

        # ✅ `{}` 패턴을 찾아 `ExprEvaluator`를 사용하여 해석
        output = re.sub(r"\{(.*?)\}", evaluate_match, output)

        # ✅ 특수 문자(\n, \t) 지원
        output = output.replace("\\n", "\n").replace("\\t", "\t")

        print(output)