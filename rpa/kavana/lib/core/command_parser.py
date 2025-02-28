import codecs
import re
import os
from typing import List
from lib.core.command_preprocessor import PreprocessedLine
from lib.core.token import Token
from lib.core.datatypes.token_type import TokenType
from lib.core.function_registry import FunctionRegistry

class CommandParser:
    """
    Kavana 스크립트의 명령어를 분석하는 파서.
    - `main ... end_main` 블록 안에서 실행
    - `INCLUDE` → 외부 KVS 파일 포함
    - `LOAD` → .env 파일을 불러와 `SET`으로 변환
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
            # tokens = self.tokenize(processed_lines[i], i+1)  # ✅ `Token` 객체 리스트 반환
            tokens = self.tokenize(processed_lines[i])  # ✅ `Token` 객체 리스트 반환
            if not tokens:
                i += 1
                continue

            cmd = tokens[0].value.upper()  # ✅ 명령어는 대문자로 변환
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
                include_path = args[0].value.strip('"')  # ✅ Token 객체에서 값 추출
                self._process_include(include_path, parsed_commands)
                i += 1
                continue

            # ✅ LOAD 처리
            if cmd == "LOAD":
                if not args:
                    raise SyntaxError("LOAD 문에 .env 파일 경로가 필요합니다.")
                env_path = args[0].value.strip('"')  # ✅ Token 객체에서 값 추출
                self._process_env(env_path, parsed_commands)
                i += 1
                continue

            # ✅ MAIN 블록 처리
            if cmd == "MAIN":
                if not getattr(self, "ignore_main_check", False):
                    if self.in_main_block:
                        raise SyntaxError("Nested 'MAIN' blocks are not allowed. line : {i+1}")
                    self.in_main_block = True
                i += 1
                continue

            if cmd == "END_MAIN":
                if not getattr(self, "ignore_main_check", False):
                    if not self.in_main_block:
                        raise SyntaxError("'END_MAIN' found without 'MAIN'.")
                    self.in_main_block = False
                i += 1
                break

            # ✅ MAIN 블록 외부에서 명령어 사용 제한
            if not self.in_main_block and not getattr(self, "ignore_main_check", False):
                raise SyntaxError("Commands must be inside a 'MAIN' block. line : {i+1}")

            # ✅ 일반 명령어 추가
            parsed_commands.append({"cmd": cmd, "args": args})  # ✅ `args`도 `Token` 리스트로 저장
            i += 1  

        if self.in_main_block:
            raise SyntaxError("Missing 'END_MAIN' at the end of the script.")

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

            cmd = tokens[0].value.upper()
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

        raise SyntaxError(f"{end_keyword}가 없습니다.")  # ✅ 종료 키워드가 없으면 오류 발생

    def parse_function(self, ppLines:List[PreprocessedLine], start_line):
        """FUNCTION 블록을 파싱하는 함수"""
        func_def_lines = [ppLines[start_line]]
        i = start_line + 1

        while i < len(ppLines) and ppLines[i].text.strip().upper() != "END_FUNCTION":
            func_def_lines.append(ppLines[i])
            i += 1

        if i >= len(ppLines) or ppLines[i].strip().upper() != "END_FUNCTION":
            raise SyntaxError("함수 정의에서 END_FUNCTION이 누락되었습니다.")
        i += 1  # ✅ END_FUNCTION 스킵

        # ✅ 함수 헤더 파싱
        header_tokens = self.tokenize(func_def_lines[0])
        if len(header_tokens) < 2:
            raise SyntaxError("함수 정의 헤더가 올바르지 않습니다.")

        func_name = header_tokens[1]
        params = []
        
        if len(header_tokens) > 2 and header_tokens[2] == "(":
            param_str = " ".join(header_tokens[3:]).rstrip(")")
            params = [p.strip() for p in param_str.split(",")]
        elif len(header_tokens) > 2:
            params = header_tokens[2:]

        # func_body = "\n".join(func_def_lines[1:])
        func_body = func_def_lines[1:]
        
        # ✅ FunctionRegistry에 등록
        FunctionRegistry.register_function(func_name, params, func_body)
        return i  # ✅ 함수 정의 후 새로운 인덱스 반환


    def parse_function_definition(self, lines: List[str]) -> dict:
        """
        함수 정의 블록을 파싱하여 함수 이름, 매개변수, 본문을 추출.
        예)
        FUNCTION plus(a, b)
            set c = a + b
            return c
        END_FUNCTION
        """
        header_line = lines[0].strip()
        header_tokens = self.tokenize(header_line)
        if len(header_tokens) < 2:
            raise SyntaxError("함수 정의 헤더가 올바르지 않습니다.")
        func_name = header_tokens[1]
        params = []
        # 헤더에 괄호가 있으면 파라미터 추출: FUNCTION plus(a, b) 또는 FUNCTION plus ( a, b )
        if len(header_tokens) > 2 and header_tokens[2] == "(":
            i = 3
            while i < len(header_tokens) and header_tokens[i] != ")":
                params.append(header_tokens[i])
                i += 1
        elif len(header_tokens) > 2:
            # 괄호 없이 바로 매개변수가 나오는 경우: FUNCTION plus a, b
            params = header_tokens[2:]
        # 함수 본문: 헤더와 END_FUNCTION을 제외한 부분
        body_lines = lines[1:-1]
        func_body = "\n".join(body_lines)
        return {"name": func_name, "params": params, "body": func_body}


    def _process_include(self, include_path, parsed_commands):
        """INCLUDE 문을 처리하여 외부 KVS 파일을 불러온다."""
        full_path = os.path.join(self.base_path, include_path)

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"INCLUDE 파일을 찾을 수 없습니다: {full_path}")

        with open(full_path, "r", encoding="utf-8") as file:
            included_lines = file.readlines()

        # ✅ 기존 상태 저장
        original_main_state = self.in_main_block
        original_ignore_main_check = getattr(self, "ignore_main_check", False)

        # ✅ INCLUDE 실행 중에는 MAIN 블록 여부를 무시하도록 설정
        self.ignore_main_check = True

        included_parser = CommandParser(included_lines, self.base_path)
        included_parser.ignore_main_check = True  # ✅ 서브 파서에서도 MAIN 블록 검사 무시

        included_commands = included_parser.parse()

        # ✅ INCLUDE 완료 후 원래 상태 복원
        self.ignore_main_check = original_ignore_main_check

        parsed_commands.extend(included_commands)  # INCLUDE된 명령어 추가

    def _process_env(self, env_path, parsed_commands):
        """LOAD 문을 처리하여 .env 파일을 변수로 변환"""
        full_path = os.path.join(self.base_path, env_path)

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"LOAD 파일을 찾을 수 없습니다: {full_path}")

        with open(full_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):  # 주석 및 빈 줄 무시
                    continue
                
                if "=" not in line:
                    raise SyntaxError(f"잘못된 환경 변수 형식: {line}")

                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()

                # ✅ 숫자, 불리언, 문자열 구분
                if value.lower() in ["true", "false"]:
                    value = value.lower()
                elif value.isdigit():
                    value = int(value)
                else:
                    value = f'"{value}"'  # ✅ 문자열로 처리

                parsed_commands.append({"cmd": "SET", "args": [key, "=", value]})

    @staticmethod
    # def tokenize(line: str, line_num: int) -> list:
    def tokenize(ppLine: PreprocessedLine) -> list:
        """한 줄을 `Token` 객체 리스트로 변환"""

        line = ppLine.text.strip()
        tokens = []

        token_patterns = [

            # ✅ 논리 값
            (r'\bTrue\b', TokenType.BOOLEAN),
            (r'\bFalse\b', TokenType.BOOLEAN),
            (r'\bNone\b', TokenType.NONE),

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
            (r'(?i)\bLOAD\b', TokenType.LOAD),
            (r'(?i)\bMAIN\b', TokenType.MAIN),
            (r'(?i)\bEND_MAIN\b', TokenType.END_MAIN),

            # ✅ 논리 연산자
            (r'(?i)\bAND\b', TokenType.LOGICAL_OPERATOR), 
            (r'(?i)\bOR\b', TokenType.LOGICAL_OPERATOR), 
            (r'(?i)\bNOT\b', TokenType.LOGICAL_OPERATOR),

            # ✅ 루프 제어 키워드
            (r'(?i)\bBREAK\b', TokenType.BREAK),
            (r'(?i)\bCONTINUE\b', TokenType.CONTINUE),

            # ✅ 데이터 타입 키워드
            (r'(?i)\bDATE\b', TokenType.DATE),
            (r'(?i)\bPOINT\b', TokenType.POINT),
            (r'(?i)\bREGION\b', TokenType.REGION),
            (r'(?i)\bRECTANGLE\b', TokenType.RECTANGLE),
            (r'(?i)\bIMAGE\b', TokenType.IMAGE),
            (r'(?i)\bWINDOW\b', TokenType.WINDOW),  
            (r'(?i)\bAPPLICATION\b', TokenType.APPLICATION),
            # ✅ 연산자
            (r'\(', TokenType.LEFT_PAREN),
            (r'\)', TokenType.RIGHT_PAREN),
            (r'\[', TokenType.LEFT_BRACKET),
            (r'\]', TokenType.RIGHT_BRACKET),
            (r',', TokenType.COMMA),

            # ✅ 일반 식별자  
            (r'[a-zA-Z_\$][a-zA-Z0-9_]*', TokenType.IDENTIFIER),

            # ✅ float, integer
            (r'\b\d+\.\d+|\.\d+|\d+\.\b', TokenType.FLOAT),  # 🔥 소수점만 있는 경우도 포함
            (r'\b\d+\b', TokenType.INTEGER),         # 정수 (예: 10, 42, 1000)

            # ✅ OPERATOR
            (r'[+\-*/=%]', TokenType.OPERATOR),

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

                    if token_type == TokenType.STRING:
                        value = CommandParser.decode_escaped_string(raw_value)  # ✅ 직접 변환 함수 호출
                    else:
                        value = raw_value

                    tokens.append(Token(value=value, type=token_type, line=line_num, column=column_num))

                    column_num += len(match.group(0))
                    line = line[len(match.group(0)):]  # ✅ `line`을 올바르게 줄임

                    matched = True
                    break

            if not matched and line:  # ✅ 더 이상 처리할 수 없는 문자가 있으면 예외 발생
                raise SyntaxError(f"Unknown token at line {line_num}, column {column_num}")

        return tokens

    @staticmethod
    def tokenize0(line: str, line_num: int) -> list:
        """한 줄을 `Token` 객체 리스트로 변환"""
        line = line.strip()
        tokens = []

        token_patterns = [

            # ✅ 논리 값
            (r'\bTrue\b', TokenType.BOOLEAN),
            (r'\bFalse\b', TokenType.BOOLEAN),
            (r'\bNone\b', TokenType.NONE),

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
            (r'(?i)\bLOAD\b', TokenType.LOAD),
            (r'(?i)\bMAIN\b', TokenType.MAIN),
            (r'(?i)\bEND_MAIN\b', TokenType.END_MAIN),

            # ✅ 논리 연산자
            (r'(?i)\bAND\b', TokenType.LOGICAL_OPERATOR), 
            (r'(?i)\bOR\b', TokenType.LOGICAL_OPERATOR), 
            (r'(?i)\bNOT\b', TokenType.LOGICAL_OPERATOR),

            # ✅ 루프 제어 키워드
            (r'(?i)\bBREAK\b', TokenType.BREAK),
            (r'(?i)\bCONTINUE\b', TokenType.CONTINUE),

            # ✅ 데이터 타입 키워드
            (r'(?i)\bDATE\b', TokenType.DATE),
            (r'(?i)\bPOINT\b', TokenType.POINT),
            (r'(?i)\bREGION\b', TokenType.REGION),
            (r'(?i)\bRECTANGLE\b', TokenType.RECTANGLE),
            (r'(?i)\bIMAGE\b', TokenType.IMAGE),
            (r'(?i)\bWINDOW\b', TokenType.WINDOW),  
            (r'(?i)\bAPPLICATION\b', TokenType.APPLICATION),
            # ✅ 연산자
            (r'\(', TokenType.LEFT_PAREN),
            (r'\)', TokenType.RIGHT_PAREN),
            (r'\[', TokenType.LEFT_BRACKET),
            (r'\]', TokenType.RIGHT_BRACKET),
            (r',', TokenType.COMMA),

            # ✅ 일반 식별자  
            (r'[a-zA-Z_\$][a-zA-Z0-9_]*', TokenType.IDENTIFIER),

            # ✅ float, integer
            (r'\b\d+\.\d+|\.\d+|\d+\.\b', TokenType.FLOAT),  # 🔥 소수점만 있는 경우도 포함
            (r'\b\d+\b', TokenType.INTEGER),         # 정수 (예: 10, 42, 1000)

            # ✅ OPERATOR
            (r'[+\-*/=%]', TokenType.OPERATOR),

            # ✅ 모든 유니코드 문자 포함          
            (r'"((?:\\.|[^"\\])*)"', TokenType.STRING),  # ✅ 문자열 정규식 수정
        ]
        column = 0
        while line:
            matched = False

            # 🔥 공백을 건너뛰고 column 조정
            while line and line[0] == " ":
                column += 1
                line = line[1:]

            for pattern, token_type in token_patterns:
                match = re.match(pattern, line)
                if match:
                    raw_value = match.group(1) if token_type == TokenType.STRING else match.group(0)

                    if token_type == TokenType.STRING:
                        value = CommandParser.decode_escaped_string(raw_value)  # ✅ 직접 변환 함수 호출
                    else:
                        value = raw_value

                    tokens.append(Token(value=value, type=token_type, line=line_num, column=column))

                    column += len(match.group(0))
                    line = line[len(match.group(0)):]  # ✅ `line`을 올바르게 줄임

                    matched = True
                    break

            if not matched and line:  # ✅ 더 이상 처리할 수 없는 문자가 있으면 예외 발생
                raise SyntaxError(f"Unknown token at line {line_num}, column {column}")

        return tokens
    
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