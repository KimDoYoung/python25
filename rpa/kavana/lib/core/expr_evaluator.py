import re
import operator
from tkinter import Image
from typing import List, Union
from datetime import datetime, timedelta
from lib.core.datatypes.application import Application
from lib.core.datatypes.kavana_datatype import Boolean, Date, Float, Integer, KavanaDataType, String
from lib.core.datatypes.point import Point
from lib.core.datatypes.rectangle import Rectangle
from lib.core.datatypes.region import Region
from lib.core.datatypes.window import Window
from lib.core.exceptions.kavana_exception import ExprEvaluationError
from lib.core.token_type import TokenType
from lib.core.function_executor import FunctionExecutor
from lib.core.function_parser import FunctionParser
from lib.core.function_registry import FunctionRegistry
from lib.core.token import Token
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
    
    def __init__(self,  var_manager: VariableManager):
        self.var_manager = var_manager

    def to_postfix(self, tokens: List[Token]) -> List[Token]:
        """토큰 리스트를 후위 표기법(RPN)으로 변환"""
        output = []
        stack = []

        i = 0
        while i < len(tokens):
            token = tokens[i]

            # ✅ 함수 처리 (PLUSE(3,4) 형태)
            if token.type == TokenType.IDENTIFIER :
                func_info = FunctionRegistry.get_function(token.data)
                if func_info is not None:
                    arg_count = func_info["arg_count"]
                    combined_token, i = FunctionParser._parse_function_call(tokens, start_index=i, func=None, arg_count=arg_count)
                    output.append(combined_token)
                    continue

            # ✅ token.type 이 KavanaDataType이면 그대로 출력
            if isinstance(token.data, KavanaDataType):
                output.append(token)
                i += 1
                continue

            # ✅ 연산자 처리
            if token.type == TokenType.OPERATOR:
                if token.data == "NOT":
                    # NOT은 오른쪽 결합, 우선순위가 더 높은 연산자만 pop
                    while stack and stack[-1].type == TokenType.OPERATOR and self.OPERATORS[token.data][0] < self.OPERATORS[stack[-1].data][0]:
                        output.append(stack.pop())
                else:
                    # 일반 이항 연산자는 왼쪽 결합, 우선순위가 같거나 높은 연산자 pop
                    while stack and stack[-1].type == TokenType.OPERATOR and self.OPERATORS[token.data][0] <= self.OPERATORS[stack[-1].data][0]:
                        output.append(stack.pop())
                stack.append(token)
                i += 1
                continue

            # ✅ 괄호 처리
            if token.type == TokenType.LEFT_PAREN:
                stack.append(token)
            elif token.type == TokenType.RIGHT_PAREN:
                while stack and stack[-1].type != TokenType.LEFT_PAREN:
                    output.append(stack.pop())
                stack.pop()  # '(' 제거
            elif i + 1 < len(tokens) and tokens[i + 1].type == TokenType.LEFT_PAREN:
                stack.append(token)  # 함수 호출 (ex: FUNC(...))

            else:
                output.append(token)

            i += 1

        # ✅ 스택에 남은 연산자 추가
        while stack:
            output.append(stack.pop())

        return output


    def evaluate_postfix(self, tokens: List[Token]) -> Token:
        """후위 표기법 수식을 계산"""
        stack = []

        for token in tokens:

            if isinstance(token.data, KavanaDataType):  # ✅ Kavana 데이터 타입이면 그대로 스택에 추가
                stack.append(token)
            
            elif token.type == TokenType.IDENTIFIER:
                valueToken = self.var_manager.get_variable(token.data)
                if valueToken is None:
                    raise ValueError(f"Undefined variable: {token.data}")
                
                stack.append(valueToken)

            elif token.type == TokenType.OPERATOR:
                if token.data == "NOT":
                    a = stack.pop()
                    result = self.OPERATORS[token.data][1](a.data)
                    stack.append(Token(result, TokenType.BOOLEAN, line=token.line, column=token.column))
                # elif token.value  == "=":
                #     b = stack.pop()
                #     a = stack.pop()
                #     if a.type != TokenType.IDENTIFIER:
                #         raise ValueError(f"Invalid assignment target: {a.value}")
                #     self.var_manager.set_variable(a.value, b)
                #     stack.append(b)
                else:
                    b = stack.pop()
                    a = stack.pop()
                    result_type = TokenType.UNKNOWN
                    if token.data == "%":
                        if not a.type == TokenType.INTEGER or not b.type == TokenType.INTEGER:
                            raise ExprEvaluationError(f"Unsupported operand types for %: {a.type} and {b.type}")
                        result = Integer(a.data.value % b.data.value)
                        result_type = TokenType.INTEGER
                    elif a.type == TokenType.DATE and b.type == TokenType.INTEGER:
                        result = a.data.value + timedelta(days=b.data.value) if token.data == "+" else a.data.value - timedelta(days=b.data.value)
                        result = Date(result)
                        result_type = TokenType.DATE
                    elif a.type == TokenType.DATE and b.type == TokenType.DATE and token.data == "-":
                        result = (a.data.value - b.data.value).days
                        result = Date(result)
                        result_type = TokenType.DATE
                    elif a.type == TokenType.STRING and b.type == TokenType.STRING and token.data == "+":
                        result = String(a.data.value + b.data.value)
                        result_type = TokenType.STRING
                    elif (a.type == TokenType.NONE or b.type == TokenType.NONE) and token.data in {"==", "!="}:
                        result = self.OPERATORS[token.data][1](a.data.value, b.data.value)
                        result_type = TokenType.BOOLEAN
                    elif a.type in {TokenType.INTEGER, TokenType.FLOAT, TokenType.BOOLEAN} and b.type in {TokenType.INTEGER, TokenType.FLOAT, TokenType.BOOLEAN}:
                        result = self.OPERATORS[token.data][1](a.data.value, b.data.value)
                        # ✅ 비교 연산자일 경우 결과는 항상 BOOLEAN
                        if token.data in {"==", "!=", ">", "<", ">=", "<="}:
                            result_type = TokenType.BOOLEAN

                        # ✅ 산술 연산자는 결과 타입을 결정해야 함
                        elif token.data in {"+", "-", "*", "/"}:
                            if a.type == TokenType.FLOAT or b.type == TokenType.FLOAT:
                                result_type = TokenType.FLOAT
                                result = Float(result)  # ✅ Float으로 변환
                            else:
                                result_type = TokenType.INTEGER
                                result = Integer(result)  # ✅ Integer로 변환
                        else:
                            raise ExprEvaluationError(f"Unsupported operator: {token.data}")
                    else:
                        raise ExprEvaluationError(f"Unsupported operand types: {a.type} and {b.type}")

                    stack.append(Token(result, result_type, line=token.line, column=token.column))

            elif self.is_function(token):
                func_info = FunctionRegistry.get_function(token.data.value)
                func_tokens = self.split_function_token(token.data)
                arg_values = [stack.pop().data.value for _ in range(func_info["arg_count"])][::-1]
                function_executor = FunctionExecutor(func_info, global_var_manager=self.var_manager, arg_values=arg_values)
                result = function_executor.execute()
                result_type = self.get_token_type(result)

                stack.append(Token(result, result_type, line=token.line, column=token.column))

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

    def is_function(self, token: Token) -> bool:
        """토큰이 함수인지 확인 PLUS(3,4)"""
        func_name = token.data.value.upper()
        func_info = FunctionRegistry.get_function(func_name)
        return func_info != None

    def execute_user_function(self, func_body: List[Token], local_vars: dict):
        """
        간단한 사용자 정의 함수 실행기
        - 현재는 간단한 RETURN 문만 지원
        """
        if func_body.startswith("RETURN "):
            expr = func_body[len("RETURN "):].strip()
            evaluator = ExprEvaluator(VariableManager())  # ✅ 새로운 평가기 생성
            evaluator.var_manager.variables.update(local_vars)  # ✅ 지역 변수 전달
            return evaluator.evaluate(func_body)
        raise ExprEvaluationError(f"Unsupported function body: {func_body}")


    def evaluate(self, tokens:List[Token]) :
        """수식을 계산하여 결과 반환 (예외 처리 강화)"""
        try:
            postfix_tokens = self.to_postfix(tokens)
            return self.evaluate_postfix(postfix_tokens)
        except Exception as e:
            raise ExprEvaluationError(f"Error evaluating : {str(e)}")

    def get_token_type(self, value) -> TokenType:
        """value 로 해당하는 토큰타입을 반환"""
        if not isinstance(value, KavanaDataType):
            raise ExprEvaluationError(f"Unsupported KavanaDataType: {value}")
        
        if value is None:
            return TokenType.NONE
        if isinstance(value, Integer):
            return TokenType.INTEGER
        if isinstance(value, Float):
            return TokenType.FLOAT
        if isinstance(value, Boolean):
            return TokenType.BOOLEAN
        if isinstance(value, String):
            return TokenType.STRING
        if isinstance(value, Date):
            return TokenType.DATE
        #Point, Rectangle, Region, window, Application, Image
        
        if isinstance(value, Point):
            return TokenType.POINT
        if isinstance(value, Rectangle):
            return TokenType.RECTANGLE
        if isinstance(value, Region):
            return TokenType.REGION
        if isinstance(value, Window):
            return TokenType.WINDOW
        if isinstance(value, Application):
            return TokenType.APPLICATION
        if isinstance(value, Image):
            return TokenType.IMAGE
        
        raise ExprEvaluationError(f"Unsupported token type: {value}")