import codecs
import re
import operator
from typing import List, Tuple, Union
from datetime import datetime, timedelta
from lib.core.command_parser import CommandParser

from lib.core.command_preprocessor import CommandPreprocessor
from lib.core.datatypes.application import Application
from lib.core.datatypes.hash_map import HashMap
from lib.core.datatypes.image import Image
from lib.core.datatypes.kavana_datatype import Boolean,  Float, Integer, KavanaDataType, String
from lib.core.datatypes.array import Array
from lib.core.datatypes.point import Point
from lib.core.datatypes.rectangle import Rectangle
from lib.core.datatypes.region import Region
from lib.core.datatypes.window import Window
from lib.core.datatypes.ymd_time import Ymd, YmdTime
from lib.core.exceptions.kavana_exception import ExprEvaluationError, KavanaException, KavanaTypeError
from lib.core.custom_token_maker import CustomTokenMaker
from lib.core.token_type import TokenType
from lib.core.function_executor import FunctionExecutor
from lib.core.function_parser import FunctionParser
from lib.core.function_registry import FunctionRegistry
from lib.core.token import ArrayToken, AccessIndexToken, StringToken, Token
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
    
    def __init__(self, executor=None, variable_manager:VariableManager=None):
        """ExprEvaluator 생성자에서 executor 또는 variable_manager 선택적으로 받음"""
        self.executor = executor
        self.variable_manager = variable_manager if variable_manager else executor.variable_manager  # ✅ 기본값 설정

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
            for var_name, token in local_vars.items():
                self.variable_manager.set_variable(var_name, token, local=True)

            evaluator = ExprEvaluator(self)  # ✅ 새로운 평가기 생성
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
            raise ExprEvaluationError(f"표현식을 해석할 때 오류발생: {str(e)}")        

    def get_token_type(self, value) -> TokenType:
        """value 로 해당하는 토큰타입을 반환"""
        if not isinstance(value, KavanaDataType):
            raise ExprEvaluationError(f"지원하지 않는 kavana 데이터타입입니다: {value}")
        
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
                    combined_token, i = FunctionParser.make_function_token(tokens, start_index=i)
                    output.append(combined_token)
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

            if token.type == TokenType.ARRAY:
                if token.status == 'Parsed':
                    # ArrayToken의 expresses를 평가해서 Array에 넣는다.
                    exprEval = ExprEvaluator(self.executor)
                    result_values = []
                    for express in token.element_expresses:
                        element_token = exprEval.evaluate(express)
                        if element_token.type == TokenType.ARRAY: # 2중배열
                            result_values.append(element_token.data.value.copy())
                            token.element_type = element_token.element_type
                        else:
                            result_values.append(element_token)
                            token.element_type = element_token.type
                    token.status = 'Evaluated'
                    token.data = Array(result_values)
                output.append(token)
                i += 1
                continue
            if token.type == TokenType.HASH_MAP:
                if token.status == 'Parsed':
                    # HashMapToken의 expresses를 평가해서 HashMap에 넣는다.
                    exprEval = ExprEvaluator(self.executor)
                    evaluated_map  = {}
                    for key, express in token.key_express_map.items():
                        evaluated_value_token = exprEval.evaluate(express)
                        if not isinstance(evaluated_value_token.data, KavanaDataType):
                            raise KavanaTypeError(f"HashMap의 값은 KavanaDataType이어야 합니다: {evaluated_value_token.data}")
                        evaluated_map[key] = evaluated_value_token

                    token.status = 'Evaluated'
                    token.data = HashMap(value=evaluated_map)
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


            # ✅ token.type 이 KavanaDataType이면 그대로 출력
            elif token.type in self.data_token_type:
                output.append(token)
                i += 1
                continue                
            else:
                output.append(token)

            i += 1

        # ✅ 스택에 남은 연산자 추가
        while stack:
            output.append(stack.pop())

        return output


    def evaluate_postfix(self, tokens: List[Token]) -> Token:
        """후위 표기법 수식을 계산"""
        from lib.core.commands.print_command import PrintCommand

        stack = []

        for token in tokens:

            if token.type == TokenType.STRING:
                applied_token = self.apply_prefix_token(token)
                stack.append(applied_token)  # ✅ 문자열 토큰은 그대로 스택에 추가                  

            elif token.type in self.data_token_type:  # ✅ Kavana 데이터 타입이면 그대로 스택에 추가
                stack.append(token)
            
            elif token.type == TokenType.IDENTIFIER:
                valueToken = self.variable_manager.get_variable(token.data.value)
                if valueToken is None:
                    raise ExprEvaluationError(f"정의되지 않은 변수: {token.data}", token.line, token.column)                
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
                            raise ExprEvaluationError(f"%는 지원하지 않는 타입입니다 : {a.type} and {b.type}")
                        result = Integer(a.data.value % b.data.value)
                        result_type = TokenType.INTEGER
                    if token.data.value == '+' and a.type == TokenType.ARRAY and b.type == TokenType.ARRAY:
                        # list + list
                        if a.element_type != b.element_type:
                            raise ExprEvaluationError("배열에는 다른 데이터 타입을 추가할 수 없습니다.", token.line, token.column)
                        new_list = Array(a.data.value.copy() + b.data.value.copy())                        
                        result = new_list
                        result_type = TokenType.ARRAY
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

                    elif a.type in {TokenType.INTEGER, TokenType.FLOAT, TokenType.BOOLEAN, TokenType.STRING} and b.type in {TokenType.INTEGER, TokenType.FLOAT, TokenType.BOOLEAN, TokenType.STRING}:
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
                            raise ExprEvaluationError(f"지원하지 않는 연산자 입니다: {token.data.value}", token.line, token.column)
                    else:
                        raise ExprEvaluationError(f"연산을 지원하지 않는 타입입니다.: {a.type} and {b.type}", token.line, token.column)

                    stack.append(Token(result, result_type, line=token.line, column=token.column))

            elif token.type == TokenType.FUNCTION:
                func_name = token.function_name.upper()
                func_info = FunctionRegistry.get_function(func_name)
                # 인자의 값을 구한다.
                arg_values = []
                for arg_tokens in token.arguments:  # ✅ 각 인자는 List[Token] 형태
                    evaluator = ExprEvaluator(self.executor)
                    result_token = evaluator.evaluate(arg_tokens)  # ✅ 표현식을 평가
                    arg_values.append(result_token)  # ✅ 평가 결과 저장
                # 함수 수행
                function_executor = FunctionExecutor(func_info, global_var_manager=self.variable_manager, arg_values=arg_values)
                result_token = function_executor.execute()
                # 결과 토큰 저장
                stack.append(result_token)
            elif token.type == TokenType.CUSTOM_TYPE:
                arg_values = []
                for arg_tokens in token.arguments:  # ✅ 각 인자는 List[Token] 형태
                    evaluator = ExprEvaluator(self.executor)
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
                    raise ExprEvaluationError(f"지원하지 않는 객체 타입입니다: {token.object_type}")
                stack.append(result_token)

            elif token.type in { TokenType.ARRAY, TokenType.HASH_MAP }:
                stack.append(token)
            elif token.type == TokenType.ACCESS_INDEX: # list[express] 또는 map[express] 형태
                var_name = token.data.value
                # row,col 값 계산
                row = ExprEvaluator(self.executor).evaluate(token.row_express).data.value
                evaluator = ExprEvaluator(self.executor).evaluate(token.column_express)
                col = None if evaluator is None else evaluator.data.value
                # list token 가져오기
                list_or_map_var_token = self.variable_manager.get_variable(var_name)
                if list_or_map_var_token.type == TokenType.ARRAY:    
                    element_token = list_or_map_var_token.data.get(row,col)
                elif list_or_map_var_token.type == TokenType.HASH_MAP:
                    element_token = list_or_map_var_token.data.get(row)
                else:
                    ExprEvaluationError(f"리스트 또는 Map 변수가 없거나 타입이 올바르지 않습니다: {var_name}", token.line, token.column)
                stack.append(element_token)

            
            else:
                raise ExprEvaluationError(f"지원하지 않는 Token타입입니다.: {token.data.value} {token.type}", token.line, token.column)  

        return stack[0]

    def apply_prefix_token(self, token: StringToken) -> StringToken:
        ''' stringtoken을 평가하여 결과를 반환 '''
        string_value = token.data.value

        if token.is_raw:
            evaluated = string_value
        elif token.is_formatted:
            evaluated = self._evaluate_fstring(string_value)
        else:
            # evaluated = self.safe_decode_unicode_escapes(string_value)
            evaluated = TokenUtil.decode_escaped_string(string_value)

        return Token(
            data=String(evaluated),
            type=TokenType.STRING,
            line=token.line,
            column=token.column
        )
    
    def safe_decode_unicode_escapes(self, s: str) -> str:
        try:
            return codecs.decode(s, 'unicode_escape')
        except Exception:
            return s 
           
    def _evaluate_fstring(self, message: str, allow_recurse=True) -> str:
        """f-string 내의 {} 표현식을 평가하여 실제 값으로 변환"""
        def replace_expr(match):
            expression = match.group(1)  # `{}` 내부 표현식

            try:
                ppLines = CommandPreprocessor().preprocess([expression])
                tokens = CommandParser.tokenize(ppLines[0])
                result_token = self.evaluate(tokens)
                return result_token.data.string
            except Exception as e:
                return f"[ERROR: {str(e)}]"

        return re.sub(r"\{(.*?)\}", replace_expr, message)    