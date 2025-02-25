import sys
from lib.core.command_parser import CommandParser
from lib.core.command_executor import CommandExecutor
from lib.core.function_registry import FunctionRegistry

#TODO
# 1. custom functions
# 2. --check, --pretty 옵션
# 3. IF,FOR, WHILE, BREAK, CONTINUE
# 4. custom type : Point, Region, Image, Application, Window
# 5. RPA 명령어들 :   Click, KeyIn, Move, Wait_For_Image, Create_Image, Sleep, Capture_Scrren, 
# Run_Application, Close_Application, Get_Window, Get_Window_List, Get_Window_Info


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
        
        # for command in parsed_commands:
        #     print(command)
        # exit(0)
        FunctionRegistry.print_user_functions()
        
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


