import sys
from lib.core.command_parser import CommandParser
from lib.core.command_executor import CommandExecutor

def main():
    if len(sys.argv) != 2:
        print("Usage: python kavana.py <script.kvs>")
        sys.exit(1)

    script_path = sys.argv[1]

    try:
        with open(script_path, "r", encoding="utf-8") as file:
            script_lines = file.readlines()

        # 명령어 분석 (구문 파싱)
        parser = CommandParser(script_lines)
        parsed_commands = parser.parse()

        # 명령어 실행
        executor = CommandExecutor()
        for command in parsed_commands:
            executor.execute(command)

    except FileNotFoundError:
        print(f"Error: File '{script_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
