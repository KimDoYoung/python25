import re
import os

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

        for line in processed_lines:
            tokens = self.tokenize(line)
            if not tokens:
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

            if cmd == "INCLUDE":
                if not args:
                    raise SyntaxError("INCLUDE 문에 파일 경로가 필요합니다.")
                include_path = args[0].strip('"')  # 따옴표 제거
                self._process_include(include_path, parsed_commands)
                continue

            if cmd == "LOAD":
                if not args:
                    raise SyntaxError("LOAD 문에 .env 파일 경로가 필요합니다.")
                env_path = args[0].strip('"')  # 따옴표 제거
                self._process_env(env_path, parsed_commands)
                continue

            if cmd == "MAIN":
                if not getattr(self, "ignore_main_check", False):  # ✅ MAIN 검사 무시 여부 확인
                    if self.in_main_block:
                        raise SyntaxError("Nested 'MAIN' blocks are not allowed.")
                    self.in_main_block = True
                continue  # `MAIN` 자체는 저장하지 않음

            elif cmd == "END_MAIN":
                if not getattr(self, "ignore_main_check", False):  # ✅ MAIN 검사 무시 여부 확인
                    if not self.in_main_block and not getattr(self, "ignore_main_check", False): 
                        raise SyntaxError("'END_MAIN' found without 'MAIN'.")
                    self.in_main_block = False
                break  # `END_MAIN` 이후 명령어는 무시

            elif not self.in_main_block and not getattr(self, "ignore_main_check", False): 
                raise SyntaxError("Commands must be inside a 'MAIN' block.")

            parsed_commands.append({"cmd": cmd, "args": args})

        if self.in_main_block:
            raise SyntaxError("Missing 'END_MAIN' at the end of the script.")

        return parsed_commands

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
    def tokenize(line: str):
        """
        명령어를 토큰 리스트로 변환
        - PRINT Hello → ["PRINT", "Hello"]
        - PRINT "Hello World" → ["PRINT", '"Hello World"']
        - PRINT("hello {name}") → ["PRINT", '"hello {name}"']
        - PRINT("hello", "world") → ["PRINT", '"hello"', '"world"']
        """
        # ✅ PRINT(...) 함수형 명령어 처리
        func_match = re.match(r'^(\w+)\((.*)\)$', line)
        if func_match:
            cmd = func_match.group(1).upper()
            args = func_match.group(2).strip()
            split_args = re.findall(r'".*?"|\w+', args)  # ✅ 쉼표 제거
            return [cmd] + split_args

        # ✅ 일반 명령어 처리
        tokens = re.findall(r'".*?"|\S+', line)
        return tokens