from typing import List
from lib.core.commands.base_command import BaseCommand
from lib.core.datatypes.application import Application
from lib.core.exceptions.kavana_exception import KavanaNameError, KavanaSyntaxError, KavanaTypeError
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.token import Token
from lib.core.token_type import TokenType
from lib.core.token_util import TokenUtil

class AppOpenCommand(BaseCommand):
    def execute(self, args: list[Token], executor):
        """
        APP_OPEN <app_variable> [maximize=<express>, focus=<express>]
        """
        if len(args) < 1 or args[0].type != TokenType.IDENTIFIER:
            raise KavanaSyntaxError("APP_OPEN 명령어는 최소 하나의 인자(application 변수)가 필요합니다.")

        app_name = args[0].data.string
        app_token = executor.variable_manager.get_variable(app_name)

        if not app_token:
            raise KavanaNameError(f"변수 '{app_name}'가 정의되지 않았습니다.")

        if app_token.type != TokenType.APPLICATION:
            raise KavanaTypeError(f"변수 '{app_name}'는 Application 타입이 아닙니다.")

        # ✅ 기본 옵션 맵 정의 (기본값 설정)
        option_map = {
            "maximize": {"default": False, "allowed_types": [TokenType.BOOLEAN]},
            "focus": {"default": True, "allowed_types": [TokenType.BOOLEAN]},
            "process_name": {"default": None, "allowed_types": [TokenType.STRING]}
        }

        # ✅ 옵션 값 초기화
        option_values = {key: option_map[key]["default"] for key in option_map}

        # ✅ 옵션 리스트가 존재하는 경우 처리 (args[1:]는 List[Token])
        if len(args) > 1:
            option_tokens: List[Token] = args[1:]  # ✅ args[1:] 전체가 옵션 리스트
            i = 0
            # option_tokens[i] 가 "," 이면 다음 토큰으로 이동
            while option_tokens[i].type == TokenType.COMMA:
                i += 1

            while i < len(option_tokens):
                key_token, express_tokens, next_index = self.extract_option1(option_tokens, i)
                
                if key_token is None:
                    break
                
                key = key_token.data.string.strip().lower()
                if key not in option_map:
                    raise KavanaSyntaxError(f"알 수 없는 옵션 '{key}'입니다.")
                
                # ✅ ExprEvaluator를 사용하여 표현식 평가
                expr_evaluator = ExprEvaluator( executor=executor)
                evaluated_value = expr_evaluator.evaluate(express_tokens)
                
                # ✅ 값의 데이터 타입 확인
                allowed_types = option_map[key]["allowed_types"]
                if evaluated_value.type not in allowed_types:
                    allowed_type_names = [t.name for t in allowed_types]
                    raise KavanaTypeError(
                        f"옵션 '{key}'는 {', '.join(allowed_type_names)} 타입만 허용됩니다. (현재: {evaluated_value.type.name})"
                    )
                
                # ✅ 옵션 값 저장
                option_values[key] = evaluated_value.data.value
                i = next_index  # 다음 key=value로 이동

        # ✅ 애플리케이션 실행 (option_map을 활용)
        app = app_token.data
        app.launch(
            executor=executor,
            maximize=option_values["maximize"],
            focus=option_values["focus"],
            process_name=option_values["process_name"]
        )
