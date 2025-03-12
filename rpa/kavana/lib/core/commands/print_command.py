import re
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor
from lib.core.commands.base_command import BaseCommand
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.token import Token
from lib.core.token_type import TokenType

class PrintCommand(BaseCommand):
    """PRINT 명령어 확장: 여러 인자 지원, `{}` 표현식 평가"""

    def execute(self, args: list[Token], executor):
        if not args:
            raise SyntaxError("PRINT 명령어는 최소 하나의 인자가 필요합니다.")

        # ✅ 콤마(COMMA) 무시하고 문자열 결합
        filtered_tokens = [token for token in args if token.type != TokenType.COMMA]

        # ✅ 여러 인자를 공백으로 연결하여 문자열 생성
        raw_message = " ".join(token.data.string for token in filtered_tokens)

        # ✅ 2단계: `{}` 표현식을 평가
        message = self._evaluate_message(raw_message, executor)

        # ✅ `__LBRACE__`, `__RBRACE__` 복원 (출력 시 `{{`와 `}}` 유지)
        message = message.replace("__LBRACE__", "{{").replace("__RBRACE__", "}}")

        # ✅ 최종 출력
        print(message)

    def _evaluate_message(self, message: str, executor, allow_recurse=True):
        """문자열 내 `{}` 표현식을 평가하여 실제 값으로 변환"""
        def replace_expr(match):
            expression = match.group(1)  # `{}` 내부 표현식
            
            try:
                # ✅ 문자열을 토큰화하여 ExprEvaluator에 전달
                ppLines = CommandPreprocessor().preprocess([expression])
                tokens = CommandParser.tokenize(ppLines[0])
                evaluator = ExprEvaluator(executor)
                
                # ✅ 변수 존재 여부 확인
                result_token = evaluator.evaluate(tokens)
                return result_token.data.string
            except Exception as e:
                # ✅ 변수 미정의 또는 오류 발생 시 `{}`를 사용하지 않고 `[ERROR]`로 처리
                return f"[ERROR: {str(e)}]"

        # ✅ `{}` 패턴을 찾아 `ExprEvaluator`를 사용하여 해석
        message = re.sub(r"\{(.*?)\}", replace_expr, message)

        # ✅ `__LBRACE__`, `__RBRACE__` 복원 (변수 해석 후 다시 `{{`와 `}}`로 원복)
        message = message.replace("__LBRACE__", "{{").replace("__RBRACE__", "}}")

        # ✅ 무한 루프 방지를 위해 추가 재평가 제한
        if allow_recurse and "{" in message and "}" in message:
            return self._evaluate_message(message, executor, allow_recurse=False)

        return message
