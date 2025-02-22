import re
import operator
from typing import List, Union
from datetime import datetime, timedelta
from lib.core.function_registry import FunctionRegistry
from lib.core.variable_manager import VariableManager
from lib.core.builtin_functions import BuiltinFunctions


class ExprEvaluator:
    OPERATORS = {
        '+': (1, operator.add),
        '-': (1, operator.sub),
        '*': (2, operator.mul),
        '/': (2, operator.truediv),
        '%': (2, operator.mod),
        '>': (0, operator.gt),
        '<': (0, operator.lt),
        '>=': (0, operator.ge),
        '<=': (0, operator.le),
        '==': (0, operator.eq),
        '!=': (0, operator.ne)
    }
    
    def __init__(self, expression: str, var_manager: VariableManager):
        self.expression = expression
        self.var_manager = var_manager
    

    def tokenize(self) -> List[str]:
        """수식을 토큰 리스트로 변환 (문자열 유지)"""
    #   tokens = re.findall(r'<=|>=|==|!=|[-+]?[0-9]*\.?[0-9]+|"[^"]*"|[a-zA-Z_][a-zA-Z0-9_]*|[()+\-*/%,]', self.expression)
        tokens = re.findall(
            r'<=|>=|==|!=|[<>]|[-+]?[0-9]*\.?[0-9]+|"[^"]*"|[a-zA-Z_][a-zA-Z0-9_]*|[()+\-*/%]', 
            self.expression
        )        

        return [t for t in tokens if t != ","]  # ✅ 쉼표 제거    

    def to_postfix(self, tokens: List[str]) -> List[str]:
        """토큰 리스트를 후위 표기법(RPN)으로 변환"""
        output = []
        stack = []
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if isinstance(token, str) and token.replace('.', '', 1).lstrip('-').isdigit():
                token = float(token) if '.' in token else int(token)  # ✅ 문자열 숫자를 실제 숫자로 변환
                output.append(token)
                i+=1
                continue

            if isinstance(token, str) and token in ("True", "False", "None"):
                token = {"True": True, "False": False, "None": None}[token]            
                output.append(token)  # ✅ 예약어는 그대로 추가
                i+=1
                continue

            if isinstance(token, str) and token.startswith('"') and token.endswith('"'):
                output.append(token)  # ✅ 문자열 그대로 추가
                i+=1
                continue
            
            token_upper = token.upper() if isinstance(token, str) and token.isidentifier() else token  

            if token.replace('.', '', 1).lstrip('-').isdigit() or token.startswith('"'):
                output.append(token)
            elif token in self.OPERATORS:
                while (stack and stack[-1] in self.OPERATORS and
                    self.OPERATORS[token][0] <= self.OPERATORS[stack[-1]][0]):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()
                if stack and stack[-1].isalpha():
                    output.append(stack.pop())
            elif i + 1 < len(tokens) and tokens[i + 1] == '(':
                stack.append(token_upper)
            else:
                output.append(token_upper)
            i += 1
        
        while stack:
            output.append(stack.pop())
        
        return output

    def evaluate_postfix(self, tokens: List[str]) -> Union[int, float, str, datetime]:
        """후위 표기법 리스트를 계산 (날짜 연산 및 문자열 연산 강화)"""
        stack = []
        
        for token in tokens:
            
            if token in (True, False, None):  # ✅ 변환된 예약어는 그대로 스택에 추가
                stack.append(token)
                continue
            if isinstance(token, (int, float)):  # ✅ 숫자는 그대로 스택에 추가
                stack.append(token)
                continue
            if isinstance(token, str) and token.startswith('"') and token.endswith('"'):
                stack.append(token.strip('"'))  # ✅ 문자열을 변수명이 아니라 문자열로 처리
                continue

            token_upper = token.upper() if isinstance(token, str) and token.isidentifier() else token  

            if token == ",":
                continue  # ✅ 쉼표 무시

            if isinstance(token, str) and token.replace('.', '', 1).lstrip('-').isdigit():
                stack.append(float(token) if '.' in token else int(token))
            elif token in self.OPERATORS:
                b = stack.pop()
                a = stack.pop()
                if token == '%':
                    if not isinstance(a, int) or not isinstance(b, int):
                        raise ValueError(f"Unsupported operand types for %: {type(a).__name__} and {type(b).__name__}")
                    result = a % b
                elif isinstance(a, datetime) and isinstance(b, int):
                    result = a + timedelta(days=b) if token == '+' else a - timedelta(days=b)
                elif isinstance(a, datetime) and isinstance(b, datetime) and token == '-':
                    result = (a - b).days  # ✅ 날짜 차이 연산 지원
                elif isinstance(a, str) and isinstance(b, str) and token == '+':
                    result = a + b  # ✅ 문자열 연결 지원
                elif (a is None or b is None) and token in ('==', '!='):  # ✅ None 비교 연산 지원
                    result = self.OPERATORS[token][1](a, b)
                elif isinstance(a, str) or isinstance(b, str):
                    if token not in ('==', '!='):
                        raise ValueError(f"Unsupported operation between strings: '{a}' {token} '{b}'")
                    result = self.OPERATORS[token][1](a, b)
                elif isinstance(a, (int, float, bool)) and isinstance(b, (int, float, bool)):
                    result = self.OPERATORS[token][1](a, b)
                else:
                    raise TypeError(f"Unsupported operand types: {type(a).__name__} and {type(b).__name__}")

                stack.append(result)

            elif FunctionRegistry.get_function(token_upper):
                func_info = FunctionRegistry.get_function(token_upper)
                if isinstance(func_info, dict):  # ✅ 사용자 정의 함수일 경우
                    param_names = func_info["params"]
                    func_body = func_info["body"]

                    # ✅ 스택에서 필요한 인자 개수만큼 꺼내서 실행 환경 구성
                    local_vars = {param: stack.pop() for param in reversed(param_names)}

                    # ✅ 사용자 함수 실행 (간단한 해석기 사용)
                    result = self.execute_user_function(func_body, local_vars)
                else:  # ✅ 내장 함수일 경우
                    if isinstance(func_info, staticmethod):
                        func_info = func_info.__func__  # ✅ 정적 메서드 실행 가능하도록 변환

                    required_args = func_info.__code__.co_argcount
                    if len(stack) < required_args:
                        raise ValueError(f"Not enough arguments for function: {token_upper}")
                    pos_args = [stack.pop() for _ in range(required_args)]
                    result = func_info(*reversed(pos_args))

                stack.append(result)

            else:
                value = self.var_manager.get_variable(token_upper)
                if value is None:
                    raise ValueError(f"Undefined variable: {token_upper}")  # ✅ 대소문자 오류 수정
                stack.append(value)

        return stack[0]


    def execute_user_function(self, func_body: str, local_vars: dict):
        """
        간단한 사용자 정의 함수 실행기
        - 현재는 간단한 RETURN 문만 지원
        """
        if func_body.startswith("RETURN "):
            expr = func_body[len("RETURN "):].strip()
            evaluator = ExprEvaluator(expr, VariableManager())  # ✅ 새로운 평가기 생성
            evaluator.var_manager.variables.update(local_vars)  # ✅ 지역 변수 전달
            return evaluator.evaluate()
        raise ValueError(f"Unsupported function body: {func_body}")


    def evaluate(self) -> Union[int, float, str, datetime]:
        """수식을 계산하여 결과 반환 (예외 처리 강화)"""
        try:
            tokens = self.tokenize()
            postfix_tokens = self.to_postfix(tokens)
            return self.evaluate_postfix(postfix_tokens)
        except Exception as e:
            raise ValueError(f"Error evaluating expression '{self.expression}': {str(e)}")

