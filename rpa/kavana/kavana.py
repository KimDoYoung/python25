import sys
from lib.core.command_parser import CommandParser
from lib.core.command_executor import CommandExecutor
from lib.core.command_preprocessor import CommandPreprocessor
from lib.core.commands.raise_command import RaiseCommand
from lib.core.datatypes.kavana_datatype import String
from lib.core.exceptions.kavana_exception import KavanaException
from lib.core.function_registry import FunctionRegistry
from lib.core.reserved_words import ReservedWords
from lib.core.token import StringToken, Token
from lib.core.token_type import TokenType
from lib.utils.check import syntax_check
from lib.utils.pretty import format_pretty


VERSION = "0.0.1"  # ✅ 버전 정보
def main():
    if len(sys.argv) < 2:
        print("Usage: python kavana.py <script.kvs> [--check] [--pretty] [--version]")
        sys.exit(1)

    script_path = sys.argv[1]
    check_syntax_only = "--check" in sys.argv  # ✅ --check 옵션 확인
    pretty_format = "--pretty" in sys.argv  # ✅ --pretty 옵션 확인
    version = "--version" in sys.argv  # ✅ --version 옵션 확인
    if version:
        print(f"Kavana Scripting Engine ver: {VERSION}")
        sys.exit(0)
    try:

        with open(script_path, "r", encoding="utf-8") as file:
            script_lines = file.readlines()

        # ✅ 1️⃣ Syntax 체크 단계
        ppLines = CommandPreprocessor().preprocess(script_lines)
        parser = CommandParser(ppLines)
        parsed_commands = []
        if pretty_format:
           for ppLine in ppLines:
                parsed_commands.append(parser.tokenize(ppLine=ppLine))
        else:
           parsed_commands = parser.parse()


        # ✅ --pretty 옵션이 있으면 예쁘게 포맷팅 후 출력하고 종료
        if pretty_format:
            pretty_script = format_pretty(parsed_commands, ReservedWords.get_all_reserved())
            print(pretty_script)
            sys.exit(0)

        # ✅ --check 옵션이 있으면 실행하지 않고 종료
        if check_syntax_only:
            check_result = syntax_check(parsed_commands, ReservedWords.get_all_reserved())
            if check_result:
                print("OK")
            else:
                print("Syntax Error")
            sys.exit(0)

        # ✅ 2️⃣ 실행 단계 (Syntax가 통과된 경우에만 실행)
        executor = CommandExecutor()
        for command in parsed_commands:
            executor.execute(command)

    except KavanaException as e:
        raise_command = RaiseCommand()
        raise_command.execute(
            [StringToken(data=String(str(e)), type=TokenType.STRING)], executor
        )        
        sys.exit(1)
    except Exception as e:
        print(f"❌ Runtime Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
