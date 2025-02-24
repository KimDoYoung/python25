from lib.core.function_registry import FunctionRegistry

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
                combined_token, new_index = FunctionParser._parse_function_call(tokens, i, func, arg_count)
                stack.append(combined_token)
                i = new_index  # ✅ 함수 호출 후 다음 토큰 위치로 이동
            else:
                # ✅ 일반 토큰 처리
                stack.append(token)
                i += 1
        return stack

    @staticmethod
    def _parse_function_call(tokens, start_index, func, arg_count):
        """함수 호출을 파싱하여 하나의 토큰으로 합침"""
        func_name = tokens[start_index].upper()
        i = start_index + 1
        args = []
        current_arg = []
        bracket_depth = 0  # ✅ 괄호 깊이 추적

        # ✅ 괄호가 있는 경우 처리 (예: my_func ( 3 4 ))
        if i < len(tokens) and tokens[i] == '(':
            bracket_depth += 1
            i += 1  # '(' 건너뛰기

            while i < len(tokens):
                if tokens[i] == '(':
                    bracket_depth += 1
                    func_info = FunctionRegistry.get_function(tokens[i - 1].upper())
                    if func_info:
                        # ✅ 중첩된 함수 호출 처리
                        nested_arg_count = func_info["arg_count"]
                        nested_token, i = FunctionParser._parse_function_call(tokens, i - 1, None, nested_arg_count)
                        args.append(nested_token)
                        i -= 1
                        # current_arg의 마지막을 삭제
                        current_arg.pop()
                        bracket_depth-=1
                    else:
                        if current_arg and current_arg[-1] not in ('('):
                            current_arg.append(",")  # ✅ 이전 인자가 존재하고 마지막이 '(' 또는 ')'가 아닐 때 쉼표 추가                        
                        current_arg.append(tokens[i])

                elif tokens[i] == ')':
                    bracket_depth -= 1
                    if bracket_depth == 0:
                        break  # ✅ 가장 바깥 괄호 닫힘
                    else:
                        current_arg.append(tokens[i])

                else:
                    if current_arg and current_arg[-1] not in ('('):
                        current_arg.append(",")  # ✅ 이전 인자가 존재하고 마지막이 '(' 또는 ')'가 아닐 때 쉼표 추가
                    current_arg.append(tokens[i])
                i += 1  # ✅ 다음 토큰 이동

            if current_arg:
                args.append("".join(current_arg).strip())  # ✅ 마지막 인자 추가

            i += 1  # ')' 건너뛰기

        else:
            # ✅ 괄호 없는 경우 (예: my_func 3 4)
            while i < len(tokens) and len(args) < arg_count:
                func_info = FunctionRegistry.get_function(tokens[i].upper())
                if func_info:
                    # ✅ 중첩된 함수 호출 처리
                    nested_arg_count = func_info["arg_count"]
                    nested_token, i = FunctionParser._parse_function_call(tokens, i, None, nested_arg_count)
                    args.append(nested_token)
                else:
                    args.append(tokens[i])
                    i += 1

        # ✅ 쉼표를 모든 인자 사이에 추가
        combined_token = f"{func_name}({','.join(args)})"
        return combined_token, i  # ✅ 새 위치 반환
