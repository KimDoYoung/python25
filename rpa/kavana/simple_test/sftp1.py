from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
ENV_LOAD ".env"
MAIN
    // sftp info
    set sftp_info = {
        "host": $SFTP_HOST,
        "port": $SFTP_PORT,
        "user": $SFTP_USER,
        "password": $SFTP_PASSWORD,
    }
    set remote_dir  = "/home/kdy987/data"
    set local_dir   = r"c:\\tmp"
    print sftp_info
    SFTP upload with=sftp_info  remote_dir=remote_dir local_dir=local_dir files=["T3600*.jpg"]
    SFTP download with=sftp_info  remote_dir=remote_dir local_dir=local_dir+"/logs" files=["T3600*.jpg"]
    //SFTP list with=sftp_info  remote_dir=remote_dir pattern="*.jpg" to_var="sftp_list"
    //print sftp_list
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
