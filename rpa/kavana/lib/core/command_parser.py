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
from lib.core.token import ArrayToken, AccessIndexToken, Express, HashMapToken, StringToken,  Token
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

            if cmd == "TRY":
                try_block, new_index = self.parse_try_block(processed_lines, i)
                parsed_commands.append(try_block)
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
                    raise KavanaSyntaxError("INCLUDE 문에 파일 경로가 필요합니다.")
                include_path = args[0].data.value.strip('"')  # ✅ Token 객체에서 값 추출
                self._include_process(include_path, parsed_commands)
                i += 1
                continue

            # ✅ LOAD 처리
            if cmd == "ENV_LOAD":
                if not args:
                    raise KavanaSyntaxError("ENV_LOAD 문에 .env 파일 경로가 필요합니다.")
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

    def parse_try_block(self, ppLines: List[PreprocessedLine], start_line: int):
        """
        TRY ... CATCH ... FINALLY ... END_TRY 블록 파싱
        """
        i = start_line
        try_body = []
        catch_body = []
        finally_body = []

        mode = "TRY"
        i = i+1  # ✅ TRY 블록 시작
        while i < len(ppLines):
            line = ppLines[i].text.strip().upper()

            if line == "CATCH":
                mode = "CATCH"
                i += 1
                continue
            elif line == "FINALLY":
                mode = "FINALLY"
                i += 1
                continue
            elif line == "END_TRY":
                break

            tokens = self.tokenize(ppLines[i])
            if not tokens:
                i += 1
                continue

            cmd = tokens[0].data.value.upper()
            args = tokens[1:]
            
            if cmd == "TRY":
                raise CommandParserError("TRY 블록 안에 또 TRY 블록이 있습니다.(내포된 TRY문을 지원하지 않습니다.)", ppLines[i].original_line, ppLines[i].original_column)

            command = {"cmd": cmd, "args": args}

            if cmd in ["IF", "WHILE", "FOR"]:
                nested_block, new_index = self.parse_block(ppLines, i + 1, f"END_{cmd}")
                command = {"cmd": f"{cmd}_BLOCK", "body": [{"cmd": cmd, "args": args}] + nested_block}
                i = new_index
            if mode == "TRY":
                try_body.append(command)
            elif mode == "CATCH":
                catch_body.append(command)
            elif mode == "FINALLY":
                finally_body.append(command)

            i += 1

        return {"cmd": "TRY_BLOCK", "try": try_body, "catch": catch_body, "finally": finally_body}, i

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
                    value_token = StringToken(data=String(value), type=TokenType.STRING)
                else:
                    value_token = StringToken(data=String(value), type=TokenType.STRING)

                # ✅ "=" 연산자 토큰 추가
                equals_token = StringToken(data=String("="), type=TokenType.ASSIGN)

                key_token = StringToken(data=String(f"${key}"), type=TokenType.IDENTIFIER)
                # ✅ `parsed_commands`에 추가하여 추적 가능
                parsed_commands.append({
                    "cmd": "CONST",
                    "args": [key_token, equals_token, value_token]
                })

    # @staticmethod
    # def tokenize(ppLine: PreprocessedLine) -> list:
    #     """한 줄을 `Token` 또는 `StringToken` 객체 리스트로 변환"""

    #     import re

    #     line = ppLine.text.strip()
    #     tokens = []

    #     string_pattern = r'(?i)(r?f?|fr?)("((?:\\.|[^"\\])*)")'  # 접두어 포함 문자열

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

    #         # ✅ 논리 연산자
    #         (r'(?i)\bAND\b', TokenType.LOGICAL_OPERATOR),
    #         (r'(?i)\bOR\b', TokenType.LOGICAL_OPERATOR),
    #         (r'(?i)\bNOT\b', TokenType.LOGICAL_OPERATOR),

    #         # ✅ 루프 제어
    #         (r'(?i)\bBREAK\b', TokenType.BREAK),
    #         (r'(?i)\bCONTINUE\b', TokenType.CONTINUE),

    #         # ✅ YmdTime 키워드
    #         (r"(?i)\bYmdTime\b", TokenType.IDENTIFIER),
    #         (r"(?i)\bYmd\b", TokenType.IDENTIFIER),

    #         # ✅ 작은따옴표 오류 감지
    #         (r"'([^']*)'", None),

    #         # ✅ 연산자 및 구문
    #         (r'\(', TokenType.LEFT_PAREN),
    #         (r'\)', TokenType.RIGHT_PAREN),
    #         (r'\[', TokenType.LEFT_BRACKET),
    #         (r'\]', TokenType.RIGHT_BRACKET),
    #         (r'\{', TokenType.LEFT_BRACE),
    #         (r'\}', TokenType.RIGHT_BRACE),
    #         (r',', TokenType.COMMA),
    #         (r':', TokenType.COLON),
    #         (r'==|!=|>=|<=|[+\-*/%<>]', TokenType.OPERATOR),
    #         (r'=', TokenType.ASSIGN),

    #         # ✅ 문자열 (접두어 포함 문자열은 따로 처리)
    #         (string_pattern, TokenType.STRING),
    #         # ✅ 식별자
    #         (r'[a-zA-Z_\$][a-zA-Z0-9_]*', TokenType.IDENTIFIER),

    #         # ✅ 숫자
    #         (r'\b\d+\.\d+|\.\d+|\d+\.\b', TokenType.FLOAT),
    #         (r'\b\d+\b', TokenType.INTEGER),

    #     ]

    #     column_num = ppLine.original_column
    #     line_num = ppLine.original_line

    #     while line:
    #         matched = False

    #         while line and line[0] == " ":
    #             column_num += 1
    #             line = line[1:]

    #         for pattern, token_type in token_patterns:
    #             match = re.match(pattern, line)
    #             if match:
    #                 if token_type is None:
    #                     raise KavanaSyntaxError(
    #                         f"잘못된 문자열 형식입니다: 쌍따옴표를 사용해 주십시오 (\") 줄번호 {line_num}, 컬럼번호 {column_num}"
    #                     )

    #                 if token_type == TokenType.STRING:
    #                     string_token = CommandParser.parse_string_token(match.group(0), line_num, column_num)
    #                     tokens.append(string_token)
    #                 else:
    #                     raw_value = match.group(0)
    #                     value = raw_value
    #                     value_datatype_changed = TokenUtil.primitive_to_kavana_by_tokentype(value, token_type)
    #                     tokens.append(Token(data=value_datatype_changed, type=token_type, line=line_num, column=column_num))

    #                 column_num += len(match.group(0))
    #                 line = line[len(match.group(0)):]
    #                 matched = True
    #                 break

    #         if not matched and line:
    #             line = line[1:]
    #             column_num += 1

    #     tokens = CommandParser.post_process_tokens(tokens)
    #     return tokens

    @staticmethod
    def tokenize(ppLine: PreprocessedLine) -> list:
        raw_tokens = CommandParser.pre_process_tokens(ppLine)
        return CommandParser.post_process_tokens(raw_tokens)

    @staticmethod
    def pre_process_tokens(ppLine: PreprocessedLine) -> List[Token]:
        """정규식 기반으로 Token 객체 리스트 생성 (전처리 단계)"""

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
        return tokens

    @staticmethod
    def parse_string_token(raw_string: str, line_num: int, column_num: int) -> StringToken:
        ''' 문자열을 파싱하여 StringToken 객체로 변환 '''
        import re
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
            decoded = TokenUtil.decode_escaped_string(inner)

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
    @staticmethod
    def _is_exists_token_type(tokens: List[Token], token_types: set) -> bool:
        """
        주어진 토큰 리스트에서 특정 토큰 타입이 존재하는지 확인하는 함수.
        :param tokens: Token 객체 리스트
        :param token_types: 확인할 TokenType 집합
        :return: 존재하면 True, 아니면 False
        """
        return any(token.type in token_types for token in tokens)
    @staticmethod
    def post_process_tokens(tokens: List[Token]) -> List[Token]:
        ''' ArrayToken, HashMapToken, AccessIndexToken을 판별하고 생성해서 대체한다'''
        if not tokens:
            return []

        processed_tokens = []
        i = 0
        # LeftBracket이 
        if not CommandParser._is_exists_token_type(tokens, {TokenType.LEFT_BRACE, TokenType.LEFT_BRACKET}):
            return tokens
        
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
        ''' 짝을 이루는 `}`의 위치를 찾는 함수 '''
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
        ''' AccessIndexToken을 생성하는 함수 '''
        var_name = tokens[start_index].data.value
        i = start_index + 1  # '[' 시작 위치
        end_idx = CommandParser._find_matching_bracket_index_for_access_token(tokens, i)
        expresses, pos = CommandParser._extract_index_expresses(tokens, i, end_idx)

        return AccessIndexToken(data=String(var_name), index_expresses = expresses), pos 

    @staticmethod
    def make_array_token(tokens: List[Token], start_index: int) -> Tuple[ArrayToken, int]:
        list_elements = []
        current_element = []
        end_idx = CommandParser._find_matching_bracket_index(tokens, start_index)
        i = start_index + 1

        while i <= end_idx:
            token = tokens[i]

            if CommandParser._is_access_index_start(tokens, i):
                access_token, i = CommandParser.make_access_index_token(tokens, i)
                current_element.append(access_token)
                continue  # ✅ 이미 i가 이동됐으므로 skip

            elif token.type == TokenType.LEFT_BRACKET:
                sub_tokens, i = CommandParser.make_array_token(tokens, i)
                current_element.append(sub_tokens)
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
            elif token.type ==  TokenType.LEFT_PAREN:
                # ✅ 괄호가 열리면 그 안의 내용을 모두 읽어야 함 [Point(1,2)]
                sub_tokens, i = CommandParser._extract_sub_tokens(tokens, i, TokenType.LEFT_PAREN)
                current_element.extend(sub_tokens)
                continue
            else:
                current_element.append(token)
                i += 1  # ✅ 일반 토큰일 경우에도 증가

        return ArrayToken(data=Array([]), element_expresses=list_elements), end_idx + 1

    @staticmethod
    def _extract_sub_tokens(tokens: List['Token'], start_idx: int,
                            left_token_type: 'TokenType') -> Tuple[List['Token'], int]:
        """
        괄호로 감싸진 sub token들을 추출한다.
        - 예: (a, b + c) → ['a', ',', 'b', '+', 'c']
        - 입력: 시작 토큰은 반드시 left_token_type 이어야 함
        - 반환: (추출된 토큰 리스트, 닫히는 괄호의 다음 인덱스)
        """
        if tokens[start_idx].type != left_token_type:
            raise CommandParserError(f"시작 토큰은 {left_token_type}이어야 합니다.", tokens[start_idx].line, tokens[start_idx].column)

        sub_tokens = []
        sub_tokens.append(tokens[start_idx])  # 시작 토큰 추가
        stack = [left_token_type]
        i = start_idx + 1

        while i < len(tokens):
            token = tokens[i]

            # 열리는 괄호들 처리
            if token.type in (TokenType.LEFT_PAREN, TokenType.LEFT_BRACE, TokenType.LEFT_BRACKET):
                stack.append(token.type)

            # 닫히는 괄호들 처리
            elif token.type in (TokenType.RIGHT_PAREN, TokenType.RIGHT_BRACE, TokenType.RIGHT_BRACKET):
                if not stack:
                    raise CommandParserError("괄호 짝이 맞지 않습니다.", token.line, token.column)

                expected = {
                    TokenType.RIGHT_PAREN: TokenType.LEFT_PAREN,
                    TokenType.RIGHT_BRACE: TokenType.LEFT_BRACE,
                    TokenType.RIGHT_BRACKET: TokenType.LEFT_BRACKET
                }[token.type]

                if stack[-1] != expected:
                    raise CommandParserError(f"예상과 다른 닫는 괄호: {token.type}", token.line, token.column)

                stack.pop()

                if not stack:  # 완전히 닫혔다면 종료
                    sub_tokens.append(tokens[i]) # 닫는 괄호 추가
                    return sub_tokens, i + 1

            sub_tokens.append(token)
            i += 1

        raise CommandParserError("괄호가 닫히지 않았습니다.", tokens[start_idx].line, tokens[start_idx].column)

    @staticmethod
    def _find_matching_bracket_index(tokens: List[Token], start_idx: int) -> int:
        """
        주어진 `start_idx` 위치의 `[`와 짝을 이루는 `]`의 위치를 찾는 함수.
        - 중첩된 (), [], {} 안에서도 정확하게 괄호 짝을 맞춤
        - 연속된 인덱싱 (예: list[0][1]) 에서도 첫 `]`를 정확히 찾아냄
        """
        if tokens[start_idx].type != TokenType.LEFT_BRACKET:
            raise CommandParserError("'[' 로 시작해야 합니다.", tokens[start_idx].line, tokens[start_idx].column)

        stack = [TokenType.LEFT_BRACKET]
        i = start_idx + 1

        while i < len(tokens):
            token = tokens[i]

            if token.type in (TokenType.LEFT_BRACKET, TokenType.LEFT_PAREN, TokenType.LEFT_BRACE):
                stack.append(token.type)

            elif token.type == TokenType.RIGHT_BRACKET:
                if not stack or stack[-1] != TokenType.LEFT_BRACKET:
                    raise CommandParserError("']' 괄호가 예상과 다릅니다.", token.line, token.column)
                stack.pop()
                if not stack:
                    return i  # 첫 번째 닫히는 ] 짝을 찾았을 때 종료

            elif token.type == TokenType.RIGHT_PAREN:
                if not stack or stack[-1] != TokenType.LEFT_PAREN:
                    raise CommandParserError("')' 괄호가 예상과 다릅니다.", token.line, token.column)
                stack.pop()

            elif token.type == TokenType.RIGHT_BRACE:
                if not stack or stack[-1] != TokenType.LEFT_BRACE:
                    raise CommandParserError("'}' 괄호가 예상과 다릅니다.", token.line, token.column)
                stack.pop()

            i += 1

        raise CommandParserError("리스트 인덱싱의 괄호가 올바르게 닫히지 않았습니다.", tokens[start_idx].line, tokens[start_idx].column)


    @staticmethod
    def _find_matching_bracket_index_for_access_token(tokens: List[Token], start_idx: int) -> int:
        """
        중첩된 리스트, 딕셔너리, 튜플 인덱싱 등을 처리할 수 있도록
        괄호 종류를 모두 고려하여 짝이 맞는 `]`의 위치를 반환
        """
        if tokens[start_idx].type != TokenType.LEFT_BRACKET:
            raise CommandParserError("리스트 인덱싱은 '['로 시작해야 합니다.", tokens[start_idx].line, tokens[start_idx].column)

        stack = [TokenType.LEFT_BRACKET]  # 시작은 '['로 보장됨
        i = start_idx + 1

        while i < len(tokens):
            token = tokens[i]

            if token.type in (TokenType.LEFT_BRACKET, TokenType.LEFT_PAREN, TokenType.LEFT_BRACE):
                stack.append(token.type)

            elif token.type == TokenType.RIGHT_BRACKET:
                if not stack:
                    raise CommandParserError("괄호 짝이 맞지 않습니다.", token.line, token.column)
                if stack[-1] == TokenType.LEFT_BRACKET:
                    stack.pop()
                    if not stack:
                        # ✅ 다음 토큰이 또 [ 이면 아직 전체 인덱싱 구조가 안 끝난 것
                        if i + 1 < len(tokens) and tokens[i + 1].type == TokenType.LEFT_BRACKET:
                            # 다음 인덱싱 구조 시작이므로 계속 진행
                            pass
                        else:
                            return i  # 진짜 끝
                else:
                    raise CommandParserError("잘못된 괄호 닫힘: ']' 앞에 '['가 없습니다.", token.line, token.column)

            elif token.type == TokenType.RIGHT_PAREN:
                if not stack or stack[-1] != TokenType.LEFT_PAREN:
                    raise CommandParserError("잘못된 괄호 닫힘: ')' 앞에 '('가 없습니다.", token.line, token.column)
                stack.pop()
            elif token.type == TokenType.RIGHT_BRACE:
                if not stack or stack[-1] != TokenType.LEFT_BRACE:
                    raise CommandParserError("잘못된 괄호 닫힘: '}' 앞에 '{'가 없습니다.", token.line, token.column)
                stack.pop()

            i += 1

        raise CommandParserError("리스트 인덱싱의 괄호가 올바르게 닫히지 않았습니다.", tokens[start_idx].line, tokens[start_idx].column)

    @staticmethod
    def _extract_index_expresses(tokens: List[Token], start_idx: int, end_idx: int) -> Tuple[List[Express], int]:
        if tokens[start_idx].type != TokenType.LEFT_BRACKET:
            raise CommandParserError("리스트 인덱싱은 반드시 '['로 시작해야 합니다.", tokens[start_idx].line, tokens[start_idx].column)

        expresses: List[Express] = []
        i = start_idx

        while i <= end_idx:
            if tokens[i].type != TokenType.LEFT_BRACKET:
                raise CommandParserError("인덱스는 '['로 시작해야 합니다.", tokens[i].line, tokens[i].column)

            close_idx = CommandParser._find_matching_bracket_index(tokens, i)
            if close_idx > end_idx:
                raise CommandParserError("']'의 위치가 잘못되었습니다.", tokens[i].line, tokens[i].column)

            sub_expr = tokens[i + 1 : close_idx]
            if not sub_expr:
                raise CommandParserError("인덱스 안의 표현식이 비어 있습니다.", tokens[i].line, tokens[i].column)

            expresses.append(sub_expr)
            i = close_idx + 1

        return expresses, i
