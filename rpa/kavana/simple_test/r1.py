from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    // 애플리케이션 실행
    SET esafe_path = "C:\\Users\\PC\\AppData\\Roaming\\KSD SAFE\\LauncherKSD\\eSAFE2019.exe"
    SET process_name = "KSD.ApplicationBrowser.Shell.exe"
    SET image_base_path = "C:\\Users\\PC\\Pictures\\SophiaCapture\\esafe"
    SET esafe = Application(esafe_path)
    
    RPA APP_OPEN from_var="esafe", maximize=False, process_name=process_name
    RPA WAIT seconds = 5
    RPA app_close from_var="esafe" 
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
