from datetime import date, datetime
import re
import os
from typing import Any, Dict, List, Tuple, Union
from lib.core.command_preprocessor import CommandPreprocessor, PreprocessedLine
from lib.core.datatypes.hash_map import HashMap
from lib.core.datatypes.kavana_datatype import Boolean,  Float, Integer, KavanaDataType, NoneType, String
from lib.core.datatypes.array import Array
from lib.core.datatypes.point import Point
from lib.core.datatypes.ymd_time import YmdTime
from lib.core.exception_registry import ExceptionRegistry
from lib.core.exceptions.kavana_exception import CommandParserError, DataTypeError, KavanaSyntaxError
from lib.core.token import ArrayToken, AccessIndexToken, HashMapToken, StringToken,  Token
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

            if cmd == "ON_EXCEPTION":
                i = self.parse_exception(processed_lines, i)
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

    def parse_exception(self, ppLines: List[PreprocessedLine], start_line: int):
        """ON_EXCEPTION 블록을 파싱하여 header를 제외하고 FunctionRegistry에 저장"""
        exception_def_lines = [ppLines[start_line]]  # ✅ ON_EXCEPTION 포함
        i = start_line + 1

        while i < len(ppLines) and ppLines[i].text.strip().upper() != "END_EXCEPTION":
            exception_def_lines.append(ppLines[i])
            i += 1

        if i >= len(ppLines):
            raise CommandParserError("예외 처리 정의에서 END_EXCEPTION이 누락되었습니다.", start_line, 0)

        # ✅ END_EXCEPTION도 예외 처리 블록에 포함
        exception_def_lines.append(ppLines[i])  
        i += 1
        
        # ✅ 수정된 블록을 등록
        ExceptionRegistry.register_exception(exception_def_lines)
        
        return i  # 다음 라인 인덱스 반환

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
                equals_token = Token(data=String("="), type=TokenType.ASSIGN)

                key_token = Token(data=String(f"${key}"), type=TokenType.IDENTIFIER)
                # ✅ `parsed_commands`에 추가하여 추적 가능
                parsed_commands.append({
                    "cmd": "CONST",
                    "args": [key_token, equals_token, value_token]
                })

    @staticmethod
    def decode_escaped_string(s: str) -> str:
        ESCAPE_MAP = {
            "n": "\n",
            "t": "\t",
            "r": "\r",
            "b": "\b",
            "f": "\f",
            "v": "\v",
            "\\": "\\",
            '"': '"',
        }        
        result = []
        i = 0
        while i < len(s):
            if s[i] == "\\":
                if i + 1 >= len(s):
                    raise ValueError("잘못된 문자열: 단독 백슬래시(`\\`)가 포함될 수 없습니다.")

                escape_seq = s[i + 1]
                result.append(ESCAPE_MAP.get(escape_seq, "\\" + escape_seq))
                i += 2
            else:
                result.append(s[i])
                i += 1
        return "".join(result)


    # @staticmethod
    # def decode_escaped_string(s: str) -> str:
    #     """✅ C 스타일 escape 변환 (`"\\n"` → `"\n"`)"""
    #     result = []
    #     i = 0
    #     while i < len(s):
    #         if s[i] == "\\":
    #             if i + 1 >= len(s):  # 🔥 단독 백슬래시는 오류
    #                 raise ValueError("잘못된 문자열: 단독 백슬래시(`\\`)가 포함될 수 없습니다.")

    #             escape_seq = s[i + 1]

    #             if escape_seq == "n":
    #                 result.append("\n")  # ✅ `\\n` → `\n` (개행 문자 변환)
    #             elif escape_seq == "t":
    #                 result.append("\t")  # ✅ `\\t` → `\t` (탭 문자 변환)
    #             elif escape_seq == "\\":
    #                 result.append("\\")  # ✅ `\\` → `\`
    #             elif escape_seq == '"':
    #                 result.append('"')  # ✅ `\"` → `"`
    #             else:
    #                 result.append("\\" + escape_seq)  # ✅ 알 수 없는 escape 문자 유지

    #             i += 2  # 🔥 이스케이프 문자 처리했으므로 두 글자 건너뛰기
    #         else:
    #             result.append(s[i])
    #             i += 1

    #     return "".join(result)

    # def decode_escaped_string(s: str) -> str:
    #     """✅ 1바이트씩 읽어가면서 이스케이프 문자 변환"""
    #     result = []
    #     i = 0
    #     while i < len(s):
    #         if s[i] == "\\" and i + 1 < len(s):  # 🔥 이스케이프 문자 발견
    #             escape_seq = s[i + 1]

    #             if escape_seq == "n":
    #                 result.append("\n")
    #             elif escape_seq == "t":
    #                 result.append("\t")
    #             elif escape_seq == "\\":
    #                 result.append("\\")
    #             elif escape_seq == '"':
    #                 result.append('"')
    #             else:
    #                 result.append("\\" + escape_seq)  # ✅ 미리 정의되지 않은 경우 그대로 추가

    #             i += 2  # 🔥 이스케이프 문자는 2바이트 처리
    #         else:
    #             result.append(s[i])
    #             i += 1

    #     return "".join(result)
    
    # @staticmethod
    # def tokenize(ppLine: PreprocessedLine) -> list:
    #     """한 줄을 `Token` 객체 리스트로 변환"""

    #     line = ppLine.text.strip()
    #     tokens = []

    #     token_patterns = [

    #         # ✅ 논리 값
    #         (r'\bTrue\b', TokenType.BOOLEAN),
    #         (r'\bFalse\b', TokenType.BOOLEAN),
    #         (r'\bNone\b', TokenType.NONE),
    #         # ✅ 데이터 타입 키워드
    #         (r'(?i)\bPOINT\b', TokenType.POINT),
    #         (r'(?i)\bREGION\b', TokenType.REGION),
    #         (r'(?i)\bRECTANGLE\b', TokenType.RECTANGLE),
    #         (r'(?i)\bIMAGE\b', TokenType.IMAGE),
    #         (r'(?i)\bWINDOW\b', TokenType.WINDOW),  
    #         (r'(?i)\bAPPLICATION\b', TokenType.APPLICATION),            
            
    #         (r'(?i)\bGLOBAL\b', TokenType.GLOBAL),

    #         # ✅ 제어문 키워드
    #         (r'(?i)\bEND_FUNCTION\b', TokenType.END_FUNCTION),
    #         (r'(?i)\bEND_WHILE\b', TokenType.END_WHILE),
    #         (r'(?i)\bFUNCTION\b', TokenType.FUNCTION),
    #         # ✅ 스크립트 실행 관련 키워드
    #         (r'(?i)\bENV_LOAD\b', TokenType.ENV_LOAD),
    #         (r'(?i)\bEND_MAIN\b', TokenType.END_MAIN),
    #         (r'(?i)\bINCLUDE\b', TokenType.INCLUDE),
    #         (r'(?i)\bRETURN\b', TokenType.RETURN),
    #         (r'(?i)\bMAIN\b', TokenType.MAIN),
    #         (r'(?i)\bEND_FOR\b', TokenType.END_FOR),
    #         (r'(?i)\bEND_IF\b', TokenType.END_IF),
    #         (r'(?i)\bWHILE\b', TokenType.WHILE),
    #         (r'(?i)\bSTEP\b', TokenType.STEP), 
    #         (r'(?i)\bELSE\b', TokenType.ELSE),
    #         (r'(?i)\bELIF\b', TokenType.ELIF),
    #         (r'(?i)\bIF\b', TokenType.IF),
    #         (r'(?i)\bFOR\b', TokenType.FOR),
    #         (r'(?i)\bTO\b', TokenType.TO),  
    #         (r'(?i)\bIN\b', TokenType.IN), 

    #         # ✅ 함수 관련 키워드

    #         # ✅ 논리 연산자
    #         (r'(?i)\bAND\b', TokenType.LOGICAL_OPERATOR), 
    #         (r'(?i)\bOR\b', TokenType.LOGICAL_OPERATOR), 
    #         (r'(?i)\bNOT\b', TokenType.LOGICAL_OPERATOR),

    #         # ✅ 루프 제어 키워드
    #         (r'(?i)\bBREAK\b', TokenType.BREAK),
    #         (r'(?i)\bCONTINUE\b', TokenType.CONTINUE),
    #         # ✅ YmdTime 패턴 추가 (괄호 필수)
    #         (r"(?i)\bYmdTime\b", TokenType.IDENTIFIER),
    #         (r"(?i)\bYmd\b", TokenType.IDENTIFIER),

    #         # ✅ 작은따옴표 사용 감지 (문법 오류 처리)
    #         (r"'([^']*)'", None),  # ❌ 작은따옴표가 감지되면 예외 발생

    #         # ✅ 연산자
    #         (r'\(', TokenType.LEFT_PAREN),
    #         (r'\)', TokenType.RIGHT_PAREN),
    #         (r'\[', TokenType.LEFT_BRACKET),
    #         (r'\]', TokenType.RIGHT_BRACKET),
    #         (r'\{', TokenType.LEFT_BRACE),
    #         (r'\}', TokenType.RIGHT_BRACE),
    #         (r',', TokenType.COMMA),
    #         (r':', TokenType.COLON),


    #         (r'==|!=|>=|<=|[+\-*/%<>]', TokenType.OPERATOR),  # ✅ '=' 제거
    #         (r'=', TokenType.ASSIGN),  # ✅ '='을 별도로 할당 연산자로 분리            

    #         # ✅ 일반 식별자  
    #         (r'[a-zA-Z_\$][a-zA-Z0-9_]*', TokenType.IDENTIFIER),

    #         # ✅ float, integer
    #         (r'\b\d+\.\d+|\.\d+|\d+\.\b', TokenType.FLOAT),  # 🔥 소수점만 있는 경우도 포함
    #         (r'\b\d+\b', TokenType.INTEGER),         # 정수 (예: 10, 42, 1000)

    #         # ✅ 모든 유니코드 문자 포함          
    #         (r'"((?:\\.|[^"\\])*)"', TokenType.STRING),  # ✅ 문자열 정규식 수정

    #     ]
    #     column_num = ppLine.original_column
    #     line_num = ppLine.original_line

    #     while line:
    #         matched = False

    #         # 🔥 공백을 건너뛰고 column 조정
    #         while line and line[0] == " ":
    #             column_num += 1
    #             line = line[1:]

    #         for pattern, token_type in token_patterns:
    #             match = re.match(pattern, line)
    #             if match:
    #                 raw_value = match.group(1) if token_type == TokenType.STRING else match.group(0)

    #                 # ❌ 작은따옴표(`' '`) 사용 감지 시 `SyntaxError` 발생
    #                 if token_type is None:
    #                     raise KavanaSyntaxError(
    #                         f"잘못된 문자열 형식입니다: 쌍따옴표를 사용해 주십시오 (\") 줄번호 {line_num}, 컬럼번호 {column_num}"
    #                     )
    #                 if token_type == TokenType.RAW_STRING:
    #                     value = raw_value
    #                     tokens.append(Token(data=value, type=TokenType.STRING, line=line_num, column=column_num))                        
    #                 elif token_type == TokenType.STRING:
    #                     value = CommandParser.decode_escaped_string(raw_value)  # ✅ 직접 변환 함수 호출
    #                     value_datatype_changed = TokenUtil.primitive_to_kavana_by_tokentype(value, token_type)
    #                     tokens.append(Token(data=value_datatype_changed, type=token_type, line=line_num, column=column_num))
    #                 else:
    #                     value = raw_value
    #                     value_datatype_changed = TokenUtil.primitive_to_kavana_by_tokentype(value, token_type)
    #                     tokens.append(Token(data=value_datatype_changed, type=token_type, line=line_num, column=column_num))

    #                 column_num += len(match.group(0))
    #                 line = line[len(match.group(0)):]  # ✅ `line`을 올바르게 줄임

    #                 matched = True
    #                 break

    #         if not matched and line:  # ✅ 더 이상 처리할 수 없는 문자가 있으면 예외 발생
    #             line = line[1:]  # ✅ 한 글자 줄여서 진행하여 무한 루프 방지
    #             column_num += 1
    #     tokens = CommandParser.post_process_tokens(tokens)
    #     return tokens

    @staticmethod
    def tokenize(ppLine: PreprocessedLine) -> list:
        """한 줄을 `Token` 또는 `StringToken` 객체 리스트로 변환"""

        import re

        line = ppLine.text.strip()
        tokens = []

        string_pattern = r'(?i)(r?f?|fr?)("((?:\\.|[^"\\])*)")'  # 접두어 포함 문자열

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
            (r'(?i)\bEND_FUNCTION\b', TokenType.END_FUNCTION),
            (r'(?i)\bEND_WHILE\b', TokenType.END_WHILE),
            (r'(?i)\bFUNCTION\b', TokenType.FUNCTION),
            (r'(?i)\bENV_LOAD\b', TokenType.ENV_LOAD),
            (r'(?i)\bEND_MAIN\b', TokenType.END_MAIN),
            (r'(?i)\bINCLUDE\b', TokenType.INCLUDE),
            (r'(?i)\bRETURN\b', TokenType.RETURN),
            (r'(?i)\bMAIN\b', TokenType.MAIN),
            (r'(?i)\bEND_FOR\b', TokenType.END_FOR),
            (r'(?i)\bEND_IF\b', TokenType.END_IF),
            (r'(?i)\bWHILE\b', TokenType.WHILE),
            (r'(?i)\bSTEP\b', TokenType.STEP),
            (r'(?i)\bELSE\b', TokenType.ELSE),
            (r'(?i)\bELIF\b', TokenType.ELIF),
            (r'(?i)\bIF\b', TokenType.IF),
            (r'(?i)\bFOR\b', TokenType.FOR),
            (r'(?i)\bTO\b', TokenType.TO),
            (r'(?i)\bIN\b', TokenType.IN),

            # ✅ 논리 연산자
            (r'(?i)\bAND\b', TokenType.LOGICAL_OPERATOR),
            (r'(?i)\bOR\b', TokenType.LOGICAL_OPERATOR),
            (r'(?i)\bNOT\b', TokenType.LOGICAL_OPERATOR),

            # ✅ 루프 제어
            (r'(?i)\bBREAK\b', TokenType.BREAK),
            (r'(?i)\bCONTINUE\b', TokenType.CONTINUE),

            # ✅ YmdTime 키워드
            (r"(?i)\bYmdTime\b", TokenType.IDENTIFIER),
            (r"(?i)\bYmd\b", TokenType.IDENTIFIER),

            # ✅ 작은따옴표 오류 감지
            (r"'([^']*)'", None),

            # ✅ 연산자 및 구문
            (r'\(', TokenType.LEFT_PAREN),
            (r'\)', TokenType.RIGHT_PAREN),
            (r'\[', TokenType.LEFT_BRACKET),
            (r'\]', TokenType.RIGHT_BRACKET),
            (r'\{', TokenType.LEFT_BRACE),
            (r'\}', TokenType.RIGHT_BRACE),
            (r',', TokenType.COMMA),
            (r':', TokenType.COLON),
            (r'==|!=|>=|<=|[+\-*/%<>]', TokenType.OPERATOR),
            (r'=', TokenType.ASSIGN),

            # ✅ 문자열 (접두어 포함 문자열은 따로 처리)
            (string_pattern, TokenType.STRING),
            # ✅ 식별자
            (r'[a-zA-Z_\$][a-zA-Z0-9_]*', TokenType.IDENTIFIER),

            # ✅ 숫자
            (r'\b\d+\.\d+|\.\d+|\d+\.\b', TokenType.FLOAT),
            (r'\b\d+\b', TokenType.INTEGER),

        ]

        column_num = ppLine.original_column
        line_num = ppLine.original_line

        while line:
            matched = False

            while line and line[0] == " ":
                column_num += 1
                line = line[1:]

            for pattern, token_type in token_patterns:
                match = re.match(pattern, line)
                if match:
                    if token_type is None:
                        raise KavanaSyntaxError(
                            f"잘못된 문자열 형식입니다: 쌍따옴표를 사용해 주십시오 (\") 줄번호 {line_num}, 컬럼번호 {column_num}"
                        )

                    if token_type == TokenType.STRING:
                        string_token = CommandParser.parse_string_token(match.group(0), line_num, column_num)
                        tokens.append(string_token)
                    else:
                        raw_value = match.group(0)
                        value = raw_value
                        value_datatype_changed = TokenUtil.primitive_to_kavana_by_tokentype(value, token_type)
                        tokens.append(Token(data=value_datatype_changed, type=token_type, line=line_num, column=column_num))

                    column_num += len(match.group(0))
                    line = line[len(match.group(0)):]
                    matched = True
                    break

            if not matched and line:
                line = line[1:]
                column_num += 1

        tokens = CommandParser.post_process_tokens(tokens)
        return tokens


    @staticmethod
    def parse_string_token(raw_string: str, line_num: int, column_num: int) -> StringToken:
        match = re.match(r'(?i)(rf|fr|r|f)?("((?:\\.|[^"\\])*)")', raw_string)

        if not match:
            raise KavanaSyntaxError(f"잘못된 문자열 형식입니다: {raw_string}")

        prefix = (match.group(1) or "").lower()
        quoted = match.group(2)
        inner = match.group(3)

        is_raw = 'r' in prefix
        is_formatted = 'f' in prefix

        if is_raw:
            decoded = inner
        else:
            decoded = CommandParser.decode_escaped_string(inner)

        expressions = []
        if is_formatted:
            parts = re.split(r'(\{.*?\})', decoded)
            for part in parts:
                if part.startswith('{') and part.endswith('}'):
                    inner_expr = part[1:-1].strip()
                    expr_tokens = CommandParser.tokenize(PreprocessedLine(inner_expr, line_num, column_num))
                    expressions.append(expr_tokens)

        return StringToken(
            data=String(decoded),
            type=TokenType.STRING,
            line=line_num,
            column=column_num,
            is_raw=is_raw,
            is_formatted=is_formatted,
            expressions=expressions if expressions else None
        )


    # @staticmethod
    # def parse_string_token(raw_string: str, line_num: int, column_num: int) -> StringToken:
    #     import re

    #     # match = re.match(r'(?i)(r?f?|fr?)("((?:\\.|[^"\\])*)")', raw_string)
    #     match = re.match(r'(?i)(rf|fr|r|f)?("((?:\\.|[^"\\])*)")', raw_string)
    #     if not match:
    #         raise KavanaSyntaxError(f"잘못된 문자열 형식입니다: {raw_string}")

    #     prefix = match.group(1).lower()
    #     quoted = match.group(2)
    #     inner = match.group(3)

    #     is_raw = 'r' in prefix
    #     is_formatted = 'f' in prefix

    #     if is_raw:
    #         decoded = inner
    #     else:
    #         decoded = CommandParser.decode_escaped_string(inner)

    #     expressions = []
    #     if is_formatted:
    #         parts = re.split(r'(\{.*?\})', decoded)
    #         for part in parts:
    #             if part.startswith('{') and part.endswith('}'):
    #                 inner_expr = part[1:-1].strip()
    #                 expr_tokens = CommandParser.tokenize(PreprocessedLine(inner_expr, line_num, column_num))
    #                 expressions.append(expr_tokens)

    #     return StringToken(
    #         data=decoded,
    #         type=TokenType.STRING,
    #         line=line_num,
    #         column=column_num,
    #         is_raw=is_raw,
    #         is_formatted=is_formatted,
    #         expressions=expressions if expressions else None
    #     )


    @staticmethod
    def post_process_tokens(tokens: List[Token]) -> List[Token]:
        ''' Array, AccessIndexToken을 생성해서 대체한다'''
        if not tokens:
            return []

        processed_tokens = []
        i = 0

        while i < len(tokens):
            token = tokens[i]

            if CommandParser._is_access_index_start(tokens, i):
                access_token, i = CommandParser.make_access_index_token(tokens, i)
                processed_tokens.append(access_token)

            elif token.type == TokenType.LEFT_BRACKET:
                array_token, i = CommandParser.make_array_token(tokens, i)
                processed_tokens.append(array_token)
            elif token.type == TokenType.LEFT_BRACE:
                hash_token, i = CommandParser.make_hash_map_token(tokens, i)
                processed_tokens.append(hash_token)
            else:
                processed_tokens.append(token)
                i += 1

        return processed_tokens

    @staticmethod
    def _is_access_index_start(tokens: List[Token], i: int) -> bool:
        return (
            i + 1 < len(tokens)
            and tokens[i].type == TokenType.IDENTIFIER
            and tokens[i + 1].type == TokenType.LEFT_BRACKET
        )

    @staticmethod
    def make_hash_map_token(tokens: List[Token], start_index: int) -> Tuple[HashMapToken, int]:
        assert tokens[start_index].type == TokenType.LEFT_BRACE

        i = start_index + 1
        end_idx = CommandParser.find_matching_brace(tokens, start_index)
        hashmap_content: Dict[Union[str, int], List[Token]] = {}

        while i < end_idx:
            key_token = tokens[i]
            if key_token.type not in [TokenType.STRING, TokenType.INTEGER]:
                raise CommandParserError("HashMap의 key는 문자열 또는 정수만 가능합니다.", key_token.line, key_token.column)

            key = key_token.data.value
            i += 1

            if i >= len(tokens) or tokens[i].type != TokenType.COLON:
                raise CommandParserError("HashMap 항목에 ':' 구문이 빠졌습니다.", tokens[i].line, tokens[i].column)
            i += 1

            value_tokens = []
            while i < end_idx and tokens[i].type != TokenType.COMMA:
                if tokens[i].type == TokenType.LEFT_BRACE:
                    sub_hashmap_token, i = CommandParser.make_hash_map_token(tokens, i)
                    value_tokens.append(sub_hashmap_token)
                elif tokens[i].type == TokenType.LEFT_BRACKET:
                    sub_array_token, i = CommandParser.make_array_token(tokens, i)
                    value_tokens.append(sub_array_token)
                elif CommandParser._is_access_index_start(tokens, i):
                    access_token, i = CommandParser.make_access_index_token(tokens, i)
                    value_tokens.append(access_token)
                else:
                    value_tokens.append(tokens[i])
                    i += 1

            hashmap_content[key] = CommandParser.post_process_tokens(value_tokens)

            if i < end_idx and tokens[i].type == TokenType.COMMA:
                i += 1

        return HashMapToken(
            data=HashMap({}),
            key_express_map=hashmap_content
        ), end_idx + 1


    @staticmethod
    def find_matching_brace(tokens: List[Token], start_idx: int) -> int:
        count = 1
        i = start_idx + 1
        while i < len(tokens):
            if tokens[i].type == TokenType.LEFT_BRACE:
                count += 1 
            elif tokens[i].type == TokenType.RIGHT_BRACE:
                count -= 1
                if count == 0:
                    return i
            i += 1
        raise CommandParserError("HashMap 중괄호가 닫히지 않았습니다.", tokens[start_idx].line, tokens[start_idx].column)


    @staticmethod
    def make_access_index_token(tokens: List[Token], start_index: int) -> Tuple[AccessIndexToken, int]:
        var_name = tokens[start_index].data.value
        i = start_index + 1  # '[' 시작 위치
        end_idx = CommandParser.find_matching_bracket(tokens, i)
        row_sub, col_sub, pos = CommandParser.extract_row_column_expresses(tokens, i, end_idx)
        row_expr = CommandParser.post_process_tokens(row_sub)
        col_expr = CommandParser.post_process_tokens(col_sub) if col_sub else []

        return AccessIndexToken(data=String(var_name), row_express=row_expr, column_express=col_expr), pos + 1

    @staticmethod
    def make_array_token(tokens: List[Token], start_index: int) -> Tuple[ArrayToken, int]:
        list_elements = []
        current_element = []
        end_idx = CommandParser.find_matching_bracket(tokens, start_index)
        i = start_index + 1

        while i <= end_idx:
            token = tokens[i]

            if CommandParser._is_access_index_start(tokens, i):
                access_token, i = CommandParser.make_access_index_token(tokens, i)
                current_element.append(access_token)
                continue  # ✅ 이미 i가 이동됐으므로 skip

            elif token.type == TokenType.LEFT_BRACKET:
                sub_array_token, i = CommandParser.make_array_token(tokens, i)
                current_element.append(sub_array_token)
                continue  # ✅ i 이미 이동됨

            elif token.type == TokenType.COMMA:
                if current_element:
                    list_elements.append(CommandParser.post_process_tokens(current_element))
                    current_element = []
                i += 1
                continue

            elif token.type == TokenType.RIGHT_BRACKET:
                if current_element:
                    list_elements.append(CommandParser.post_process_tokens(current_element))
                break  # ✅ while 탈출 (i는 end_idx + 1로 반환됨)

            else:
                current_element.append(token)
                i += 1  # ✅ 일반 토큰일 경우에도 증가

        return ArrayToken(data=Array([]), element_expresses=list_elements), end_idx + 1


    @staticmethod
    def find_matching_bracket(tokens: List[Token], start_idx: int) -> int:
        """
        주어진 `start_idx` 위치의 `[`와 짝을 이루는 `]`의 위치를 찾는 함수.
        '['에서 시작 ']'의 index를 리턴한다.
        """
        count_bracket = 1  # `[`를 만나고 시작하므로 1로 초기화
        i = start_idx + 1

        while i < len(tokens):
            if tokens[i].type == TokenType.LEFT_BRACKET:
                count_bracket += 1
            elif tokens[i].type == TokenType.RIGHT_BRACKET:
                count_bracket -= 1
                if count_bracket == 0:
                    return i  # 짝을 이루는 `]`의 위치 반환
            i += 1

        raise CommandParserError("리스트 인덱싱의 괄호가 올바르게 닫히지 않았습니다.", tokens[start_idx].line, tokens[start_idx].column)


    @staticmethod
    def extract_row_column_expresses(tokens: List[Token], start_idx: int, end_idx: int) -> Tuple[List[Token], List[Token], int]:
        ''' 
        리스트 접근 표현식을 파싱하여 row_tokens, column_tokens, 마지막 index를 추출하는 함수.
        
        tokens[start_idx]는 반드시 LEFT_BRACKET ('[') 이어야 하며,
        COMMA (',')가 나오면 row와 column을 구분한다.
        
        `end_idx`를 사용하여 탐색 범위를 제한할 수 있도록 수정.
        '''
        
        if tokens[start_idx].type != TokenType.LEFT_BRACKET:
            raise CommandParserError("리스트 접근 표현식은 반드시 '['로 시작해야 합니다.", tokens[start_idx].line, tokens[start_idx].column)

        row_tokens = []
        column_tokens = []
        i = start_idx + 1  # '[' 다음부터 시작
        count_bracket = 1  # 처음 '['을 만났으므로 1로 시작
        is_row = True  # 처음에는 row를 채움

        while i <= end_idx:  # 🔥 end_idx까지만 탐색하도록 수정
            token = tokens[i]

            # 괄호 개수 카운팅
            if token.type == TokenType.LEFT_BRACKET:
                count_bracket += 1
            elif token.type == TokenType.RIGHT_BRACKET:
                count_bracket -= 1

            # ','를 만나면 column_tokens로 전환
            if token.type == TokenType.COMMA and count_bracket == 1:
                is_row = False
            elif token.type == TokenType.RIGHT_BRACKET and count_bracket == 0:
                break
            else:
                if is_row:
                    row_tokens.append(token)
                else:
                    column_tokens.append(token)

            i += 1

        # 괄호가 제대로 닫히지 않았는지 검사
        if count_bracket != 0:
            raise CommandParserError("리스트 인덱싱의 괄호가 올바르게 닫히지 않았습니다.", tokens[i].line, tokens[i].column)

        if len(row_tokens) == 0:
            raise CommandParserError("리스트 인덱스의 첫 번째 값(row)이 비어 있습니다.", tokens[start_idx].line, tokens[start_idx].column)

        return row_tokens, column_tokens, i

