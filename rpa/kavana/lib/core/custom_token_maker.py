from lib.core.exceptions.kavana_exception import CustomTokenMakerError
from lib.core.token_custom import (
    PointToken, RectangleToken, RegionToken,
    ImageToken, WindowToken, ApplicationToken
)
from lib.core.token_type import TokenType


class CustomTokenMaker:
    # 선언형 정의: 토큰 타입 → 인자 수 + 클래스
    _custom_token_definitions = {
        TokenType.POINT:       {"arg_count": 2, "token_class": PointToken},
        TokenType.RECTANGLE:   {"arg_count": 4, "token_class": RectangleToken},
        TokenType.REGION:      {"arg_count": 4, "token_class": RegionToken},
        TokenType.IMAGE:       {"arg_count": 1, "token_class": ImageToken},
        TokenType.WINDOW:      {"arg_count": 3, "token_class": WindowToken},
        TokenType.APPLICATION: {"arg_count": 2, "token_class": ApplicationToken},
    }

    @staticmethod
    def custom_object_token(tokens, start_idx, object_type=TokenType.UNKNOWN):
        object_type = tokens[start_idx].type if object_type == TokenType.UNKNOWN else object_type
        if object_type not in CustomTokenMaker._custom_token_definitions:
            raise CustomTokenMakerError(
                f"알려지지 않은 데이터 타입입니다.: {object_type}",
                tokens[start_idx].line, tokens[start_idx].column
            )
        return CustomTokenMaker.parse_arguments(tokens, start_idx, object_type)

    @staticmethod
    def parse_arguments(tokens, start_idx, object_type):
        """공통 파서: 선언형 정의 기반으로 CustomToken 생성"""
        definition = CustomTokenMaker._custom_token_definitions[object_type]
        expected_count = definition["arg_count"]
        token_cls = definition["token_class"]

        if tokens[start_idx].type != object_type:
            raise CustomTokenMakerError(
                f"Invalid {object_type.name} syntax: Expected {object_type.name}",
                tokens[start_idx].line, tokens[start_idx].column
            )

        i = start_idx + 1
        if i >= len(tokens) or tokens[i].type != TokenType.LEFT_PAREN:
            raise CustomTokenMakerError(
                f"Invalid {object_type.name} syntax: Expected '(' after {object_type.name}",
                tokens[start_idx].line, tokens[start_idx].column
            )
        i += 1  # skip '('

        args = [[] for _ in range(expected_count)]
        arg_index = 0
        paren_count = 1
        bracket_count = 0
        brace_count = 0

        while i < len(tokens):
            tok = tokens[i]

            if tok.type == TokenType.LEFT_PAREN:
                paren_count += 1
            elif tok.type == TokenType.RIGHT_PAREN:
                paren_count -= 1
                if paren_count == 0 and bracket_count == 0 and brace_count == 0:
                    i += 1
                    break
            elif tok.type == TokenType.LEFT_BRACKET:
                bracket_count += 1
            elif tok.type == TokenType.RIGHT_BRACKET:
                bracket_count -= 1
            elif tok.type == TokenType.LEFT_BRACE:
                brace_count += 1
            elif tok.type == TokenType.RIGHT_BRACE:
                brace_count -= 1
            elif tok.type == TokenType.COMMA:
                if paren_count == 1 and bracket_count == 0 and brace_count == 0:
                    arg_index += 1
                    if arg_index >= expected_count:
                        raise CustomTokenMakerError(
                            f"Invalid {object_type.name} syntax: Too many arguments",
                            tokens[start_idx].line, tokens[start_idx].column
                        )
                    i += 1
                    continue

            if arg_index >= expected_count:
                raise CustomTokenMakerError(
                    f"Invalid {object_type.name} syntax: Too many arguments",
                    tokens[start_idx].line, tokens[start_idx].column
                )
            args[arg_index].append(tok)
            i += 1

        if paren_count != 0 or bracket_count != 0 or brace_count != 0:
            raise CustomTokenMakerError(
                f"Invalid {object_type.name} syntax: Unmatched grouping symbols",
                tokens[start_idx].line, tokens[start_idx].column
            )

        if any(not arg for arg in args):
            raise CustomTokenMakerError(
                f"Invalid {object_type.name} syntax: Expected {expected_count} arguments",
                tokens[start_idx].line, tokens[start_idx].column
            )

        # ✅ CustomToken 인스턴스 생성
        result_token = token_cls(data=None)
        result_token.expressions = args
        result_token.line = tokens[start_idx].line
        result_token.column = tokens[start_idx].column

        return result_token, i
