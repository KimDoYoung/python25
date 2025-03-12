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

        # ✅ 1단계: `{{i}}` 같은 패턴을 `{i}`로 변환 (안전한 토큰 사용)
        raw_message = raw_message.replace("{{", "__LBRACE__").replace("}}", "__RBRACE__")

        # ✅ 2단계: `{}` 표현식을 평가
        message = self._evaluate_message(raw_message, executor)


        # ✅ 중첩된 `{}` 표현식 재평가 (예: `$exception_message` 안의 `{}` 처리)
        while "{" in message and "}" in message:
            new_message = self._evaluate_message(message, executor)
            if new_message == message:
                break  # 더 이상 변화가 없으면 종료
            message = new_message  # 변환된 메시지를 계속 처리

        # ✅ 3단계: `__LBRACE__` → `{`, `__RBRACE__` → `}` 복원
        message = message.replace("__LBRACE__", "{").replace("__RBRACE__", "}")

        # ✅ 최종 출력
        print(message)

    def _evaluate_message(self, message: str, executor):
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
                # return str(result_token.data.value)
                return result_token.data.string
            except Exception as e:
                # ✅ 변수 미정의 시 `{var1}`을 그대로 유지
                if "Undefined variable" in str(e):
                    return f"{{{expression}}}"
                return f"{{ERROR: {e}}}"  # 다른 오류 발생 시 메시지 출력

        # ✅ `{}` 패턴을 찾아 `ExprEvaluator`를 사용하여 해석
        return re.sub(r"\{(.*?)\}", replace_expr, message)
