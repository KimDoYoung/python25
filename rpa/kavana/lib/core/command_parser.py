from datetime import date, datetime
import re
import os
from typing import Any, List
from lib.core.command_preprocessor import CommandPreprocessor, PreprocessedLine
from lib.core.datatypes.kavana_datatype import Boolean,  Float, Integer, KavanaDataType, NoneType, String
from lib.core.datatypes.list_type import ListType
from lib.core.datatypes.point import Point
from lib.core.datatypes.ymd_time import YmdTime
from lib.core.exceptions.kavana_exception import CommandParserError, DataTypeError
from lib.core.token import ListIndexToken, ListToken, Token
from lib.core.token_type import TokenType
from lib.core.function_registry import FunctionRegistry
from lib.core.token_util import TokenUtil

class CommandParser:
    """
    Kavana 스크립트의 명령어를 분석하는 파서.
    - `main ... end_main` 블록 안에서 실행
    - `INCLUDE` → 외부 KVS 파일 포함
    - `ENV_LOAD` → .env 파일을 불러와 `SET`으로 변환
    """
    def __init__(self, script_lines=[], base_path="."):
        self.script_lines = script_lines
        self.base_path = base_path  # 스크립트 기본 경로 (INCLUDE, LOAD 처리용)
        self.in_main_block = False

    def parse(self, lines = []):
        """
        ✅ 스크립트의 모든 명령어를 분석하여 `Token` 리스트로 반환.
        """
        self.in_main_block = False
        parsed_commands = []
        if lines:
            self.script_lines = lines
        processed_lines = self.script_lines
        i = 0  

        while i < len(processed_lines):
            print(processed_lines[i].text)
            tokens = self.tokenize(processed_lines[i])  # ✅ `Token` 객체 리스트 반환
            
            if not tokens:
                i += 1
                continue

            cmd = tokens[0].data.value.upper()  # ✅ 명령어는 대문자로 변환
            args = tokens[1:]  # ✅ 나머지는 `Token` 리스트 그대로 유지

            # ✅ 블록 명령어 처리
            if cmd in ["IF", "WHILE", "FOR"]:
                end_mapping = {"IF": "END_IF", "WHILE": "END_WHILE", "FOR": "END_FOR"}
                block_body, new_index = self.parse_block(processed_lines, i + 1, end_mapping[cmd])
                parsed_commands.append({"cmd": f"{cmd}_BLOCK", "body": [{"cmd": cmd, "args": args}] + block_body})
                i = new_index + 1
                continue

            # ✅ FUNCTION 처리
            if cmd == "FUNCTION":
                i = self.parse_function(processed_lines, i)
                continue  # ✅ 함수 정의는 parsed_commands에 추가하지 않음

            # ✅ INCLUDE 처리
            if cmd == "INCLUDE":
                if not args:
                    raise SyntaxError("INCLUDE 문에 파일 경로가 필요합니다.")
                include_path = args[0].data.value.strip('"')  # ✅ Token 객체에서 값 추출
                self._include_process(include_path, parsed_commands)
                i += 1
                continue

            # ✅ LOAD 처리
            if cmd == "ENV_LOAD":
                if not args:
                    raise SyntaxError("ENV_LOAD 문에 .env 파일 경로가 필요합니다.")
                env_path = args[0].data.value.strip('"')  # ✅ Token 객체에서 값 추출
                self._env_load(env_path, parsed_commands)
                i += 1
                continue

            # ✅ MAIN 블록 처리
            if cmd == "MAIN":
                if not getattr(self, "ignore_main_check", False):
                    if self.in_main_block:
                        raise CommandParserError("중복된 MAIN문은 허용되지 않습니다. ", line = i+1)
                    self.in_main_block = True
                i += 1
                continue
            # ✅ END_MAIN 처리
            if cmd == "END_MAIN":
                if not getattr(self, "ignore_main_check", False):
                    if not self.in_main_block:
                        raise CommandParserError("'END_MAIN'이 'MAIN' 문 없이 사용되었습니다.", line = i+1)
                    self.in_main_block = False
                i += 1
                break

            # ✅ MAIN 블록 외부에서 명령어 사용 제한
            if not self.in_main_block and not getattr(self, "ignore_main_check", False):
                raise CommandParserError("명렁어는 MAIN 블록 내에서만 사용할 수 있습니다.", line = i+1)

            # ✅ 일반 명령어 추가
            parsed_commands.append({"cmd": cmd, "args": args})  # ✅ `args`도 `Token` 리스트로 저장
            i += 1  

        if self.in_main_block:
            raise CommandParserError("'END_MAIN'문이 빠졌습니다.", line = i+1)

        return parsed_commands

    def parse_block(self, ppLines: List[PreprocessedLine], start_line, end_keyword):
        """재귀적으로 블록을 파싱하는 함수"""
        block_body = []
        i = start_line

        while i < len(ppLines):
            line = ppLines[i].text.strip().upper()

            if line == end_keyword:
                return block_body, i  # ✅ END 키워드를 만나면 종료

            tokens = self.tokenize(ppLines[i])
            if not tokens:
                i += 1
                continue

            cmd = tokens[0].data.value.upper()
            args = tokens[1:]

            # ✅ 중첩된 블록 처리 (IF, WHILE, FOR)
            if cmd in ["IF", "WHILE", "FOR"]:
                end_mapping = {"IF": "END_IF", "WHILE": "END_WHILE", "FOR": "END_FOR"}
                nested_block, new_index = self.parse_block(ppLines, i + 1, end_mapping[cmd])
                block_body.append({"cmd": f"{cmd}_BLOCK", "body": [{"cmd": cmd, "args": args}] + nested_block})
                i = new_index + 1
                continue

            # ✅ 일반 명령어 추가
            block_body.append({"cmd": cmd, "args": args})
            i += 1

        raise CommandParserError(f"{end_keyword}가 없습니다.")  # ✅ 종료 키워드가 없으면 오류 발생

    def parse_function(self, ppLines:List[PreprocessedLine], start_line):
        """FUNCTION 블록을 파싱하여  header를 제외하고 FunctionRegistry에 저장"""
        func_def_lines = [ppLines[start_line]]
        i = start_line + 1

        while i < len(ppLines) and ppLines[i].text.strip().upper() != "END_FUNCTION":
            func_def_lines.append(ppLines[i])
            i += 1

        if i >= len(ppLines) or ppLines[i].text.strip().upper() != "END_FUNCTION":
            raise CommandParserError("함수 정의에서 END_FUNCTION이 누락되었습니다.", start_line, 0)
        i += 1  # ✅ END_FUNCTION 스킵

        # ✅ 함수 헤더 파싱
        header_tokens = self.tokenize(func_def_lines[0])
        if len(header_tokens) < 2:
            raise CommandParserError("함수 정의 헤더가 올바르지 않습니다.", start_line, 0)

        func_name = header_tokens[1].data.value
        params = []
        
        if len(header_tokens) > 2 and header_tokens[2].data.value == "(":
            # index 2부터 header_tokens의 끝까지를 가져와서 ")"를 제거 function plus a b 
            param_str = " ".join([t.data.value for t in header_tokens[3:]]).rstrip(")")
            params = [p.strip() for p in param_str.split(",")]
        elif len(header_tokens) > 2:
            params = header_tokens[2:]

        # ✅ `CommandParser`를 사용하여 함수 본문을 미리 파싱하여 저장
        parser = CommandParser()
        parser.ignore_main_check = True  # ✅ MAIN 블록 검사 무시
        parsed_commands = parser.parse(func_def_lines[1:])

        # ✅ FunctionRegistry에 저장
        FunctionRegistry.register_function(func_name, params, parsed_commands)
        return i  # ✅ 함수 정의 후 새로운 라인 번호 반환

    def _include_process(self, include_path, parsed_commands):
        """INCLUDE 문을 처리하여 외부 KVS 파일을 불러온다."""
        """✅ `INCLUDE "파일.kvs"` 처리 (상대 경로 지원)"""
        file_path = os.path.join(self.base_path, include_path)  # ✅ 상대 경로 → 절대 경로 변환
        full_path = os.path.abspath(file_path)  # ✅ 최종 절대 경로 변환

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"INCLUDE 파일을 찾을 수 없음: {file_path}")

        with open(full_path, "r", encoding="utf-8") as file:
            included_lines = file.readlines()

        # ✅ 기존 상태 저장
        original_ignore_main_check = getattr(self, "ignore_main_check", False)

        # ✅ INCLUDE 실행 중에는 MAIN 블록 여부를 무시하도록 설정
        self.ignore_main_check = True
        preprocessor = CommandPreprocessor()
        ppLines = preprocessor.preprocess(included_lines)

        included_parser = CommandParser(ppLines, self.base_path)
        included_parser.ignore_main_check = True  # ✅ 서브 파서에서도 MAIN 블록 검사 무시

        included_commands = included_parser.parse()

        # ✅ INCLUDE 완료 후 원래 상태 복원
        self.ignore_main_check = original_ignore_main_check

        parsed_commands.extend(included_commands)  # INCLUDE된 명령어 추가

    def _env_load(self, env_path, parsed_commands):
    
        # ✅ 상대 경로를 절대 경로로 변환
        full_path = os.path.abspath(os.path.join(self.base_path, env_path))

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"ENV_LOAD 파일을 찾을 수 없습니다: {full_path}")

        with open(full_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):  # ✅ 주석 및 빈 줄 무시
                    continue

                if "=" not in line:
                    raise CommandParserError(f"잘못된 환경 변수 형식 env line : {line}")

                key, value = line.split("=", 1)
                key = key.strip().upper()  # ✅ `$KEY` 형태로 저장
                value = value.strip()

                # ✅ 값의 타입을 판별하여 Token으로 변환
                if value.lower() in ["true", "false"]:
                    value_token = Token(data=Boolean(value.lower() == "true"), type=TokenType.BOOLEAN)
                elif value.isdigit():
                    value_token = Token(data=Integer(int(value)), type=TokenType.INTEGER)
                elif value.replace(".", "", 1).isdigit():  # ✅ Float 판별
                    value_token = Token(data=Float(float(value), type=TokenType.FLOAT))
                elif  (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                    value =value[1:-1]  # 앞뒤 따옴표 제거
                    value_token = Token(data=String(value), type=TokenType.STRING)
                else:
                    value_token = Token(data=String(value), type=TokenType.STRING)

                # ✅ "=" 연산자 토큰 추가
                equals_token = Token(data=String("="), type=TokenType.OPERATOR)

                key_token = Token(data=String(f"${key}"), type=TokenType.IDENTIFIER)
                # ✅ `parsed_commands`에 추가하여 추적 가능
                const_token = Token(data=String("const"), type=TokenType.COMMAND)
                parsed_commands.append({
                    "cmd": "CONST",
                    "args": [key_token, equals_token, value_token]
                })

    

    @staticmethod
    def tokenize(ppLine: PreprocessedLine) -> list:
        """한 줄을 `Token` 객체 리스트로 변환"""

        line = ppLine.text.strip()
        tokens = []

        token_patterns = [

            # ✅ 논리 값
            (r'\bTrue\b', TokenType.BOOLEAN),
            (r'\bFalse\b', TokenType.BOOLEAN),
            (r'\bNone\b', TokenType.NONE),
            # ✅ 데이터 타입 키워드
            (r'(?i)\bPOINT\b', TokenType.POINT),
            (r'(?i)\bREGION\b', TokenType.REGION),
            (r'(?i)\bRECTANGLE\b', TokenType.RECTANGLE),
            (r'(?i)\bIMAGE\b', TokenType.IMAGE),
            (r'(?i)\bWINDOW\b', TokenType.WINDOW),  
            (r'(?i)\bAPPLICATION\b', TokenType.APPLICATION),            
            
            (r'(?i)\bGLOBAL\b', TokenType.GLOBAL),

            # ✅ 제어문 키워드
            (r'(?i)\bIF\b', TokenType.IF),
            (r'(?i)\bELSE\b', TokenType.ELSE),
            (r'(?i)\bELIF\b', TokenType.ELIF),
            (r'(?i)\bWHILE\b', TokenType.WHILE),
            (r'(?i)\bFOR\b', TokenType.FOR),
            (r'(?i)\bTO\b', TokenType.TO),  
            (r'(?i)\bSTEP\b', TokenType.STEP), 
            (r'(?i)\bEND_IF\b', TokenType.END_IF),
            (r'(?i)\bEND_WHILE\b', TokenType.END_WHILE),
            (r'(?i)\bEND_FOR\b', TokenType.END_FOR),

            # ✅ 함수 관련 키워드
            (r'(?i)\bFUNCTION\b', TokenType.FUNCTION),
            (r'(?i)\bEND_FUNCTION\b', TokenType.END_FUNCTION),
            (r'(?i)\bRETURN\b', TokenType.RETURN),

            # ✅ 스크립트 실행 관련 키워드
            (r'(?i)\bINCLUDE\b', TokenType.INCLUDE),
            (r'(?i)\bENV_LOAD\b', TokenType.ENV_LOAD),
            (r'(?i)\bMAIN\b', TokenType.MAIN),
            (r'(?i)\bEND_MAIN\b', TokenType.END_MAIN),

            # ✅ 논리 연산자
            (r'(?i)\bAND\b', TokenType.LOGICAL_OPERATOR), 
            (r'(?i)\bOR\b', TokenType.LOGICAL_OPERATOR), 
            (r'(?i)\bNOT\b', TokenType.LOGICAL_OPERATOR),

            # ✅ 루프 제어 키워드
            (r'(?i)\bBREAK\b', TokenType.BREAK),
            (r'(?i)\bCONTINUE\b', TokenType.CONTINUE),
            # ✅ YmdTime 패턴 추가 (괄호 필수)
            (r"(?i)\bYmdTime\b", TokenType.IDENTIFIER),
            (r"(?i)\bYmd\b", TokenType.IDENTIFIER),

            # ✅ 작은따옴표 사용 감지 (문법 오류 처리)
            (r"'([^']*)'", None),  # ❌ 작은따옴표가 감지되면 예외 발생

            # ✅ LIST로 처리할 경우: `=` 또는 연산자(`+`, `-`, `*`, `/`, `,`, `(`) 뒤에 오는 `[ ... ]`
            #(r'\[(\s*\d+\s*(,\s*\d+\s*)*)\]', TokenType.LIST),

            # ✅ 연산자
            (r'\(', TokenType.LEFT_PAREN),
            (r'\)', TokenType.RIGHT_PAREN),
            (r'\[', TokenType.LEFT_BRACKET),
            (r'\]', TokenType.RIGHT_BRACKET),
            (r',', TokenType.COMMA),

            # ✅ OPERATOR
            # ✅ 2글자 연산자를 먼저 매칭해야 함 (순서 중요!)
            # (r'==|!=|>=|<=|>|<', TokenType.OPERATOR),  # ✅ 비교연산자
            # (r'[+\-*/=%]', TokenType.OPERATOR),

            # ✅ 연산자 (두 글자 연산자 먼저 매칭)
            (r'==|!=|>=|<=|[+\-*/=%<>]', TokenType.OPERATOR),

            # ✅ 일반 식별자  
            (r'[a-zA-Z_\$][a-zA-Z0-9_]*', TokenType.IDENTIFIER),

            # ✅ float, integer
            (r'\b\d+\.\d+|\.\d+|\d+\.\b', TokenType.FLOAT),  # 🔥 소수점만 있는 경우도 포함
            (r'\b\d+\b', TokenType.INTEGER),         # 정수 (예: 10, 42, 1000)

            # ✅ 모든 유니코드 문자 포함          
            (r'"((?:\\.|[^"\\])*)"', TokenType.STRING),  # ✅ 문자열 정규식 수정
        ]
        column_num = ppLine.original_column
        line_num = ppLine.original_line

        while line:
            matched = False

            # 🔥 공백을 건너뛰고 column 조정
            while line and line[0] == " ":
                column_num += 1
                line = line[1:]

            for pattern, token_type in token_patterns:
                match = re.match(pattern, line)
                if match:
                    raw_value = match.group(1) if token_type == TokenType.STRING else match.group(0)

                    # ❌ 작은따옴표(`' '`) 사용 감지 시 `SyntaxError` 발생
                    if token_type is None:
                        raise SyntaxError(
                            f"Invalid string format: Use double quotes (\") instead of single quotes (') at line {line_num}, column {column_num}"
                        )
                    if token_type == TokenType.STRING:
                        value = CommandParser.decode_escaped_string(raw_value)  # ✅ 직접 변환 함수 호출
                        value_datatype_changed = TokenUtil.value_by_kavana_type(value, token_type)
                        tokens.append(Token(data=value_datatype_changed, type=token_type, line=line_num, column=column_num))
                    elif token_type == TokenType.LIST:
                        list_values = [int(v.strip()) for v in raw_value.strip("[]").split(",")]
                        value_datatype_changed = ListType(*list_values)
                        token = ListToken(data=value_datatype_changed, type=token_type, line=line_num, column=column_num)
                        tokens.append(token)
                    else:
                        value = raw_value
                        value_datatype_changed = TokenUtil.value_by_kavana_type(value, token_type)
                        tokens.append(Token(data=value_datatype_changed, type=token_type, line=line_num, column=column_num))

                    column_num += len(match.group(0))
                    line = line[len(match.group(0)):]  # ✅ `line`을 올바르게 줄임

                    matched = True
                    break

            if not matched and line:  # ✅ 더 이상 처리할 수 없는 문자가 있으면 예외 발생
                CommandParserError(f"Unknown token at line {line_num}, column {column_num} : {line}")
        tokens = CommandParser.post_process_tokens(tokens)
        return tokens

    @staticmethod
    def post_process_tokens(tokens: List[Token]) -> List[Token]:
        ''' 
        [] 처리 TokenType.LIST로 처리할지, TokenType.LIST_INDEX로 처리할지 결정 
        set list = [1,2,3] => [SET, list, =, [1,2,3]]
        set list[0] = 100 => [SET, list[0], =, 100]
        +, = , ',' '(',  뒤에 '['가 오면 TokenType.LIST로 처리
        '[' 안에 있으면 TokenType.LIST_INDEX로 처리 (ex: list[b[1]])
        a[ b[1] + 1] 같은 중첩 구조도 처리 가능
        '''
        if not tokens:
            return []

        processed_tokens = []
        i = 0
        bracket_count = 0  # `[` 개수 추적

        while i < len(tokens):
            token = tokens[i]
            var_name = None
            if token.type == TokenType.LEFT_BRACKET:
                
                # `[` 시작 시 개수 증가
                bracket_count += 1

                # LIST 또는 LIST_INDEX인지 판별
                if bracket_count == 1 and processed_tokens and processed_tokens[-1].data.value in {
                    '=','+',',','(','-'
                }:
                    var_name = tokens[i-2].data.value
                    # ✅ LIST 처리 (최상위 `[`인 경우)
                    list_values = []
                    i += 1  # `[` 다음 토큰부터 시작

                    while i < len(tokens):
                        if tokens[i].type == TokenType.RIGHT_BRACKET:
                            bracket_count -= 1
                            if bracket_count == 0:  # 최상위 `[`가 닫힘
                                break
                        elif tokens[i].type == TokenType.LEFT_BRACKET:
                            bracket_count += 1  # 중첩 `[` 개수 증가
                        list_values.append(tokens[i])
                        i += 1

                    if i < len(tokens) and tokens[i].type == TokenType.RIGHT_BRACKET:
                        i += 1  # `]` 건너뛰기
                        if len(list_values) == 0:
                            raise CommandParserError("리스트 내용이 없습니다.", tokens[i].line, tokens[i].column)
                        element_type = list_values[0].type
                        processed_tokens.append(ListToken(data=ListType(*[t.data.value for t in list_values if t.type != TokenType.COMMA]), element_type=element_type))
                    else:
                        raise CommandParserError("리스트 닫힘 `]`이 없습니다.", tokens[i].line, tokens[i].column)

                else:
                    var_name = tokens[i-1].data.value
                    # ✅ LIST_INDEX 처리 (중첩된 `[`인 경우)
                    list_index_values = []
                    i += 1  # `[` 다음 토큰부터 시작
                    while i < len(tokens):
                        if tokens[i].type == TokenType.RIGHT_BRACKET:
                            bracket_count -= 1
                            if bracket_count == 0:  # 최상위 `[`가 닫힘
                                break
                        elif tokens[i].type == TokenType.LEFT_BRACKET:
                            bracket_count += 1  # 중첩 `[` 개수 증가
                        list_index_values.append(tokens[i])
                        i += 1

                    if i < len(tokens) and tokens[i].type == TokenType.RIGHT_BRACKET:
                        i += 1  # `]` 건너뛰기
                        if var_name is None:
                            raise CommandParserError("이름이 없는 리스트 index입니다", tokens[i].line, tokens[i].column)    
                        list_index_token = ListIndexToken(data=String(var_name), express=list_index_values)
                        # processed_tokens에서 마지막 토큰 제거
                        processed_tokens.pop()
                        processed_tokens.append(list_index_token)
                    else:
                        raise CommandParserError("인덱스 닫힘 `]`이 없습니다.", tokens[i].line, tokens[i].column)

            else:
                processed_tokens.append(token)
                i += 1

        return processed_tokens

    @staticmethod
    def decode_escaped_string(s: str) -> str:
        """✅ 1바이트씩 읽어가면서 이스케이프 문자 변환"""
        result = []
        i = 0
        while i < len(s):
            if s[i] == "\\" and i + 1 < len(s):  # 🔥 이스케이프 문자 발견
                escape_seq = s[i + 1]

                if escape_seq == "n":
                    result.append("\n")
                elif escape_seq == "t":
                    result.append("\t")
                elif escape_seq == "\\":
                    result.append("\\")
                elif escape_seq == '"':
                    result.append('"')
                else:
                    result.append("\\" + escape_seq)  # ✅ 미리 정의되지 않은 경우 그대로 추가

                i += 2  # 🔥 이스케이프 문자는 2바이트 처리
            else:
                result.append(s[i])
                i += 1

        return "".join(result)
    
    # @staticmethod        
    # def value_by_kavana_type(value: Any, token_type: TokenType) -> KavanaDataType:
    #     """토큰 값을 해당 TokenType에 맞게 변환 (잘못된 값이면 Custom Exception 발생)"""
    #     try:
    #         if token_type == TokenType.INTEGER:
    #             if not isinstance(value, int) and not str(value).isdigit():
    #                 raise DataTypeError("Invalid integer format", value)
    #             return Integer(int(value))

    #         elif token_type == TokenType.FLOAT:
    #             if not isinstance(value, float) and not re.match(r'^-?\d+\.\d+$', str(value)):
    #                 raise DataTypeError("Invalid float format", value)
    #             return Float(float(value))

    #         elif token_type == TokenType.BOOLEAN:
    #             if value not in {"True", "False", True, False}:
    #                 raise DataTypeError("Invalid boolean value, expected 'True' or 'False'", value)
    #             return Boolean(value == "True" or value is True)

    #         elif token_type == TokenType.NONE:
    #             if value not in {"None", None}:
    #                 raise DataTypeError("Invalid None value, expected 'None'", value)
    #             return NoneType(None)

    #         elif token_type == TokenType.STRING:
    #             return String(str(value))

    #         elif token_type == TokenType.LIST:
    #             if isinstance(value, list):  # ✅ 이미 리스트인 경우
    #                 return ListType(*value)
    #             if isinstance(value, str) and value.startswith("[") and value.endswith("]"):
    #                 elements = [int(v.strip()) for v in value.strip("[]").split(",")]
    #                 return ListType(*elements)
    #         #TODO : 추가 타입 추가

    #         return String(str(value))  # 나머지는 String (IDENTIFIER, OPERATOR 등)

    #     except DataTypeError as e:
    #         raise e  # 이미 처리된 예외 그대로 전달
    #     except Exception as e:
    #         raise DataTypeError(f"Unexpected error in classify_datatype: {str(e)}", value)
        
    # @staticmethod
    # def get_kavana_datatype(value: Any) -> KavanaDataType | None:
    #     """
    #     주어진 value에서 KavanaDataType의 요소 타입을 추출하는 함수
    #     - 리스트일 경우 내부 요소의 공통 타입을 반환
    #     - 단일 값일 경우 해당 타입 반환
    #     - 리스트가 비어 있으면 None 반환
    #     """
    #     if isinstance(value, list):  # 리스트 타입이면 내부 요소 확인
    #         if len(value) == 0:
    #             return None  # 빈 리스트이면 타입 미정

    #         first_type = CommandParser.get_kavana_datatype(value[0])  # 첫 번째 요소 타입 결정
    #         return first_type

    #     # 개별 값에 대한 타입 결정
    #     if isinstance(value, int):
    #         return Integer
    #     elif isinstance(value, float):
    #         return Float
    #     elif isinstance(value, bool):
    #         return Boolean
    #     elif value is None:
    #         return NoneType
    #     elif isinstance(value, str):
    #         return String
    #     elif isinstance(value, datetime):
    #         return datetime
    #     elif isinstance(value, date):
    #         return date
    #     elif isinstance(value, Point):
    #         return Point
    #     return None  # 알 수 없는 타입
