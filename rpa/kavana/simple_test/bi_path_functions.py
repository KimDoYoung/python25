from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    //set path = PATH_JOIN("C:\\", "Users", "user", "Documents")
    set path = r"c:\\Users\\user\\Documents\\file.txt"
    set basename = PATH_BASENAME(path)
    set dirname = PATH_DIRNAME(path)
    print "Path: ", path
    print "Basename: ", basename
    print "Dirname: ", dirname
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
