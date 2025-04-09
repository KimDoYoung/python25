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
        i = start_idx + 1
        has_parentheses = False

        if i < len(tokens) and tokens[i].type == TokenType.LEFT_PAREN:
            has_parentheses = True
            i += 1  # `(` 스킵

        arguments = []

        # ✅ x 값 체크
        if i >= len(tokens) or tokens[i].type != TokenType.INTEGER:
            raise CustomTokenMakerError(
                f"Invalid POINT syntax: Expected number at position {i}",
                tokens[start_idx].line, tokens[start_idx].column
            )
        arguments.append([tokens[i]])  # ✅ List[List[Token]] 구조로 저장
        i += 1

        # ✅ 쉼표 체크
        if i < len(tokens) and tokens[i].type == TokenType.COMMA:
            i += 1  # 쉼표 스킵

        # ✅ y 값 체크
        if i >= len(tokens) or tokens[i].type != TokenType.INTEGER:
            raise CustomTokenMakerError(
                f"Invalid POINT syntax: Expected number at position {i}",
                tokens[start_idx].line, tokens[start_idx].column
            )
        arguments.append([tokens[i]])  # ✅ List[List[Token]] 구조 유지
        i += 1

        if has_parentheses:
            if i >= len(tokens) or tokens[i].type != TokenType.RIGHT_PAREN:
                raise CustomTokenMakerError(
                    f"Invalid POINT syntax: Expected ')' at position {i}",
                    tokens[start_idx].line, tokens[start_idx].column
                )
            i += 1  # `)` 스킵

        point_token = PointToken(data=None)
        point_token.type = TokenType.POINT  # ✅ 타입 설정
        point_token.expressions = arguments  # ✅ List[List[Token]] 구조 유지
        point_token.line = tokens[start_idx].line
        point_token.column = tokens[start_idx].column
        return point_token, i


    @staticmethod
    def rectangle_token(tokens, start_idx):
        """✅ `Rectangle(x, y, width, height)` 또는 `Rectangle x, y, width, height` 형식을 처리"""
        i = start_idx + 1
        has_parentheses = False

        if i < len(tokens) and tokens[i].type == TokenType.LEFT_PAREN:
            has_parentheses = True
            i += 1  # `(` 스킵

        arguments = []

        # ✅ x, y, width, height 개별 체크 & List[List[Token]] 형태 유지
        for param in ["x", "y", "width", "height"]:
            if i >= len(tokens) or tokens[i].type != TokenType.INTEGER:
                raise CustomTokenMakerError(
                    f"Invalid RECTANGLE syntax: Expected {param} at position {i}",
                    tokens[start_idx].line,
                    tokens[start_idx].column
                )

            arguments.append([tokens[i]])  # ✅ 개별 리스트로 감싸기
            i += 1

            if param != "height" and i < len(tokens) and tokens[i].type == TokenType.COMMA:
                i += 1  # 쉼표 스킵

        if has_parentheses:
            if i >= len(tokens) or tokens[i].type != TokenType.RIGHT_PAREN:
                raise CustomTokenMakerError(
                    f"Invalid RECTANGLE syntax: Expected ')' at position {i}",
                    tokens[start_idx].line,
                    tokens[start_idx].column
                )
            i += 1  # `)` 스킵
        rectangle_token = RectangleToken(data=None)
        rectangle_token.type = TokenType.RECTANGLE
        rectangle_token.expressions = arguments
        rectangle_token.line = tokens[start_idx].line
        rectangle_token.column = tokens[start_idx].column
        return rectangle_token, i

    @staticmethod
    def image_token(tokens, start_idx):
        """✅ `Image("path")` 또는 `Image "path"` 형식을 처리"""
        i = start_idx + 1
        has_parentheses = False

        if i < len(tokens) and tokens[i].type == TokenType.LEFT_PAREN:
            has_parentheses = True
            i += 1  # `(` 스킵

        if i >= len(tokens) or tokens[i].type != TokenType.STRING:
            raise CustomTokenMakerError(
                f"Invalid IMAGE syntax: Expected string at position {i}",
                tokens[start_idx].line, tokens[start_idx].column
            )

        arguments = [[tokens[i]]]  # ✅ List[List[Token]] 구조 유지
        i += 1

        if has_parentheses:
            if i >= len(tokens) or tokens[i].type != TokenType.RIGHT_PAREN:
                raise CustomTokenMakerError(
                    f"Invalid IMAGE syntax: Expected ')' at position {i}",
                    tokens[start_idx].line, tokens[start_idx].column
                )
            i += 1  # `)` 스킵

        image_token = ImageToken(data=None)
        image_token.type = TokenType.IMAGE  # ✅ 타입 설정
        image_token.expressions = arguments  # ✅ List[List[Token]] 구조 유지
        image_token.line = tokens[start_idx].line
        image_token.column = tokens[start_idx].column
        return image_token, i
    

    @staticmethod
    def window_token(tokens, start_idx):
        """✅ `Window("title")` 또는 `Window "title"` 형식을 처리"""
        return CustomTokenMaker._parse_single_string(tokens, start_idx, TokenType.WINDOW)

    @staticmethod
    def application_token(tokens, start_idx):
        """✅ `Application("name")` 또는 `Application "name"` 형식을 처리"""
        return CustomTokenMaker._parse_single_string(tokens, start_idx, TokenType.APPLICATION)

    @staticmethod
    def _parse_single_string(tokens, start_idx, object_type):
        """✅ 공통 문자열 처리"""
        i = start_idx + 1
        has_parentheses = False

        if i < len(tokens) and tokens[i].type == TokenType.LEFT_PAREN:
            has_parentheses = True
            i += 1  # `(` 스킵

        arguments = [[tokens[i]]]  # ✅ List[List[Token]] 구조로 변경
        i += 1

        if has_parentheses:
            if i >= len(tokens) or tokens[i].type != TokenType.RIGHT_PAREN:
                raise CustomTokenMakerError(
                    f"Invalid {object_type.name} syntax: Expected ')' at position {i}",
                    tokens[start_idx].line, tokens[start_idx].column
                )
            i += 1  # `)` 스킵
        if object_type == TokenType.WINDOW:
            result_token = WindowToken(data=None)
            result_token.type = TokenType.WINDOW  # ✅ 타입 설정
        elif object_type == TokenType.APPLICATION:
            result_token = ApplicationToken(data=None)
            result_token.type = TokenType.APPLICATION
        else:
            raise CustomTokenMakerError(f"Unknown object type: {object_type}", tokens[start_idx].line, tokens[start_idx].column)
        result_token.expressions = arguments 
        result_token.line = tokens[start_idx].line
        result_token.column = tokens[start_idx].column
        return result_token, i

    @staticmethod
    def region_token(tokens, start_idx):
        """✅ `Region(x, y, width, height)` 또는 `Region x, y, width, height` 형식을 처리"""
        i = start_idx + 1
        has_parentheses = False

        if i < len(tokens) and tokens[i].type == TokenType.LEFT_PAREN:
            has_parentheses = True
            i += 1  # `(` 스킵

        arguments = []

        # ✅ x, y, width, height 개별 체크 & List[List[Token]] 형태 유지
        for param in ["x", "y", "width", "height"]:
            if i >= len(tokens) or tokens[i].type != TokenType.INTEGER:
                raise CustomTokenMakerError(
                    f"Invalid REGION syntax: Expected {param} at position {i}",
                    tokens[start_idx].line,
                    tokens[start_idx].column
                )

            arguments.append([tokens[i]])  # ✅ 개별 리스트로 감싸기
            i += 1

            if param != "height" and i < len(tokens) and tokens[i].type == TokenType.COMMA:
                i += 1  # 쉼표 스킵

        if has_parentheses:
            if i >= len(tokens) or tokens[i].type != TokenType.RIGHT_PAREN:
                raise CustomTokenMakerError(
                    f"Invalid REGION syntax: Expected ')' at position {i}",
                    tokens[start_idx].line,
                    tokens[start_idx].column
                )
            i += 1  # `)` 스킵
        region_token = RegionToken(data=None)
        region_token.type = TokenType.REGION
        region_token.expressions = arguments
        region_token.line = tokens[start_idx].line
        region_token.column = tokens[start_idx].column
        return region_token, i
