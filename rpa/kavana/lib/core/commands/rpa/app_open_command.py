from typing import List
from lib.core.commands.base_command import BaseCommand
from lib.core.datatypes.application import Application
from lib.core.exceptions.kavana_exception import KavanaNameError, KavanaSyntaxError, KavanaTypeError
from lib.core.token import Token
from lib.core.token_type import TokenType

class AppOpenCommand(BaseCommand):
    def execute(self, args:list[Token], executor):
        """
        APP_OPEN <app_variable> [maximize=True, focus=True]
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
        }

        # ✅ 옵션 값 초기화
        option_values = {key: option_map[key]["default"] for key in option_map}


        # ✅ 옵션 리스트가 존재하는 경우 처리 (args[1:]는 List[Token])
        if len(args) > 1:
            option_tokens: List[Token] = args[1:]  # ✅ args[1:] 전체가 옵션 리스트

            i = 0
            while i < len(option_tokens) - 1:
                if option_tokens[i + 1].type == TokenType.ASSIGN:  # ✅ 현재 토큰의 다음이 ASSIGN 토큰인지 확인
                    key_token = option_tokens[i]  # ✅ ASSIGN 앞 토큰이 key
                    value_token = option_tokens[i + 2]  # ✅ ASSIGN 뒤 토큰이 value

                    # ✅ 키가 option_map에 있는지 확인
                    key = key_token.data.string.strip().lower()
                    if key not in option_map:
                        raise KavanaSyntaxError(f"알 수 없는 옵션 '{key}'입니다.")

                    # ✅ 값의 데이터 타입 확인
                    allowed_types = option_map[key]["allowed_types"]
                    if value_token.type not in allowed_types:
                        allowed_type_names = [t.name for t in allowed_types]
                        raise SyntaxError(
                            f"옵션 '{key}'는 {', '.join(allowed_type_names)} 타입만 허용됩니다. "
                            f"(현재: {value_token.type.name})"
                        )

                    # ✅ 옵션 값 저장
                    option_values[key] = value_token.data.value  # True / False 저장

                    i += 3  # ✅ `key_token, assign_token, value_token`을 처리했으므로 +3 증가
                else:
                    i += 1  # ✅ `ASSIGN`이 없으면 그냥 다음 토큰으로 이동

            # ✅ 애플리케이션 실행 (option_map을 활용)
        app = app_token.data
        app.launch(
            executor=executor,
            maximize=option_map["maximize"],
            focus=option_map["focus"]
        )
