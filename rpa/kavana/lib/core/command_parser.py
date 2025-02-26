import re
import os
from typing import List

from lib.core.function_registry import FunctionRegistry

class CommandParser:
    """
    Kavana 스크립트의 명령어를 분석하는 파서.
    - `main ... end_main` 블록 안에서 실행
    - `INCLUDE` → 외부 KVS 파일 포함
    - `LOAD` → .env 파일을 불러와 `SET`으로 변환
    """
    def __init__(self, script_lines, base_path="."):
        self.script_lines = script_lines
        self.base_path = base_path  # 스크립트 기본 경로 (INCLUDE, LOAD 처리용)
        self.in_main_block = False

    def preprocess_lines(self):
        """멀티라인 (`\\`) 연결 및 주석 (`//`) 제거"""
        merged_lines = []
        current_line = ""

        for line in self.script_lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("//"):
                continue  # 빈 줄 및 주석 제거
            # 라인 중 //이 나오면 //이후는 삭제 후 추가
            

            if stripped.endswith("\\"):
                current_line += stripped[:-1] + " "  # `\` 제거 후 다음 줄 연결
            else:
                if "//" in stripped:
                    stripped = stripped[:stripped.index("//")]                
                current_line += stripped
                merged_lines.append(current_line)
                current_line = ""  # 새로운 줄 시작

        return merged_lines

    def parse(self):
        """
        스크립트의 모든 명령어를 분석하여 리스트로 반환.
        - `INCLUDE "./scripts/common.kvs"` → 외부 파일 불러오기
        - `LOAD "./config.env"` → 환경 변수 불러오기
        - `SET name = "홍길동"` → 변수 설정
        """
        parsed_commands = []
        processed_lines = self.preprocess_lines()

        i = 0  # ✅ i 변수 초기화
        while i < len(processed_lines):  # ✅ while 루프로 변경
            line = processed_lines[i]
            tokens = self.tokenize(line)
            if not tokens:
                i += 1  # ✅ 빈 줄일 경우 i 증가
                continue

            cmd_original = tokens[0]  # 원본 명령어 유지
            cmd = cmd_original.upper()  # ✅ 명령어만 대문자로 변환
            args = tokens[1:]  # ✅ 인자는 원본 그대로 유지

            # ✅ PRINT("hello") 같은 함수 호출 처리
            if "(" in cmd_original and cmd_original.endswith(")"):
                func_match = re.match(r'(\w+)\((.*)\)', cmd_original)
                if func_match:
                    cmd = func_match.group(1).upper()  # ✅ 명령어만 대문자로 변환
                    raw_args = func_match.group(2)  # ✅ 괄호 안의 내용 원본 유지

                    # ✅ 함수 인자 여러 개 처리 (PRINT("hello", "world"))
                    args = [arg.strip() for arg in raw_args.split(",")]
            # ✅ IF 블록 처리 (cmd + args 리스트로 변환)
            if cmd == "IF":
                block_body = []  # IF 내부 명령어 리스트
                block_body.append({"cmd": cmd, "args": args})  # IF 헤더 저장
                i += 1

                while i < len(processed_lines) and processed_lines[i].strip().upper() not in ["END_IF"]:
                    inner_tokens = self.tokenize(processed_lines[i])
                    if inner_tokens:
                        block_body.append({"cmd": inner_tokens[0].upper(), "args": inner_tokens[1:]})
                    i += 1

                if i >= len(processed_lines) or processed_lines[i].strip().upper() != "END_IF":
                    raise SyntaxError("IF 문에서 END_IF가 필요합니다.")
                i += 1  # END_IF 스킵

                parsed_commands.append({"cmd": "IF_BLOCK", "body": block_body})
                continue

            # ✅ WHILE 블록 처리
            if cmd == "WHILE":
                block_body = [{"cmd": cmd, "args": args}]
                i += 1

                while i < len(processed_lines) and processed_lines[i].strip().upper() != "END_WHILE":
                    inner_tokens = self.tokenize(processed_lines[i])
                    if inner_tokens:
                        block_body.append({"cmd": inner_tokens[0].upper(), "args": inner_tokens[1:]})
                    i += 1

                if i >= len(processed_lines) or processed_lines[i].strip().upper() != "END_WHILE":
                    raise SyntaxError("WHILE 문에서 END_WHILE이 필요합니다.")
                i += 1  # END_WHILE 스킵

                parsed_commands.append({"cmd": "WHILE_BLOCK", "body": block_body})
                continue

            # ✅ FOR 블록 처리
            if cmd == "FOR":
                block_body = [{"cmd": cmd, "args": args}]
                i += 1

                while i < len(processed_lines) and processed_lines[i].strip().upper() != "END_FOR":
                    inner_tokens = self.tokenize(processed_lines[i])
                    if inner_tokens:
                        block_body.append({"cmd": inner_tokens[0].upper(), "args": inner_tokens[1:]})
                    i += 1

                if i >= len(processed_lines) or processed_lines[i].strip().upper() != "END_FOR":
                    raise SyntaxError("FOR 문에서 END_FOR이 필요합니다.")
                i += 1  # END_FOR 스킵

                parsed_commands.append({"cmd": "FOR_BLOCK", "body": block_body})
                continue

            # 함수 정의 처리: FUNCTION으로 시작하면 END_FUNCTION까지 읽음
            if cmd == "FUNCTION":
                func_def_lines = [line]  # FUNCTION 줄을 포함시킴
                i += 1  # FUNCTION 줄 다음 줄부터 시작

                # FUNCTION 줄부터 END_FUNCTION까지 모두 읽음
                while i < len(processed_lines) and processed_lines[i].strip().upper() != "END_FUNCTION":
                    func_def_lines.append(processed_lines[i])
                    i += 1

                # END_FUNCTION 줄은 추가하지 않음
                if i >= len(processed_lines) or processed_lines[i].strip().upper() != "END_FUNCTION":
                    raise SyntaxError("함수 정의에서 END_FUNCTION이 누락되었습니다.")
                i += 1  # END_FUNCTION 줄을 건너�

                # 함수 헤더 파싱: FUNCTION plus(a, b)
                header_line = func_def_lines[0].strip()  # FUNCTION 줄
                header_tokens = self.tokenize(header_line)
                if len(header_tokens) < 2:
                    raise SyntaxError("함수 정의 헤더가 올바르지 않습니다.")

                func_name = header_tokens[1]  # 함수 이름 추출
                params = []

                # 매개변수 추출: FUNCTION plus(a, b) 또는 FUNCTION plus a, b
                if len(header_tokens) > 2 and header_tokens[2] == "(":
                    # 괄호 안의 매개변수 추출
                    param_str = " ".join(header_tokens[3:])
                    param_str = param_str.rstrip(")")  # 닫는 괄호 제거
                    params = [p.strip() for p in param_str.split(",")]
                elif len(header_tokens) > 2:
                    # 괄호 없이 매개변수가 나오는 경우
                    params = [p.strip() for p in header_tokens[2:]]

                # 함수 본문 추출: 헤더를 제외한 나머지 줄
                func_body = "\n".join(func_def_lines[1:])

                # FunctionRegistry에 등록
                FunctionRegistry.register_function(func_name, params, func_body)
                continue  # 함수 정의는 parsed_commands에 추가하지 않음

            if cmd == "INCLUDE":
                if not args:
                    raise SyntaxError("INCLUDE 문에 파일 경로가 필요합니다.")
                include_path = args[0].strip('"')  # 따옴표 제거
                self._process_include(include_path, parsed_commands)
                i += 1  # ✅ INCLUDE 처리 후 i 증가
                continue

            if cmd == "LOAD":
                if not args:
                    raise SyntaxError("LOAD 문에 .env 파일 경로가 필요합니다.")
                env_path = args[0].strip('"')  # 따옴표 제거
                self._process_env(env_path, parsed_commands)
                i += 1  # ✅ LOAD 처리 후 i 증가
                continue

            if cmd == "MAIN":
                if not getattr(self, "ignore_main_check", False):  # ✅ MAIN 검사 무시 여부 확인
                    if self.in_main_block:
                        raise SyntaxError("Nested 'MAIN' blocks are not allowed.")
                    self.in_main_block = True
                i += 1  # ✅ MAIN 처리 후 i 증가
                continue  # `MAIN` 자체는 저장하지 않음

            elif cmd == "END_MAIN":
                if not getattr(self, "ignore_main_check", False):  # ✅ MAIN 검사 무시 여부 확인
                    if not self.in_main_block and not getattr(self, "ignore_main_check", False): 
                        raise SyntaxError("'END_MAIN' found without 'MAIN'.")
                    self.in_main_block = False
                i += 1  # ✅ END_MAIN 처리 후 i 증가
                break  # `END_MAIN` 이후 명령어는 무시

            elif not self.in_main_block and not getattr(self, "ignore_main_check", False): 
                raise SyntaxError("Commands must be inside a 'MAIN' block.")

            parsed_commands.append({"cmd": cmd, "args": args})
            i += 1  # ✅ 일반 명령어 처리 후 i 증가

        if self.in_main_block:
            raise SyntaxError("Missing 'END_MAIN' at the end of the script.")

        return parsed_commands
    
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
    def tokenize(line: str) -> List[str]:
        """명령어를 토큰 리스트로 변환"""
        line = line.strip()

        # ✅ FUNCTION 명령어 처리 (괄호 있는 경우와 없는 경우)
        func_match = re.match(r'^(FUNCTION)\s+(\w+)\s*\(?([^()]*)\)?$', line, re.IGNORECASE)
        if func_match:
            cmd = func_match.group(1).upper()   # FUNCTION
            func_name = func_match.group(2)     # myfunc
            args = func_match.group(3).strip()  # "a,b" 또는 "a b"

            # ✅ 쉼표 제거하고 인자 분리
            split_args = re.findall(r'".*?"|\w+', args)
            return [cmd, func_name] + split_args

        # ✅ 일반 함수형 명령어 처리 (PRINT("hello", "world"))
        func_call_match = re.match(r'^(\w+)\((.*)\)$', line)
        if func_call_match:
            cmd = func_call_match.group(1).upper()  # PRINT 같은 명령어
            args = func_call_match.group(2).strip()  # "hello", "world"

            # ✅ 쉼표로 구분된 인자 분리 (쉼표 없이 공백 구분도 처리)
            split_args = re.findall(r'".*?"|\w+', args)
            return [cmd] + split_args

        # ✅ 일반 명령어 처리 (PRINT "Hello World", SET x = 10, IF a and b)
        # tokens = re.findall(r'".*?"|\S+', line)
        tokens = re.findall(r'<=|>=|==|!=|[()+\-*/%=<>]|[-+]?[0-9]*\.?[0-9]+|"[^"]*"|[a-zA-Z_][a-zA-Z0-9_]*', line)

        # ✅ boolean 예약어 대문자로 변환
        reserved = {"and", "or", "not"}
        tokens = [t.upper() if t.lower() in reserved else t for t in tokens]

        return tokens    
    
#     test_cases = [
#     "FUNCTION myfunc a,b",       # → ['FUNCTION', 'myfunc', 'a', 'b']
#     "FUNCTION myfunc(a,b)",      # → ['FUNCTION', 'myfunc', 'a', 'b']
#     "FUNCTION myfunc ( a , b )", # → ['FUNCTION', 'myfunc', 'a', 'b']
#     'PRINT "Hello World"',       # → ['PRINT', '"Hello World"']
#     'PRINT("hello {name}")',     # → ['PRINT', '"hello {name}"']
#     'PRINT("hello", "world")',   # → ['PRINT', '"hello"', '"world"']
#     'SET x = 10',                # → ['SET', 'x', '=', '10']
#     'IF a and b',                # → ['IF', 'a', 'AND', 'b']
# ]