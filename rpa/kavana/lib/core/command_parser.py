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
        """
        parsed_commands = []
        processed_lines = self.preprocess_lines()
        i = 0  

        while i < len(processed_lines):
            tokens = self.tokenize(processed_lines[i])
            if not tokens:
                i += 1
                continue

            cmd = tokens[0].upper()
            args = tokens[1:]

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
                continue  # 함수 정의는 parsed_commands에 추가하지 않음

            # ✅ INCLUDE 처리
            if cmd == "INCLUDE":
                if not args:
                    raise SyntaxError("INCLUDE 문에 파일 경로가 필요합니다.")
                include_path = args[0].strip('"')
                self._process_include(include_path, parsed_commands)
                i += 1
                continue

            # ✅ LOAD 처리
            if cmd == "LOAD":
                if not args:
                    raise SyntaxError("LOAD 문에 .env 파일 경로가 필요합니다.")
                env_path = args[0].strip('"')
                self._process_env(env_path, parsed_commands)
                i += 1
                continue

            # ✅ MAIN 블록 처리
            if cmd == "MAIN":
                if not getattr(self, "ignore_main_check", False):
                    if self.in_main_block:
                        raise SyntaxError("Nested 'MAIN' blocks are not allowed.")
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
                raise SyntaxError("Commands must be inside a 'MAIN' block.")

            # ✅ 일반 명령어 추가
            parsed_commands.append({"cmd": cmd, "args": args})
            i += 1  

        if self.in_main_block:
            raise SyntaxError("Missing 'END_MAIN' at the end of the script.")

        return parsed_commands

    def parse_block(self, processed_lines, start_index, end_keyword):
        """재귀적으로 블록을 파싱하는 함수"""
        block_body = []
        i = start_index

        while i < len(processed_lines):
            line = processed_lines[i].strip().upper()

            if line == end_keyword:
                return block_body, i  # ✅ END 키워드를 만나면 종료

            tokens = self.tokenize(processed_lines[i])
            if not tokens:
                i += 1
                continue

            cmd = tokens[0].upper()
            args = tokens[1:]

            # ✅ 중첩된 블록 처리 (IF, WHILE, FOR)
            if cmd in ["IF", "WHILE", "FOR"]:
                end_mapping = {"IF": "END_IF", "WHILE": "END_WHILE", "FOR": "END_FOR"}
                nested_block, new_index = self.parse_block(processed_lines, i + 1, end_mapping[cmd])
                block_body.append({"cmd": f"{cmd}_BLOCK", "body": [{"cmd": cmd, "args": args}] + nested_block})
                i = new_index + 1
                continue

            # ✅ 일반 명령어 추가
            block_body.append({"cmd": cmd, "args": args})
            i += 1

        raise SyntaxError(f"{end_keyword}가 없습니다.")  # ✅ 종료 키워드가 없으면 오류 발생
   

    def parse_function(self, processed_lines, start_index):
        """FUNCTION 블록을 파싱하는 함수"""
        func_def_lines = [processed_lines[start_index]]
        i = start_index + 1

        while i < len(processed_lines) and processed_lines[i].strip().upper() != "END_FUNCTION":
            func_def_lines.append(processed_lines[i])
            i += 1

        if i >= len(processed_lines) or processed_lines[i].strip().upper() != "END_FUNCTION":
            raise SyntaxError("함수 정의에서 END_FUNCTION이 누락되었습니다.")
        i += 1  # ✅ END_FUNCTION 스킵

        # ✅ 함수 헤더 파싱
        header_tokens = self.tokenize(func_def_lines[0].strip())
        if len(header_tokens) < 2:
            raise SyntaxError("함수 정의 헤더가 올바르지 않습니다.")

        func_name = header_tokens[1]
        params = []
        
        if len(header_tokens) > 2 and header_tokens[2] == "(":
            param_str = " ".join(header_tokens[3:]).rstrip(")")
            params = [p.strip() for p in param_str.split(",")]
        elif len(header_tokens) > 2:
            params = header_tokens[2:]

        func_body = "\n".join(func_def_lines[1:])
        
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