import sys
from lib.core.command_parser import CommandParser
from lib.core.command_executor import CommandExecutor
from lib.core.function_registry import FunctionRegistry
from lib.utils.pretty import format_pretty

# TODO
# 1. Custom functions
# 2. --check, --pretty 옵션 추가
# 3. IF, FOR, WHILE, BREAK, CONTINUE 지원
# 4. Custom types: Point, Region, Image, Application, Window
# 5. RPA 명령어 지원: Click, KeyIn, Move, Wait_For_Image, Create_Image, Sleep, Capture_Screen, 
#    Run_Application, Close_Application, Get_Window, Get_Window_List, Get_Window_Info


def main():
    if len(sys.argv) < 2:
        print("Usage: python kavana.py <script.kvs> [--check] [--pretty]")
        sys.exit(1)

    script_path = sys.argv[1]
    check_syntax_only = "--check" in sys.argv  # ✅ --check 옵션 확인
    pretty_format = "--pretty" in sys.argv  # ✅ --pretty 옵션 확인

    try:
        with open(script_path, "r", encoding="utf-8") as file:
            script_lines = file.readlines()

        # ✅ 1️⃣ Syntax 체크 단계
        parser = CommandParser(script_lines)
        parsed_commands = parser.parse()

        print("✅ Syntax Check Passed!")  # Syntax 체크 성공 메시지 출력

        # ✅ --pretty 옵션이 있으면 예쁘게 포맷팅 후 출력하고 종료
        if pretty_format:
            pretty_script = format_pretty(parsed_commands)
            print("\n📌 Pretty Formatted Script:\n")
            print(pretty_script)
            sys.exit(0)

        # ✅ --check 옵션이 있으면 실행하지 않고 종료
        if check_syntax_only:
            sys.exit(0)

        # ✅ 2️⃣ 실행 단계 (Syntax가 통과된 경우에만 실행)
        FunctionRegistry.print_user_functions()
        executor = CommandExecutor()
        for command in parsed_commands:
            executor.execute(command)

    except FileNotFoundError:
        print(f"❌ Error: File '{script_path}' not found.")
        sys.exit(1)
    except SyntaxError as e:
        print(f"❌ Syntax Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Runtime Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
