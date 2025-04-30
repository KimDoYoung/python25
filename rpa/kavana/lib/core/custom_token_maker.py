# custom_token_maker.py: 사용자 정의 객체 토큰 생성기
from lib.core.exceptions.kavana_exception import CustomTokenMakerError
from lib.core.token_custom import ApplicationToken, CustomToken, ImageToken, PointToken, RectangleToken, RegionToken, WindowToken
from lib.core.token_type import TokenType


class CustomTokenMaker:
    @staticmethod
    def custom_object_token(tokens, start_idx, object_type=TokenType.UNKNOWN):
        """
        ✅ `Point`, `Rectangle`, `Region`, `Image` 등을 공통 처리하는 함수.
        ✅ `object_type`에 따라 각 타입별 개별 함수를 호출.

        - tokens: 토큰 리스트
        - start_idx: 객체 시작 인덱스
        - object_type: 객체의 타입 (`POINT`, `RECTANGLE`, `REGION`, `IMAGE`, `WINDOW`, `APPLICATION` 등)
        - 반환값: (생성된 CustomToken, 재시작할 인덱스)
        """
        object_type = tokens[start_idx].type if object_type == TokenType.UNKNOWN else object_type
        type_to_function = {
            TokenType.POINT: CustomTokenMaker.point_token,
            TokenType.RECTANGLE: CustomTokenMaker.rectangle_token,
            TokenType.REGION: CustomTokenMaker.region_token,
            TokenType.IMAGE: CustomTokenMaker.image_token,
            TokenType.WINDOW: CustomTokenMaker.window_token,
            TokenType.APPLICATION: CustomTokenMaker.application_token,
        }

        if object_type not in type_to_function:
            raise CustomTokenMakerError(f"Unknown object type: {object_type}", tokens[start_idx].line, tokens[start_idx].column)

        return type_to_function[object_type](tokens, start_idx)

    @staticmethod
    def point_token(tokens, start_idx):
        """✅ `Point(x, y)` 또는 `Point x, y` 형식을 처리"""
        return CustomTokenMaker._parse_two_arguments(tokens, start_idx, TokenType.POINT)

    @staticmethod
    def rectangle_token(tokens, start_idx):
        """✅ `Rectangle(x, y, width, height)` 또는 `Rectangle x, y, width, height` 형식을 처리"""
        return CustomTokenMaker._parse_four_arguments(tokens, start_idx, TokenType.RECTANGLE)

    @staticmethod
    def region_token(tokens, start_idx):
        """✅ `Region(x, y, width, height)` 또는 `Region x, y, width, height` 형식을 처리"""
        return CustomTokenMaker._parse_four_arguments(tokens, start_idx, TokenType.REGION)

    @staticmethod
    def window_token(tokens, start_idx):
        """✅ `Window("title")` 또는 `Window "title"` 형식을 처리"""
        return CustomTokenMaker._parse_single_argument(tokens, start_idx, TokenType.WINDOW)

    @staticmethod
    def application_token(tokens, start_idx):
        """✅ `Application("name")` 또는 `Application "name"` 형식을 처리"""
        return CustomTokenMaker._parse_single_argument(tokens, start_idx, TokenType.APPLICATION)
   
    @staticmethod
    def image_token(tokens, start_idx):
        """✅ Image"""
        return CustomTokenMaker._parse_single_argument(tokens, start_idx, TokenType.IMAGE)    


    @staticmethod
    def _parse_single_argument(tokens, start_idx, object_type):
        """ 1개의 인자를 갖는 객체처리 Image, Window, Application """
        if tokens[start_idx].type not in [TokenType.WINDOW, TokenType.APPLICATION, TokenType.IMAGE]:
            raise CustomTokenMakerError(
                f"Invalid {object_type.name} syntax: Expected 'Image' or 'Window' or 'Application' at position {start_idx}",
                tokens[start_idx].line, tokens[start_idx].column
            )
        i = start_idx + 1

        if i >= len(tokens):
            raise CustomTokenMakerError(
                f"Invalid {object_type.name} syntax: Missing argument",
                tokens[start_idx].line, tokens[start_idx].column
            )

        arg_tokens = []
        if tokens[i].type != TokenType.LEFT_PAREN:
            raise CustomTokenMakerError(
                f"Invalid {object_type.name} syntax: Expected '(' after '{object_type.name}'",
                tokens[start_idx].line, tokens[start_idx].column
            )

        # ✅ 괄호 시작 → 복합 표현식 수집
        i += 1
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
                    break
            elif tok.type == TokenType.LEFT_BRACKET:
                bracket_count += 1
            elif tok.type == TokenType.RIGHT_BRACKET:
                bracket_count -= 1
            elif tok.type == TokenType.LEFT_BRACE:
                brace_count += 1
            elif tok.type == TokenType.RIGHT_BRACE:
                brace_count -= 1

            arg_tokens.append(tok)
            i += 1

        if paren_count != 0 or bracket_count != 0 or brace_count != 0:
            raise CustomTokenMakerError(
                f"Invalid {object_type.name} syntax: Unmatched grouping symbols",
                tokens[start_idx].line, tokens[start_idx].column
            )

        i += 1  # skip final RIGHT_PAREN

        # ✅ 토큰 생성
        if object_type == TokenType.WINDOW:
            result_token = WindowToken(data=None)
            result_token.type = TokenType.WINDOW
        elif object_type == TokenType.APPLICATION:
            result_token = ApplicationToken(data=None)
            result_token.type = TokenType.APPLICATION
        elif object_type == TokenType.IMAGE:
            result_token = ImageToken(data=None)
            result_token.type = TokenType.IMAGE
        else:
            raise CustomTokenMakerError(f"Unknown object type: {object_type}", tokens[start_idx].line, tokens[start_idx].column)

        result_token.expressions = [arg_tokens]
        result_token.line = tokens[start_idx].line
        result_token.column = tokens[start_idx].column

        return result_token, i


    @staticmethod
    def _parse_two_arguments(tokens, start_idx, object_type):
        """✅ Point(10, 20)처럼 인자가 2개인 표현을 파싱"""
        if tokens[start_idx].type != object_type:
            raise CustomTokenMakerError(
                f"Invalid {object_type.name} syntax: Expected {object_type.name} at position {start_idx}",
                tokens[start_idx].line, tokens[start_idx].column
            )

        i = start_idx + 1
        if i >= len(tokens) or tokens[i].type != TokenType.LEFT_PAREN:
            raise CustomTokenMakerError(
                f"Invalid {object_type.name} syntax: Expected '(' after {object_type.name}",
                tokens[start_idx].line, tokens[start_idx].column
            )

        i += 1  # skip LEFT_PAREN
        arg1_tokens = []
        arg2_tokens = []

        paren_count = 1
        bracket_count = 0
        brace_count = 0

        current_arg = arg1_tokens

        while i < len(tokens):
            tok = tokens[i]

            if tok.type == TokenType.LEFT_PAREN:
                paren_count += 1
            elif tok.type == TokenType.RIGHT_PAREN:
                paren_count -= 1
                if paren_count == 0 and bracket_count == 0 and brace_count == 0:
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
                    # ✅ 최상위 레벨에서 콤마 발견 → 인자 구분
                    current_arg = arg2_tokens
                    i += 1
                    continue

            current_arg.append(tok)
            i += 1

        if paren_count != 0 or bracket_count != 0 or brace_count != 0:
            raise CustomTokenMakerError(
                f"Invalid {object_type.name} syntax: Unmatched grouping symbols",
                tokens[start_idx].line, tokens[start_idx].column
            )

        if not arg1_tokens or not arg2_tokens:
            raise CustomTokenMakerError(
                f"Invalid {object_type.name} syntax: Expected two arguments",
                tokens[start_idx].line, tokens[start_idx].column
            )

        # ✅ 해당 object_type에 맞는 토큰 생성
        if object_type == TokenType.POINT:
            result_token = PointToken(data=None)
            result_token.type = TokenType.POINT
        else:
            raise CustomTokenMakerError(
                f"Unknown two-argument token type: {object_type}",
                tokens[start_idx].line, tokens[start_idx].column
            )

        result_token.expressions = [arg1_tokens, arg2_tokens]
        result_token.line = tokens[start_idx].line
        result_token.column = tokens[start_idx].column

        return result_token, i   # `)` 다음 토큰 인덱스

    @staticmethod
    def _parse_four_arguments(tokens, start_idx, object_type):
        """✅ Rectangle(x1, y1, x2, y2) 또는 Region(x, y, w, h)처럼 4개의 인자를 처리"""

        if tokens[start_idx].type != object_type:
            raise CustomTokenMakerError(
                f"Invalid {object_type.name} syntax: Expected {object_type.name} at position {start_idx}",
                tokens[start_idx].line, tokens[start_idx].column
            )

        i = start_idx + 1
        if i >= len(tokens) or tokens[i].type != TokenType.LEFT_PAREN:
            raise CustomTokenMakerError(
                f"Invalid {object_type.name} syntax: Expected '(' after {object_type.name}",
                tokens[start_idx].line, tokens[start_idx].column
            )

        i += 1  # skip '('
        arg1, arg2, arg3, arg4 = [], [], [], []
        args = [arg1, arg2, arg3, arg4]
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
                    if arg_index >= 4:
                        raise CustomTokenMakerError(
                            f"Invalid {object_type.name} syntax: Too many arguments",
                            tokens[start_idx].line, tokens[start_idx].column
                        )
                    i += 1
                    continue

            args[arg_index].append(tok)
            i += 1

        if paren_count != 0 or bracket_count != 0 or brace_count != 0:
            raise CustomTokenMakerError(
                f"Invalid {object_type.name} syntax: Unmatched grouping symbols",
                tokens[start_idx].line, tokens[start_idx].column
            )

        if any(not arg for arg in args):
            raise CustomTokenMakerError(
                f"Invalid {object_type.name} syntax: Expected 4 arguments",
                tokens[start_idx].line, tokens[start_idx].column
            )

        # ✅ 객체 생성
        if object_type == TokenType.RECTANGLE:
            result_token = RectangleToken(data=None)
            result_token.type = TokenType.RECTANGLE
        elif object_type == TokenType.REGION:
            result_token = RegionToken(data=None)
            result_token.type = TokenType.REGION
        else:
            raise CustomTokenMakerError(
                f"Unknown four-argument token type: {object_type}",
                tokens[start_idx].line, tokens[start_idx].column
            )

        result_token.expressions = args
        result_token.line = tokens[start_idx].line
        result_token.column = tokens[start_idx].column

        return result_token, i 
