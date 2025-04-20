from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    SET list1 = [1,2,3]
    SET map1 = {
        "a":1, "b":2
    }
    SET v1 = list1[0]
    SET v2 = map1["a"]
    print v1, v2
    SET list2 = [
        ["a","b","c"],
        ["d","e","f"]
    ]
    SET map2 = {
        "k1" :{
            "key1": [1,2,3],
            "key2": {
                "key21": "abc"
            }
        }
    }
    SET v3 = list2[0][2-1]
    SET v4 = map2["k1"]["key2"]
    SET v5 = map2["k1"]["key2"]["key21"]
    print v3, v4, v5
    SET map2["k1"]= 100
    print map2

END_MAIN
"""
#---------------------------
# 기본적인 사용
#---------------------------
script_lines = script.split("\n")
command_preprocssed_lines = CommandPreprocessor().preprocess(script_lines)
for line in command_preprocssed_lines:
    print(line)
parser = CommandParser()
parsed_commands = parser.parse(command_preprocssed_lines)

commandExecutor = CommandExecutor()

for command in parsed_commands:
    print("----------------------")
    print(command)
    commandExecutor.execute(command)
    print("----------------------")
