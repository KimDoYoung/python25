import re
import operator
from typing import List, Union
from datetime import datetime, timedelta
from varaible_manager import VariableManager
from builtin_functions import BuiltinFunctions

class ExprEvaluator:
    OPERATORS = {
        '+': (1, operator.add),
        '-': (1, operator.sub),
        '*': (2, operator.mul),
        '/': (2, operator.truediv),
        '%': (2, operator.mod)
    }
    
    def __init__(self, expression: str, var_manager: VariableManager):
        self.expression = expression
        self.var_manager = var_manager
    
    def tokenize(self) -> List[str]:
        """수식을 토큰 리스트로 변환"""
        return re.findall(r'\".*?\"|\d+\.\d+|\d+|[a-zA-Z_][a-zA-Z0-9_]*|[()+\-*/%,]', self.expression)
    
    def to_postfix(self, tokens: List[str]) -> List[str]:
        """토큰 리스트를 후위 표기법(RPN)으로 변환"""
        output = []
        stack = []
        func_args = {}
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.isnumeric() or re.match(r'\d+\.\d+', token) or token.startswith('"'):
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
                if stack and stack[-1] in func_args:
                    output.append(stack.pop())
            elif i + 1 < len(tokens) and tokens[i + 1] == '(':  # 함수 호출 감지
                stack.append(token)
                func_args[token] = []
            else:
                output.append(token)
            i += 1
        
        while stack:
            output.append(stack.pop())
        
        return output
    
    def evaluate_postfix(self, tokens: List[str]) -> Union[int, float, str, datetime]:
        """후위 표기법 리스트를 계산"""
        stack = []
        
        for token in tokens:
            if token.isnumeric():
                stack.append(int(token))
            elif re.match(r'\d+\.\d+', token):
                stack.append(float(token))
            elif token.startswith('"') and token.endswith('"'):
                stack.append(token.strip('"'))  # 문자열 리터럴 처리
            elif token in self.OPERATORS:
                b = stack.pop()
                a = stack.pop()
                
                if token == '%' and not (isinstance(a, int) and isinstance(b, int)):
                    raise TypeError("Modulo operator '%' only supports integer operands")
                
                if isinstance(a, datetime) and isinstance(b, int):
                    result = a + timedelta(days=b) if token == '+' else a - timedelta(days=b)
                elif isinstance(a, datetime) and isinstance(b, datetime) and token == '-':
                    result = (a - b).days  # 날짜 차이 반환 (일 단위)
                elif isinstance(a, str) and isinstance(b, str) and token == '+':
                    result = a + b  # 문자열 연결 지원
                elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
                    result = self.OPERATORS[token][1](a, b)
                    result = int(result) if isinstance(a, int) and isinstance(b, int) else result
                else:
                    raise TypeError(f"Unsupported operand types: {type(a).__name__} and {type(b).__name__}")
                
                stack.append(result)
            elif hasattr(BuiltinFunctions, token.upper()):  # 함수 호출
                func = getattr(BuiltinFunctions, token.upper())
                args = []
                while stack and isinstance(stack[-1], (int, float, str, datetime)):
                    args.insert(0, stack.pop())
                stack.append(func(*args))
            else:
                value = self.var_manager.get_variable(token)
                if value is None:
                    raise ValueError(f"Undefined variable: {token}")
                stack.append(value)
        
        return stack[0]
    
    def evaluate(self) -> Union[int, float, str, datetime]:
        """수식을 계산하여 결과 반환"""
        tokens = self.tokenize()
        postfix_tokens = self.to_postfix(tokens)
        return self.evaluate_postfix(postfix_tokens)

# 테스트 코드
if __name__ == "__main__":
    var_manager = VariableManager()
    var_manager.set_variable("name", "hello")
    expr = "LENGTH(name) + 3"
    evaluator = ExprEvaluator(expr, var_manager)
    result = evaluator.evaluate()
    print(f"{expr} = {result}")
