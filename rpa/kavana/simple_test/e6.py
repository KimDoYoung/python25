from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# HashMap
script = """
MAIN
    SET map4 = {
        "a": [1,2,3],
        "b": [4,5,6],
        "c": "홍길동"
    }
    print map4["c"]
    SET info = {
        "hwnd": 123456,
        "title": "유의사항",
        "class": "MDIClient"}
    SET allow_titles = ["유의사항", "안내"]
    SET title = TRIM(info["title"])
    print f"'{title}' 팝업입니다."
    if CONTAINS(allow_titles, title)    
    
            print f"'{title}' 팝업입니다."
        else
            print f"'{title}' 팝업이 아닙니다."
        end_if
END_MAIN
"""
#---------------------------
# 기본적인 사용
#---------------------------
script_lines = script.split("\n")
command_preprocssed_lines = CommandPreprocessor().preprocess(script_lines)
parsed_commands = CommandParser().parse(command_preprocssed_lines)
commandExecutor = CommandExecutor()
for command in parsed_commands:
    # print("----------------------")
    # print(command)
    commandExecutor.execute(command)
    # print("----------------------")
