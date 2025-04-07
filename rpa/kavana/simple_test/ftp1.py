from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
ENV_LOAD ".env"
MAIN
    // ftp info
    set ftp_info = {
        "host": "jskn.ipdisk.co.kr",
        "port": 21,
        "user": $FTP_USER,
        "password": $FTP_PASSWORD,
    }
    print ftp_info
    FTP upload with=ftp_info  remote_dir="/HDD1/test1" local_dir=r"c:\\tmp" files=["1.txt", "2.txt"]
    FTP download with=ftp_info  remote_dir="/HDD1/test1"  local_dir=r"c:\\tmp" files=["*.txt"]
    FTP list with=ftp_info  remote_dir="/HDD1/test1" pattern="*.txt" to_var="ftp_list"
    for item in ftp_list
        print item
    end_for
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
