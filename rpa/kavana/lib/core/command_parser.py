import re

class CommandParser:
    """
    Kavana 스크립트의 명령어를 분석하는 파서.
    `main ... end_main` 블록 안에서만 실행 가능하며, 명령어와 인자를 분리한다.
    """
    def __init__(self, script_lines):
        self.script_lines = script_lines
        self.in_main_block = False

    def preprocess_lines(self):
        """멀티라인(`\`) 연결 및 주석(`//`) 제거"""
        merged_lines = []
        current_line = ""

        for line in self.script_lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("//"):
                continue  # 빈 줄 및 주석 제거

            if stripped.endswith("\\"):
                current_line += stripped[:-1] + " "  # `\` 제거 후 다음 줄 연결
            else:
                current_line += stripped
                merged_lines.append(current_line)
                current_line = ""  # 새로운 줄 시작

        return merged_lines

    def parse(self):
        """
        스크립트의 모든 명령어를 분석하여 리스트로 반환.
        - `PRINT("hello")` → `{"cmd": "PRINT", "args": ["hello"]}`
        - `SET a = 10` → `{"cmd": "SET", "args": ["a", "=", "10"]}`
        """
        parsed_commands = []
        processed_lines = self.preprocess_lines()

        for line in processed_lines:
            tokens = self.tokenize(line)
            if not tokens:
                continue

            cmd_original = tokens[0]  # 원본 명령어 유지
            cmd = cmd_original.upper()  # 명령어만 대문자로 변환
            args = tokens[1:]

            if cmd == "MAIN":
                if self.in_main_block:
                    raise SyntaxError("Nested 'MAIN' blocks are not allowed.")
                self.in_main_block = True
                continue  # `MAIN` 자체는 저장하지 않음

            elif cmd == "END_MAIN":
                if not self.in_main_block:
                    raise SyntaxError("'END_MAIN' found without 'MAIN'.")
                self.in_main_block = False
                break  # `END_MAIN` 이후 명령어는 무시

            elif not self.in_main_block:
                raise SyntaxError("Commands must be inside a 'MAIN' block.")

            # PRINT("hello") 같은 경우 처리
            if "(" in cmd_original and cmd_original.endswith(")"):
                func_match = re.match(r'(\w+)\((.*)\)', cmd_original)
                if func_match:
                    cmd = func_match.group(1).upper()  # 명령어만 대문자로 변환
                    args = [func_match.group(2)]  # 괄호 안의 내용만 추출 (원본 유지)

            parsed_commands.append({"cmd": cmd, "args": args})

        if self.in_main_block:
            raise SyntaxError("Missing 'END_MAIN' at the end of the script.")

        return parsed_commands

    @staticmethod
    def tokenize(line: str):
        """명령어를 토큰 리스트로 변환"""
        return re.findall(r'".*?"|\S+', line)  # 문자열 유지하면서 공백 기준 분리
