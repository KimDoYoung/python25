import re
import operator
from typing import List, Union
from datetime import datetime, timedelta
from lib.core.function_executor import FunctionExecutor
from lib.core.function_parser import FunctionParser
from lib.core.function_registry import FunctionRegistry
from lib.core.variable_manager import VariableManager

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
        '!=': (0, operator.ne),
        'NOT': (-1, lambda a: not a),  # 단항 연산자
        'AND': (-2, lambda a, b: bool(a) and bool(b)),
        'OR':  (-3, lambda a, b: bool(a) or bool(b))        
    }
    
    def __init__(self, expression: str, var_manager: VariableManager):
        self.expression = expression
        self.var_manager = var_manager
    

    def tokenize(self) -> List[str]:
        """수식을 토큰 리스트로 변환 (문자열 유지)"""
    #   tokens = re.findall(r'<=|>=|==|!=|[-+]?[0-9]*\.?[0-9]+|"[^"]*"|[a-zA-Z_][a-zA-Z0-9_]*|[()+\-*/%,]', self.expression)
        # tokens = re.findall(
        #     r'<=|>=|==|!=|[<>]|[-+]?[0-9]*\.?[0-9]+|"[^"]*"|[a-zA-Z_][a-zA-Z0-9_]*|[()+\-*/%]', 
        #     self.expression
        # )        
        tokens = re.findall(
            r'<=|>=|==|!=|[<>]|[-+]?[0-9]*\.?[0-9]+|"[^"]*"|[a-zA-Z_][a-zA-Z0-9_]*|[(),+\-*/%]', 
            self.expression
        )   
        # 쉼표 제거
        tokens = [t for t in tokens if t != ","]
        
        # boolean 예약어를 대문자로 변환하여 토큰으로 처리 ("and", "or", "not")
        reserved = {"and", "or", "not"}
        tokens = [t.upper() if t.lower() in reserved else t for t in tokens]
        
        return tokens

    def to_postfix(self, tokens: List[str]) -> List[str]:
        """토큰 리스트를 후위 표기법(RPN)으로 변환"""
        output = []
        stack = []
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            # pluse ( 3 4 ) -> pluse(3,4)로 
            func_info = FunctionRegistry.get_function(token.upper())
            if func_info != None:
                arg_count = func_info["arg_count"]
                combined_token, i = FunctionParser._parse_function_call(tokens, start_index = i, func=None,  arg_count=arg_count)
                output.append(combined_token)
                continue

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
                if token == "NOT":
                    # NOT은 오른쪽 결합이므로, 우선순위가 '더 큰' 연산자만 pop합니다.
                    while (stack and stack[-1] in self.OPERATORS and
                        self.OPERATORS[token][0] < self.OPERATORS[stack[-1]][0]):
                        output.append(stack.pop())
                else:
                    # 이항 연산자는 왼쪽 결합: 우선순위가 같거나 큰 연산자 pop
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
            elif token == "NOT":
                # 단항 boolean not 연산자 처리
                a = stack.pop()
                result = self.OPERATORS[token][1](a)
                stack.append(result)                
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

            elif self.isFunction(token_upper):  
                func_tokens = self.split_function_token(token_upper)  
                func_info = FunctionRegistry.get_function(func_tokens[0])
                
                if func_info is None:
                    raise ValueError(f"Undefined function: {func_tokens[0]}")

                arg_values = func_tokens[1:]

                function_executor = FunctionExecutor(func_info, global_var_manager=self.var_manager, arg_values=arg_values)

                result = function_executor.execute()
                stack.append(result)  

            else:  
                value = self.var_manager.get_variable(token_upper)
                if value is None:
                    raise ValueError(f"Undefined variable: {token_upper}")
                stack.append(value)

        return stack[0]
    
    def split_function_token(self, function_token:str) -> List[str]:
        """function_token PLUS(3,4) -> PLUS,3,4 함수명과 인자로 분리"""
        if "(" not in function_token or not function_token.endswith(")"):
            return [function_token]  # 괄호가 없으면 그대로 반환

        func_name = function_token[:function_token.index("(")]  # ✅ 함수명 추출
        args_str = function_token[function_token.index("(") + 1:-1].strip()  # ✅ 괄호 안의 내용

        if not args_str:  # ✅ 빈 괄호 처리 (예: MY_FUNC())
            return [func_name]

        args = []
        current_arg = []
        bracket_depth = 0  # ✅ 괄호 깊이 추적

        i = 0
        while i < len(args_str):
            char = args_str[i]

            if char == "(":
                bracket_depth += 1
            elif char == ")":
                bracket_depth -= 1

            if char == "," and bracket_depth == 0:
                # ✅ 쉼표가 최상위 레벨에 있을 때만 인자 구분
                args.append("".join(current_arg).strip())
                current_arg = []
            else:
                current_arg.append(char)

            i += 1

        if current_arg:  # ✅ 마지막 인자 추가
            args.append("".join(current_arg).strip())

        return [func_name] + args

    def isFunction(self, token: str) -> bool:
        """토큰이 함수인지 확인 PLUS(3,4)"""
        func_name = token.upper()
        if "(" in token:
            func_name =  token[:token.index("(")]  # '(' 이전까지 잘라서 반환
        func_info = FunctionRegistry.get_function(func_name)
        return func_info != None

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

