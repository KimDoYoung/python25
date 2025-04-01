from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    DB connect path="test1.db" 
    db execute sql=\"\"\"
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        done INTEGER DEFAULT 0
    )
    \"\"\"    
    DB execute sql="insert into tasks (title) values ('task1')"
    DB execute sql="insert into tasks (title) values ('task2')"
    DB execute sql="insert into tasks (title) values ('task3')"
    DB query sql="select * from tasks order by id desc", to_var="tasks"
    PRINT "길이:", Length(tasks)
    PRINT tasks[0] 
    DB query sql="select count(*) as count from tasks", to_var="result"
    PRINT  result[0]["count"]
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
    print("----------------------")
    commandExecutor.execute(command)
