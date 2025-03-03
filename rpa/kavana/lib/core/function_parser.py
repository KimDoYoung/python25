from typing import List, Tuple
from lib.core.datatypes.kavana_datatype import String
from lib.core.exceptions.kavana_exception import FunctionParserError
from lib.core.function_registry import FunctionRegistry
from lib.core.token import FunctionToken, Token
from lib.core.token_type import TokenType

class FunctionParser:
    @staticmethod
    def parse(tokens):
        """토큰 리스트를 파싱하여 함수 호출을 처리"""
        stack = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            func_info = FunctionRegistry.get_function(token.upper())
            if func_info:
                # ✅ 함수 호출 감지
                func = None
                arg_count = func_info["arg_count"]
                combined_token, new_index = FunctionParser._func_tokens_to_string(tokens, i, func, arg_count)
                stack.append(combined_token)
                i = new_index  # ✅ 함수 호출 후 다음 토큰 위치로 이동
            else:
                # ✅ 일반 토큰 처리
                stack.append(token)
                i += 1
        return stack

    # @staticmethod
    # def _func_tokens_to_string(tokens, start_index, func, arg_count):
    #     """함수 호출을 파싱하여 하나의 토큰으로 합침 tokens plus,(,1,2,) -> plus(1,2)"""
    #     func_name = tokens[start_index].data.value.upper()
    #     i = start_index + 1
    #     args = []
    #     current_arg = []
    #     bracket_depth = 0  # ✅ 괄호 깊이 추적

    #     # ✅ 괄호가 있는 경우 처리 (예: my_func ( 3 4 ))
    #     if i < len(tokens) and tokens[i].type == TokenType.LEFT_PAREN: # '(' 인 경우
    #         bracket_depth += 1
    #         i += 1  # '(' 건너뛰기

    #         while i < len(tokens):
    #             if tokens[i].type == TokenType.LEFT_PAREN: # '(' 인 경우
    #                 bracket_depth += 1
    #                 func_info = FunctionRegistry.get_function(tokens[i - 1].data.value.upper())
    #                 if func_info:
    #                     # ✅ 중첩된 함수 호출 처리
    #                     nested_arg_count = func_info["arg_count"]
    #                     nested_token, i = FunctionParser._func_tokens_to_string(tokens, i - 1, None, nested_arg_count)
    #                     args.append(nested_token)
    #                     i -= 1
    #                     # current_arg의 마지막을 삭제
    #                     current_arg.pop()
    #                     bracket_depth-=1
    #                 else:
    #                     if current_arg and current_arg[-1].type not in (TokenType.LEFT_PAREN):
    #                         current_arg.append("")  # ✅ 이전 인자가 존재하고 마지막이 '(' 또는 ')'가 아닐 때 쉼표 추가                        
    #                     current_arg.append(str(tokens[i].data.value))

    #             elif tokens[i].type == TokenType.RIGHT_PAREN: # ')' 인 경우
    #                 bracket_depth -= 1
    #                 if bracket_depth == 0:
    #                     break  # ✅ 가장 바깥 괄호 닫힘
    #                 else:
    #                     current_arg.append(str(tokens[i].data.value))

    #             else:
    #                 if current_arg and current_arg[-1] not in ('('):
    #                     current_arg.append("")  # ✅ 이전 인자가 존재하고 마지막이 '(' 또는 ')'가 아닐 때 쉼표 추가
    #                 current_arg.append(str(tokens[i].data.value))
    #             i += 1  # ✅ 다음 토큰 이동

    #         if current_arg:
    #             args.append("".join(current_arg).strip())  # ✅ 마지막 인자 추가

    #         i += 1  # ')' 건너뛰기

    #     else:
    #         # ✅ 괄호 없는 경우 (예: my_func 3 4)
    #         while i < len(tokens) and len(args) < arg_count:
    #             func_info = FunctionRegistry.get_function(tokens[i].data.value.upper())
    #             if func_info:
    #                 # ✅ 중첩된 함수 호출 처리
    #                 nested_arg_count = func_info["arg_count"]
    #                 nested_token, i = FunctionParser._func_tokens_to_string(tokens, i, None, nested_arg_count)
    #                 args.append(nested_token)
    #             else:
    #                 args.append(tokens[i].data.value)
    #                 i += 1

    #     # ✅ 쉼표를 모든 인자 사이에 추가
    #     combined_token = Token(String(f"{func_name}({','.join(args)})"), TokenType.FUNCTION, start_index,0)
    #     return combined_token, i  # ✅ 새 위치 반환

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


    # @staticmethod
    # def make_function_token(tokens: List[Token], start_index: int) -> Tuple[FunctionToken, int]:
    #     """
    #     ✅ 함수 호출을 파싱하여 FunctionToken으로 변환
    #     - `tokens[start_index]`는 함수 이름이어야 한다.
    #     - `start_index`에서 시작하여 `FunctionToken`을 생성하고, `)` 이후의 위치 반환.
    #     """
    #     if not isinstance(tokens[start_index].data, String) :
    #         raise FunctionParserError(f"Expected function name, but got {tokens[start_index].data} at line {tokens[start_index].line}, column {tokens[start_index].column}")    
    #     func_name = tokens[start_index].data.value.upper()  # 함수명
    #     args = []
    #     i = start_index + 2  # ✅ '(' 이후부터 시작
    #     paren_depth = 1  # ✅ 괄호 깊이 추적

    #     arg_tokens = []  # ✅ 하나의 인자 그룹을 위한 임시 리스트

    #     while i < len(tokens) and paren_depth > 0:
    #         if tokens[i].type == TokenType.LEFT_PAREN:
    #             paren_depth += 1  # ✅ 중첩된 괄호 증가
    #         elif tokens[i].type == TokenType.RIGHT_PAREN:
    #             paren_depth -= 1  # ✅ 중첩된 괄호 감소
    #             if paren_depth == 0:  # ✅ 최상위 함수 호출 종료
    #                 break

    #         if tokens[i].type == TokenType.COMMA and paren_depth == 1:
    #             args.append(arg_tokens)  # ✅ 인자 저장
    #             arg_tokens = []  # ✅ 새로운 인자 그룹 시작
    #         else:
    #             arg_tokens.append(tokens[i])  # ✅ 현재 인자 그룹에 추가
            
    #         i += 1

    #     if arg_tokens:
    #         args.append(arg_tokens)  # ✅ 마지막 인자 저장

    #     return FunctionToken(function_name=func_name, arguments=args), i + 1
