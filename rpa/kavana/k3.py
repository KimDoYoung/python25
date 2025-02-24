from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.function_registry import FunctionRegistry


script_lines = [
    "function plus(a, b)",
    "SET result = a + b",
    "RETURN result",
    "end_function",
    "main",
    "SET a = plus(1,2) + 1",
    "set b = substr(\"12345\",1,2)",
    "end_main"
];

parser = CommandParser(script_lines)
parsed_commands = parser.parse()

for command in parsed_commands:
    print(command)
# exit(0)
FunctionRegistry.print_user_functions()

# 명령어 실행
executor = CommandExecutor()
for command in parsed_commands:
    executor.execute(command)