import re
from lib.core.reserved_words import ReservedWords

class CommandParser:
    """
    Kavana 스크립트의 명령어를 분석하여 명령어 타입과 인자를 분리하는 파서.
    실행은 담당하지 않고, 단순 구문 분석 역할만 수행.
    """

    def __init__(self, script_line: str):
        self.script_line = script_line.strip()

    def parse(self):
        """
        주어진 명령어를 분석하여 {cmd: 명령어, args: 인자 리스트} 형태로 반환.
        """
        if not self.script_line or self.script_line.startswith("//"):  # 빈 줄 또는 주석
            return None

        tokens = self.tokenize(self.script_line)
        if not tokens:
            return None

        cmd = tokens[0].upper()
        args = tokens[1:]

        if ReservedWords.is_reserved(cmd):
            return {"cmd": cmd, "args": args}
        else:
            raise ValueError(f"Invalid command: {cmd}")

    @staticmethod
    def tokenize(line: str):
        """
        명령어를 토큰 리스트로 변환.
        """
        return re.findall(r'".*?"|\S+', line)  # 공백 기준 분리, 문자열 유지

# 테스트 코드
if __name__ == "__main__":
    test_commands = [
        'SET a = 10',
        'PRINT "Hello, World!"',
        'IF a == 10',
        'GOTO label1',
        '// This is a comment',
        '   ',  # 빈 줄
    ]

    for cmd in test_commands:
        parser = CommandParser(cmd)
        try:
            result = parser.parse()
            print(f"Input: {cmd} → Parsed: {result}")
        except ValueError as e:
            print(f"Error parsing '{cmd}': {e}")
