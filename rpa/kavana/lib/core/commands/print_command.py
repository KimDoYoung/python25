import re
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor
from lib.core.commands.base_command import BaseCommand
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.token import Token

class PrintCommand(BaseCommand):
    def execute(self, args: list[Token], executor):
        if not args:
            raise SyntaxError("PRINT command requires at least one argument.")

        # ✅ 여러 인자를 공백으로 결합하여 문자열 생성
        output = " ".join(token.value.value for token in args)

        # ✅ `{}` 내부 표현을 평가하는 함수
        def evaluate_match(match):
            expression = match.group(1)  # `{}` 내부 표현식
            
            # ✅ 문자열을 토큰화하여 ExprEvaluator에 전달
            ppLines = CommandPreprocessor().preprocess([expression])
            tokens = CommandParser.tokenize(ppLines[0])
            evaluator = ExprEvaluator(executor.variable_manager)
            
            # ✅ 평가 후 문자열 반환
            result_token = evaluator.evaluate(tokens)
            return str(result_token.value.value)

        # ✅ `{}` 패턴을 찾아 `ExprEvaluator`를 사용하여 해석
        output = re.sub(r"\{(.*?)\}", evaluate_match, output)

        # ✅ 특수 문자(\n, \t) 지원 (Pythonic한 방식으로 변환)
        output = output.encode().decode("unicode_escape")

        print(output)
