from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# EXIT, ON_EXCEPTION, RAISE
script = """
MAIN
    SET a = SUBSTR("abcde", 1+ LENGTH("K"), 1+3=1)
    print a
    SET b = LENGTH(["1", "2", "3"])
    print b
END_MAIN

"""
#---------------------------
# 기본적인 사용
#---------------------------
script_lines = script.split("\n")
command_preprocssed_lines = CommandPreprocessor().preprocess(script_lines)
parsed_commands = CommandParser().parse(command_preprocssed_lines)
commandExecutor = CommandExecutor()
try:
    for command in parsed_commands:
        commandExecutor.execute(command)
except Exception as e:
    print(f"예외 발생: {e}")
