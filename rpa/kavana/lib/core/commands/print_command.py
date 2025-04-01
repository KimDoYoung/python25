from lib.core.commands.base_command import BaseCommand
from lib.core.datatypes.kavana_datatype import KavanaDataType
from lib.core.exceptions.kavana_exception import KavanaSyntaxError
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.token import Token
from lib.core.token_type import TokenType  # 필요 시

class PrintCommand(BaseCommand):
    def execute(self, args: list[Token], executor):
        if not args:
            raise KavanaSyntaxError("PRINT 명령어는 최소 하나 이상의 인자가 필요합니다.")

        # 1. 콤마로 분할하여 각 expression 단위로 분리
        expressions = self._split_expressions(args)

        # 2. 각 expression을 평가
        evaluator = ExprEvaluator(executor)
        evaluated_values = []
        for expr_tokens in expressions:
            result_token = evaluator.evaluate(expr_tokens)
            if isinstance(result_token, Token):
                evaluated_values.append(result_token.data.string)
            elif isinstance(result_token, KavanaDataType):
                evaluated_values.append(result_token.string)

        # 3. 공백으로 join해서 출력
        print(" ".join(evaluated_values))

    def _split_expressions(self, tokens: list[Token]) -> list[list[Token]]:
        expressions = []
        current_expr = []

        # 괄호 깊이 추적
        paren_count = 0     # ()
        bracket_count = 0   # []
        brace_count = 0     # {}

        for token in tokens:
            tok_type = token.type
            tok_val = token.data.value

            # 괄호 카운트
            if tok_val == '(':
                paren_count += 1
            elif tok_val == ')':
                paren_count -= 1
            elif tok_val == '[':
                bracket_count += 1
            elif tok_val == ']':
                bracket_count -= 1
            elif tok_val == '{':
                brace_count += 1
            elif tok_val == '}':
                brace_count -= 1

            # 괄호 바깥에서 나오는 콤마만 expression 분리 기준
            if tok_type == TokenType.COMMA and paren_count == 0 and bracket_count == 0 and brace_count == 0:
                if current_expr:
                    expressions.append(current_expr)
                    current_expr = []
                continue

            current_expr.append(token)

        if current_expr:
            expressions.append(current_expr)

        return expressions

