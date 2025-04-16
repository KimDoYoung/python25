from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
function login(image_base_path)
    SET login_file = f"{image_base_path}\\로그인.png"
    RPA WAIT seconds = 5
    RPA wait_image_and_click from_file=login_file

    RPA WAIT seconds=5
    RPA click_point x=1627, y=1020  //1627, 1020
    RPA WAIT seconds=1
    RPA click_point x=2028, y=1333  //2028, 1333
    RPA put_text text="kfund8100*"
    RPA click_point x=2141, y=1421 //2141, 1421
    //RPA wait_image_and_click from_file=cert_name, area= Region(1529, 937, 465, 179)
    RPA WAIT seconds=10
    RPA click_point x=1807, y=1004  //1807, 1004 업무자격
    RPA click_point x=1978, y=1104 , duration=0.8

end_function
MAIN
    // 애플리케이션 실행
    SET esafe_path = "C:\\Users\\PC\\AppData\\Roaming\\KSD SAFE\\LauncherKSD\\eSAFE2019.exe"
    SET process_name = "KSD.ApplicationBrowser.Shell.exe"
    SET image_base_path = "C:\\Users\\PC\\Pictures\\SophiaCapture\\esafe"
    SET esafe = Application(esafe_path)
    
    // 이름 이미지 저장
    SET cert_name = f"{image_base_path}\\cert_name.png"
    IMAGE create_text_image text="한국펀드" to_file=cert_name

    

    RPA APP_OPEN from_var="esafe", maximize=False, process_name=process_name

    JUST login(image_base_path)
    
    RPA MOUSE_MOVE x=1978, y=1
    RPA WAIT seconds=10

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
