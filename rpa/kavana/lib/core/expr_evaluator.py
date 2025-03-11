import re
import operator
from typing import List, Tuple, Union
from datetime import datetime, timedelta
from lib.core.command_parser import CommandParser
from lib.core.datatypes.application import Application
from lib.core.datatypes.image import Image
from lib.core.datatypes.kavana_datatype import Boolean,  Float, Integer, KavanaDataType, String
from lib.core.datatypes.list_type import ListType
from lib.core.datatypes.point import Point
from lib.core.datatypes.rectangle import Rectangle
from lib.core.datatypes.region import Region
from lib.core.datatypes.window import Window
from lib.core.datatypes.ymd_time import Ymd, YmdTime
from lib.core.exceptions.kavana_exception import ExprEvaluationError, KavanaException
from lib.core.custom_token_maker import CustomTokenMaker
from lib.core.token_type import TokenType
from lib.core.function_executor import FunctionExecutor
from lib.core.function_parser import FunctionParser
from lib.core.function_registry import FunctionRegistry
from lib.core.token import ListExToken, ListIndexToken, Token
from lib.core.token_util import TokenUtil
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
        self.data_token_type = {
            TokenType.NONE,
            TokenType.INTEGER,
            TokenType.FLOAT,
            TokenType.STRING,
            TokenType.BOOLEAN,
            TokenType.YMDTIME,
            TokenType.YMD,
            TokenType.POINT,
            TokenType.REGION,
            TokenType.RECTANGLE,
            TokenType.IMAGE,
            TokenType.WINDOW,
            TokenType.APPLICATION
        }            

    def to_postfix(self, tokens: List[Token]) -> List[Token]:
        """토큰 리스트를  후위 표기법(RPN)으로 변환"""
        output = []
        stack = []

        i = 0
        while i < len(tokens):
            token = tokens[i]

            # ✅ 함수 처리 (PLUSE(3,4) 형태)
            if token.type == TokenType.IDENTIFIER :
                func_info = FunctionRegistry.get_function(token.data.value)
                if func_info is not None:
                    arg_count = func_info["arg_count"]
                    # combined_token, i = FunctionParser._func_tokens_to_string(tokens, start_index=i, func=None, arg_count=arg_count)
                    combined_token, i = FunctionParser.make_function_token(tokens, start_index=i)
                    output.append(combined_token)
                    continue
                else: # list[express]과 같은 형태
                    var_token = self.var_manager.get_variable(token.data.value)

                    if var_token is not None and var_token.type == TokenType.LIST_EX:
                        list_index_token,i = self.make_list_index_token(tokens, i)
                        if list_index_token is not None and len(list_index_token) > 0:
                            output.append(list_index_token)
                            continue
                        else: # 아무것도 없이 단독으로 사용된 변수
                            output.append(var_token)
                            i += 1
                            continue    


            # ✅ 연산자 처리
            if token.type == TokenType.OPERATOR or token.type == TokenType.LOGICAL_OPERATOR:
                if token.data.value.upper() == "NOT":
                    # NOT은 오른쪽 결합, 우선순위가 더 높은 연산자만 pop
                    while stack and stack[-1].type == TokenType.OPERATOR and self.OPERATORS[token.data.value][0] < self.OPERATORS[stack[-1].data.value][0]:
                        output.append(stack.pop())
                else:
                    # 일반 이항 연산자는 왼쪽 결합, 우선순위가 같거나 높은 연산자 pop
                    while stack and stack[-1].type == TokenType.OPERATOR and self.OPERATORS[token.data.value][0] <= self.OPERATORS[stack[-1].data.value][0]:
                        output.append(stack.pop())
                stack.append(token)
                i += 1
                continue

            if token.type in {TokenType.POINT, TokenType.RECTANGLE, TokenType.REGION, TokenType.IMAGE, TokenType.WINDOW, TokenType.APPLICATION}:
                custom_token, i = CustomTokenMaker.custom_object_token(tokens, i, token.type)
                stack.append(custom_token)
                continue
            # ✅ token.type 이 KavanaDataType이면 그대로 출력
            if token.type in self.data_token_type:
                output.append(token)
                i += 1
                continue
            if token.type == TokenType.LIST_EX:
                if token.status == 'Parsed':
                    # ListExToken의 expresses를 평가해서 ListType에 넣는다.
                    exprEval = ExprEvaluator(self.var_manager)
                    result_values = []
                    for express in token.element_expresses:
                        element_token = exprEval.evaluate(express)
                        if element_token.type == TokenType.LIST_EX: # 2중배열
                            result_values.append(element_token.data.to_list())
                            token.element_type = element_token.element_type
                        else:
                            result_values.append(element_token)
                            token.element_type = element_token.type
                    token.status = 'Evaluated'
                    token.data = ListType(*result_values)
                output.append(token)
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

            if token.type in self.data_token_type:  # ✅ Kavana 데이터 타입이면 그대로 스택에 추가
                stack.append(token)
            
            elif token.type == TokenType.IDENTIFIER:
                valueToken = self.var_manager.get_variable(token.data.value)
                if valueToken is None:
                    raise ExprEvaluationError(f"Undefined variable: {token.data}", token.line, token.column)                
                stack.append(valueToken)
            
            elif token.type == TokenType.OPERATOR or token.type == TokenType.LOGICAL_OPERATOR:
                if token.data.value.upper() == "NOT":
                    a = stack.pop()
                    logical_op = token.data.value.upper()
                    result = self.OPERATORS[logical_op][1](a.data.value)
                    stack.append(Token(Boolean(result), TokenType.BOOLEAN, line=token.line, column=token.column))
                else:
                    b = stack.pop()
                    a = stack.pop()
                    result_type = TokenType.UNKNOWN
                    if token.data.value == "%":
                        if not a.type == TokenType.INTEGER or not b.type == TokenType.INTEGER:
                            raise ExprEvaluationError(f"Unsupported operand types for %: {a.type} and {b.type}")
                        result = Integer(a.data.value % b.data.value)
                        result_type = TokenType.INTEGER
                    if token.data.value == '+' and a.type == TokenType.LIST_EX and b.type == TokenType.LIST_EX:
                        # list + list
                        if a.element_type != b.element_type:
                            raise ExprEvaluationError("Cannot add lists of different types", token.line, token.column)
                        new_list = ListType(*(a.data.to_list() + b.data.to_list()))
                        result = new_list
                        result_type = TokenType.LIST_EX
                    # YmdTime 연산 : Ymd + Integer, Ymd - Integer, Ymd - Ymd
                    elif a.type == TokenType.YMDTIME and b.type == TokenType.INTEGER:
                        dt = a.data.value + timedelta(days=b.data.value) if token.data.value == "+" else a.data.value - timedelta(days=b.data.value)
                        result = YmdTime.from_datetime(dt)
                        result_type = TokenType.YMDTIME
                    elif a.type == TokenType.YMDTIME and b.type == TokenType.YMDTIME and token.data.value == "-":
                        # YMDTIME - YMDTIME
                        diff_seconds = (a.data.value - b.data.value).total_seconds()  # ✅ 초 단위 차이 계산
                        result = Integer(int(diff_seconds))  # ✅ 결과를 정수(Integer)로 변환
                        result_type = TokenType.INTEGER
                    # Ymd연산 : Ymd + Integer, Ymd - Integer, Ymd - Ymd
                    elif a.type == TokenType.YMD and b.type == TokenType.INTEGER:
                        # ✅ YMD + int 또는 YMD - int (N일 더하거나 빼기)
                        dt = a.data.value + timedelta(days=b.data.value) if token.data.value == "+" else a.data.value - timedelta(days=b.data.value)
                        result = Ymd.from_date(dt)  
                        result_type = TokenType.YMD

                    elif a.type == TokenType.YMD and b.type == TokenType.YMD and token.data.value == "-":
                        # ✅ YMD - YMD (날짜 차이 반환)
                        diff_days = (a.data.value - b.data.value).days  # ✅ `days` 속성은 이미 `일 단위`이므로 `// 86400` 불필요
                        result = Integer(diff_days)
                        result_type = TokenType.INTEGER


                    elif a.type == TokenType.STRING and b.type == TokenType.STRING and token.data.value == "+":
                        result = String(a.data.value + b.data.value)
                        result_type = TokenType.STRING
                    elif (a.type == TokenType.NONE or b.type == TokenType.NONE) and token.data in {"==", "!="}:
                        result = self.OPERATORS[token.data][1](a.data.value, b.data.value)
                        result_type = TokenType.BOOLEAN

                    elif a.type in {TokenType.INTEGER, TokenType.FLOAT, TokenType.BOOLEAN} and b.type in {TokenType.INTEGER, TokenType.FLOAT, TokenType.BOOLEAN}:
                        result = self.OPERATORS[token.data.value][1](a.data.value, b.data.value)
                        # ✅ 비교 연산자일 경우 결과는 항상 BOOLEAN
                        if token.data.value in {"==", "!=", ">", "<", ">=", "<="}:
                            result = Boolean(result)
                            result_type = TokenType.BOOLEAN

                        # ✅ 산술 연산자는 결과 타입을 결정해야 함
                        elif token.data.value in {"+", "-", "*", "/"}:
                            if a.type == TokenType.FLOAT or b.type == TokenType.FLOAT:
                                result = Float(result)  # ✅ Float으로 변환
                                result_type = TokenType.FLOAT
                            else:
                                result = Integer(result)  # ✅ Integer로 변환
                                result_type = TokenType.INTEGER
                        else:
                            raise ExprEvaluationError(f"Unsupported operator: {token.data.value}", token.line, token.column)
                    else:
                        raise ExprEvaluationError(f"Unsupported operand types: {a.type} and {b.type}", token.line, token.column)

                    stack.append(Token(result, result_type, line=token.line, column=token.column))

            elif token.type == TokenType.FUNCTION:
                func_name = token.function_name.upper()
                func_info = FunctionRegistry.get_function(func_name)
                # 인자의 값을 구한다.
                arg_values = []
                for arg_tokens in token.arguments:  # ✅ 각 인자는 List[Token] 형태
                    evaluator = ExprEvaluator(self.var_manager)
                    result_token = evaluator.evaluate(arg_tokens)  # ✅ 표현식을 평가
                    arg_values.append(result_token)  # ✅ 평가 결과 저장
                # 함수 수행
                function_executor = FunctionExecutor(func_info, global_var_manager=self.var_manager, arg_values=arg_values)
                result_token = function_executor.execute()
                # 결과 토큰 저장
                stack.append(result_token)
            elif token.type == TokenType.CUSTOM_TYPE:
                arg_values = []
                for arg_tokens in token.arguments:  # ✅ 각 인자는 List[Token] 형태
                    evaluator = ExprEvaluator(self.var_manager)
                    result_token = evaluator.evaluate(arg_tokens)  # ✅ 표현식을 평가
                    arg_values.append(result_token.data.value)  # ✅ 평가 결과 저장
                if token.object_type == TokenType.POINT:
                    result_token = Token(data=Point(*arg_values), type=TokenType.POINT)
                elif token.object_type == TokenType.RECTANGLE:
                    result_token = Token(data=Rectangle(*arg_values), type=TokenType.RECTANGLE)
                elif token.object_type == TokenType.REGION:
                    result_token = Token(data=Region(*arg_values), type=TokenType.REGION)
                elif token.object_type == TokenType.IMAGE:
                    result_token = Token(data=Image(*arg_values), type=TokenType.IMAGE)
                elif token.object_type == TokenType.WINDOW:
                    result_token = Token(data=Window(*arg_values), type=TokenType.WINDOW)
                elif token.object_type == TokenType.APPLICATION:
                    result_token = Token(data=Application(*arg_values), type=TokenType.APPLICATION)
                else:
                    raise ExprEvaluationError(f"Unsupported custom object type: {token.object_type}")
                stack.append(result_token)

            elif token.type == TokenType.LIST_EX:
                stack.append(token)
            elif token.type == TokenType.LIST_INDEX: # list[express] 형태
                var_name = token.data.value
                # row,col 값 계산
                row = ExprEvaluator(self.var_manager).evaluate(token.row_express).data.value
                evaluator = ExprEvaluator(self.var_manager).evaluate(token.column_express)
                col = None if evaluator is None else evaluator.data.value
                # list token 가져오기
                list_var_token = self.var_manager.get_variable(var_name)
                if list_var_token is None or list_var_token.type != TokenType.LIST_EX:
                    ExprEvaluationError(f"리스트 변수가 없거나 변수가 리스트 타입이 아닙니다: {var_name}", token.line, token.column)
                # 인덱스 값 계산
                element_token = list_var_token.data.get(row,col)
                # token_type = list_var_token.element_type
                # index_value_token = Token(data=data, type=token_type)
                stack.append(element_token)
            
            else:
                raise ExprEvaluationError(f"지원하지 않는 Token타입입니다.: {token.data.value} {token.type}", token.line, token.column)  

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
            # expr = func_body[len("RETURN "):].strip()
            evaluator = ExprEvaluator(VariableManager())  # ✅ 새로운 평가기 생성
            evaluator.var_manager.variables.update(local_vars)  # ✅ 지역 변수 전달
            return evaluator.evaluate(func_body)
        raise ExprEvaluationError(f"Unsupported function body: {func_body}")


    def evaluate(self, tokens:List[Token]) -> Token:
        """수식을 계산하여 결과 반환 (예외 처리 강화)"""
        if not tokens or len(tokens) == 0:
            return None
        try:
            postfix_tokens = self.to_postfix(tokens)
            return self.evaluate_postfix(postfix_tokens)
        except KavanaException as ke:
            # ✅ Kavana 예외는 그대로 전달
            raise ke

        except Exception as e:
            # ✅ 기타 예외는 ExprEvaluationError로 변환하여 감싸기
            raise ExprEvaluationError(f"Error evaluate express: {str(e)}")        

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
        if isinstance(value, datetime):
            return TokenType.YMDTIME
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


    def make_list_index_token(self, tokens: List[Token], start_index: int) -> Tuple[Token, int]:
        """ 리스트 인덱싱 토큰을 파싱하는 함수 (중첩 인덱싱 지원) """
        
        if start_index + 2 >= len(tokens):  # 최소한 list[0] 형태가 있어야 함
            return [], start_index  # 인덱스 초과 방지

        var_token = tokens[start_index]  # 리스트 변수

        if tokens[start_index + 1].value == "[":  # 리스트 접근 시작
            express = []
            i = start_index + 2

            bracket_count = 1  # `[` 개수를 추적하여 중첩된 인덱싱 확인
            while i < len(tokens) and bracket_count > 0:
                if tokens[i].value == "[":
                    bracket_count += 1
                elif tokens[i].value == "]":
                    bracket_count -= 1
                    if bracket_count == 0:  # 마지막 `]`을 찾았으면 종료
                        break
                express.append(tokens[i])
                i += 1

            if bracket_count > 0:  # 닫는 `]`가 부족하면 오류
                raise ExprEvaluationError("리스트 인덱스의 `]`가 부족합니다.", tokens[start_index].line, tokens[start_index].column)

            # 리스트 인덱스 토큰 생성
            list_index_token = ListIndexToken(express=express, data=String(var_token.value))

            return list_index_token, i + 1  # 생성한 토큰과 새로운 위치 반환
        
        return None, start_index  # 리스트 인덱스가 아니라면 원래 위치 유지
