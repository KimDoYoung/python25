from lib.core.function_registry import FunctionRegistry


class FunctionParser:
    @staticmethod
    def parse(tokens):
        """토큰 리스트를 파싱하여 함수 호출을 처리"""
        stack = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            func, arg_count = FunctionRegistry.get_function(token.upper())
            if func:
                # 함수 호출 감지
                combined_token, i = FunctionParser._parse_function_call(tokens, i, func, arg_count)
                stack.append(combined_token)
            else:
                # 일반 토큰 처리
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

        # 괄호가 있는 경우와 없는 경우 처리
        if i < len(tokens) and tokens[i] == '(':
            i += 1  # '(' 건너뛰기
            while i < len(tokens) and tokens[i] != ')':
                # 중첩된 함수 호출 처리
                nested_func, nested_arg_count = FunctionRegistry.get_function(tokens[i].upper())
                if nested_func:
                    nested_token, i = FunctionParser._parse_function_call(tokens, i, nested_func, nested_arg_count)
                    current_arg.append(nested_token)
                else:
                    current_arg.append(tokens[i])
                i += 1
            # 마지막 인자 추가
            if current_arg:
                args.append(''.join(current_arg).strip())
            i += 1  # ')' 건너뛰기
        else:
            # 괄호가 없는 경우 (예: my_func 3 4)
            while i < len(tokens) and len(args) < arg_count:
                args.append(tokens[i])
                i += 1

        # 인자 개수 확인
        if len(args) != arg_count:
            raise ValueError(f"Function {func_name} expects {arg_count} arguments, but got {len(args)}")

        # 함수와 인자를 하나의 토큰으로 합침
        combined_token = f"{func_name}({','.join(args)})"
        return combined_token, i