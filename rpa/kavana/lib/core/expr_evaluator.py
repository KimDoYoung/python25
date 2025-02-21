import re
import operator
from typing import List, Union
from datetime import datetime, timedelta
from lib.core.variable_manager import VariableManager
from lib.core.builtin_functions import BuiltinFunctions
from lib.core.function_parser import FunctionParser

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
        """수식을 토큰 리스트로 변환 (단항 연산자 및 날짜 지원 추가)"""
        tokens = re.findall(r'-?\d+\.\d+|-?\d+|".*?"|[a-zA-Z_][a-zA-Z0-9_]*|[()+\-*/%,]', self.expression)
        return [t for t in tokens if t != ","]  # ✅ 쉼표 제거
    
    def to_postfix(self, tokens: List[str]) -> List[str]:
        """토큰 리스트를 후위 표기법(RPN)으로 변환"""
        output = []
        stack = []
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            token_upper = token.upper() if token.isidentifier() else token  

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
            token_upper = token.upper() if token.isidentifier() else token  
            
            if token == ",":
                continue  # ✅ 쉼표 무시
            
            if token.replace('.', '', 1).lstrip('-').isdigit():
                stack.append(float(token) if '.' in token else int(token))
            elif token.startswith('"') and token.endswith('"'):
                stack.append(token.strip('"'))
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
                elif isinstance(a, str) or isinstance(b, str):
                    raise ValueError(f"Unsupported operation between strings: '{a}' {token} '{b}'")
                elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
                    result = self.OPERATORS[token][1](a, b)
                else:
                    raise TypeError(f"Unsupported operand types: {type(a).__name__} and {type(b).__name__}")
                stack.append(result)
            elif hasattr(BuiltinFunctions, token_upper):
                func = getattr(BuiltinFunctions, token_upper)
                required_args = func.__code__.co_argcount
                pos_args = [stack.pop() for _ in range(required_args)]
                result = func(*reversed(pos_args))
                stack.append(result)
            else:
                value = self.var_manager.get_variable(token_upper)
                if value is None:
                    raise ValueError(f"Undefined variable: {token}")
                stack.append(value)
        
        return stack[0]
    
    def evaluate(self) -> Union[int, float, str, datetime]:
        """수식을 계산하여 결과 반환 (예외 처리 강화)"""
        try:
            tokens = self.tokenize()
            postfix_tokens = self.to_postfix(tokens)
            return self.evaluate_postfix(postfix_tokens)
        except Exception as e:
            raise ValueError(f"Error evaluating expression '{self.expression}': {str(e)}")

#---------------------------------------------------------------
#---------------------------------------------------------------
# import re
# import operator
# from typing import List, Union
# from datetime import datetime, timedelta
# from lib.core.variable_manager import VariableManager
# from lib.core.builtin_functions import BuiltinFunctions
# from lib.core.function_parser import FunctionParser

# class ExprEvaluator:
#     OPERATORS = {
#         '+': (1, operator.add),
#         '-': (1, operator.sub),
#         '*': (2, operator.mul),
#         '/': (2, operator.truediv),
#         '%': (2, operator.mod)
#     }
    
#     def __init__(self, expression: str, var_manager: VariableManager):
#         self.expression = expression
#         self.var_manager = var_manager
    
#     def tokenize(self) -> List[str]:
#         """수식을 토큰 리스트로 변환"""
#         tokens = re.findall(r'\".*?\"|\d+\.\d+|\d+|[a-zA-Z_][a-zA-Z0-9_]*|[()+\-*/%,]', self.expression)
#         return [t for t in tokens if t != ","]  # ✅ 쉼표 제거
    
#     def to_postfix(self, tokens: List[str]) -> List[str]:
#         """토큰 리스트를 후위 표기법(RPN)으로 변환"""
#         output = []
#         stack = []
        
#         i = 0
#         while i < len(tokens):
#             token = tokens[i]
#             # token_upper = token.upper()  # ✅ 대소문자 무시
#             token_upper = token.upper() if token.isidentifier() else token  

#             if token.isnumeric() or re.match(r'\d+\.\d+', token) or token.startswith('"'):
#                 output.append(token)
#             elif token in self.OPERATORS:
#                 while (stack and stack[-1] in self.OPERATORS and
#                        self.OPERATORS[token][0] <= self.OPERATORS[stack[-1]][0]):
#                     output.append(stack.pop())
#                 stack.append(token)
#             elif token == '(':
#                 stack.append(token)
#             elif token == ')':
#                 while stack and stack[-1] != '(':
#                     output.append(stack.pop())
#                 stack.pop()
#                 if stack and stack[-1].isalpha():
#                     output.append(stack.pop())
#             elif i + 1 < len(tokens) and tokens[i + 1] == '(':  # 함수 호출 감지
#                 stack.append(token_upper)
#             else:
#                 output.append(token_upper)
#             i += 1
        
#         while stack:
#             output.append(stack.pop())
        
#         return output
    
#     def evaluate_postfix(self, tokens: List[str]) -> Union[int, float, str, datetime]:
#         """후위 표기법 리스트를 계산"""
#         stack = []
        
#         for token in tokens:
#             token_upper = token.upper() if token.isidentifier() else token  
            
#             if token == ",":
#                 continue  # ✅ 쉼표 무시
            
#             if token.isnumeric():
#                 stack.append(int(token))
#             elif re.match(r'\d+\.\d+', token):
#                 stack.append(float(token))
#             elif token.startswith('"') and token.endswith('"'):
#                 stack.append(token.strip('"'))  # ✅ 문자열 따옴표 제거
#             elif token in self.OPERATORS:
#                 b = stack.pop()
#                 a = stack.pop()

#                 # ✅ 문자열 연산 예외 처리
#                 if isinstance(a, str) or isinstance(b, str):
#                     if token != '+':  # ✅ 문자열 연결만 허용
#                         raise TypeError(f"Unsupported operation: {a} {token} {b}")

#                 # ✅ 문자열 + 문자열 (문자열 연결 지원)
#                 if isinstance(a, str) and isinstance(b, str) and token == '+':
#                     result = a + b

#                 # ✅ 날짜 연산 지원 (datetime + int, datetime - int)
#                 elif isinstance(a, datetime) and isinstance(b, int):
#                     if token == '+':
#                         result = a + timedelta(days=b)
#                     elif token == '-':
#                         result = a - timedelta(days=b)
#                     else:
#                         raise TypeError(f"Unsupported operation: {a} {token} {b}")

#                 # ✅ 날짜 차이 계산 (datetime - datetime)
#                 elif isinstance(a, datetime) and isinstance(b, datetime) and token == '-':
#                     result = (a - b).days  # 날짜 차이 (일 단위)

#                 elif token == '%':
#                     if not isinstance(a, int) or not isinstance(b, int):
#                         raise TypeError(f"Unsupported operand types for %: {type(a).__name__} and {type(b).__name__}")
#                     result = a % b  # ✅ 정수 나머지 연산 수행
                
#                 # ✅ 일반 숫자 연산 (int, float)
#                 elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
#                     result = self.OPERATORS[token][1](a, b)
#                     result = int(result) if isinstance(a, int) and isinstance(b, int) else result

#                 # ❌ 지원하지 않는 연산 예외 발생
#                 else:
#                     raise TypeError(f"Unsupported operand types: {type(a).__name__} and {type(b).__name__}")

#                 stack.append(result)


#             elif hasattr(BuiltinFunctions, token_upper):  # ✅ 함수 호출 처리
#                 func = getattr(BuiltinFunctions, token_upper)

#                 # ✅ 스택에서 필요한 인자 개수만큼 꺼내기
#                 parser = FunctionParser(f"{token_upper}({', '.join(map(str, stack))})")
#                 pos_args, kw_args = parser.parse_arguments()

#                 result = func(*pos_args, **kw_args)  # ✅ 함수 실행
#                 stack.clear()  # ✅ 스택 비우고 결과만 남김
#                 stack.append(result)

#             else:
#                 value = self.var_manager.get_variable(token_upper)
#                 if value is None:
#                     raise ValueError(f"Undefined variable: {token}")
#                 stack.append(value)
    
#         return stack[0]
    
#     def evaluate(self) -> Union[int, float, str, datetime]:
#         """수식을 계산하여 결과 반환"""
#         tokens = self.tokenize()
#         postfix_tokens = self.to_postfix(tokens)
#         return self.evaluate_postfix(postfix_tokens)

