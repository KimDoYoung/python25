from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    SET i = 1 // 정수형
    SET f = 12.34 // 실수형
    SET s = "Hello" // 문자열형
    SET b = not True // 불리언형
    
    PRINT f"i={i} f={f} s={s} b={b}" 

    SET array1 = [1, 2, 3] // 배열형
    SET array2 = [
        [1, 2, 3], 
        [4, 5, 6],
        [7, 8, 9]
    ]  
    SET dict1 = {
        "key1": 1,
        "key2": 2,
        "key3": 3
    } 
    SET dict2 = {
        "key1": [1, 2, 3],
        "key2": [4, 5, 6],
        "key3": [7, 8, 9]
    } 
    PRINT array1[1] // 2
    PRINT array2[1][2] // 6
    PRINT dict1["key2"] // 2
    PRINT dict2["key3"][1] // 8
END_MAIN
"""
#---------------------------
# 기본적인 사용
#---------------------------
script_lines = script.split("\n")
command_preprocssed_lines = CommandPreprocessor().preprocess(script_lines)
parser = CommandParser()
parsed_commands = parser.parse(command_preprocssed_lines)

commandExecutor = CommandExecutor()

for command in parsed_commands:
    commandExecutor.execute(command)
