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
    
    APP_OPEN from_var="esafe", maximize=False, process_name=process_name
    
    SET number = 1
    WAIT (5+(2*2)+ number)
    WAIT until image_path=image_base_path + "\\login_button.png"
    if _LastError_ == ""
        LOG_INFO "로그인 버튼을 찾았습니다."
    else
        LOG_ERROR "로그인 버튼을 찾지 못했습니다"
    end_if
    WAIT 10
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
