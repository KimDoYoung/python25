from typing import List, Tuple
from lib.core.datatypes.kavana_datatype import String
from lib.core.exceptions.kavana_exception import FunctionParserError
from lib.core.function_registry import FunctionRegistry
from lib.core.token import FunctionToken, Token
from lib.core.token_type import TokenType

class FunctionParser:
    # @staticmethod
    # def parse(tokens):
    #     """토큰 리스트를 파싱하여 함수 호출을 처리"""
    #     stack = []
    #     i = 0
    #     while i < len(tokens):
    #         token = tokens[i]
    #         func_info = FunctionRegistry.get_function(token.upper())
    #         if func_info:
    #             # ✅ 함수 호출 감지
    #             func = None
    #             arg_count = func_info["arg_count"]
    #             combined_token, new_index = FunctionParser._func_tokens_to_string(tokens, i, func, arg_count)
    #             stack.append(combined_token)
    #             i = new_index  # ✅ 함수 호출 후 다음 토큰 위치로 이동
    #         else:
    #             # ✅ 일반 토큰 처리
    #             stack.append(token)
    #             i += 1
    #     return stack

    @staticmethod
    def make_function_token(tokens: List[Token], start_index: int) -> Tuple[FunctionToken, int]:
        """
        ✅ 함수 호출을 파싱하여 FunctionToken으로 변환
        - `tokens[start_index]`는 함수 이름이어야 한다.
        - `start_index`에서 시작하여 `FunctionToken`을 생성하고, `)` 이후의 위치 반환.
        """
        if not isinstance(tokens[start_index].data, String):
            raise FunctionParserError(f"Expected function name, but got {tokens[start_index].data} at line {tokens[start_index].line}, column {tokens[start_index].column}")    

        func_name = tokens[start_index].data.value.upper()  # ✅ 함수명
        args = []
        i = start_index + 2  # ✅ '(' 이후부터 시작
        paren_depth = 1  # ✅ 괄호 깊이 추적

        arg_tokens = []  # ✅ 하나의 인자 그룹을 위한 임시 리스트

        while i < len(tokens) and paren_depth > 0:
            if tokens[i].type == TokenType.LEFT_PAREN:
                paren_depth += 1  # ✅ 중첩된 괄호 증가
            elif tokens[i].type == TokenType.RIGHT_PAREN:
                paren_depth -= 1  # ✅ 중첩된 괄호 감소
                if paren_depth == 0:  # ✅ 최상위 함수 호출 종료
                    break
            if tokens[i].type == TokenType.COMMA and paren_depth == 1:
                args.append(arg_tokens)  # ✅ 인자 저장
                arg_tokens = []  # ✅ 새로운 인자 그룹 시작
            else:
                arg_tokens.append(tokens[i])  # ✅ 현재 인자 그룹에 추가
            
            i += 1

        if arg_tokens:
            args.append(arg_tokens)  # ✅ 마지막 인자 저장

        return FunctionToken(function_name=func_name, arguments=args), i + 1
