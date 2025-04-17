from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
function login(image_base_path)
    SET login_file = f"{image_base_path}\\로그인.png"
    RPA WAIT seconds = 5
    RPA wait_image from_file=login_file after="click"
    //사용자이름 click
    RPA wait seconds=3
    RPA click_point location=Point(1627,1020), after="wait:1s"  //1627, 1020
    //RPA WAIT seconds=1
    SET point_password_input = Point(2028,1333) //2028, 1333
    RPA click_point location=point_password_input, after="wait:1s"
    RPA put_text text="kfund8100*"
    RPA click_point x=2141, y=1421 //2141, 1421
    //RPA wait_image_and_click from_file=cert_name, area= Region(1529, 937, 465, 179)
    RPA WAIT seconds=10
    RPA click_point x=1807, y=1004  //1807, 1004 업무자격
    RPA click_point x=1978, y=1104 , duration=0.8

end_function
function go_mouse_origin()
    RPA mouse_move x=1978, y= 1, duration=0.5, after="wait:1s"
end_function
function do_500068(image_base_path)
    SET save_folder = r"c:\\tmp"
    SET number_input = Point(3705, 56) 
    SET fundall_checkbox = Point(2044,172)
    SET query_btn = Point(3646,352)
    SET file_download_combo = Point(448, 1896)
    SET save_as_input = Point(757, 780)


    //번호 넣고 enger
    RPA CLICK_POINT location=number_input after="wait:1s"
    RPA PUT_TEXT text="500068"  
    RPA KEY_IN keys=["enter"] after="wait:10s"

    //펀드전체checkbox 클릭
    RPA CLICK_POINT location=fundall_checkbox after="wait:2s"

    //조회버튼 클릭
    RPA CLICK_POINT location=query_btn after="wait:10s"
    just go_mouse_origin()
    set query_complete_image = f"{image_base_path}\\조회완료.png"
    LOG_INFO "조회완료 이미지 대기...."
    RPA WAIT_IMAGE from_file=query_complete_image, after="wait:10s", grayscale=True, confidence=0.8, area=Region(277, 71, 294, 51), timeout=(60*10)
    RPA CAPTURE to_file=f"{image_base_path}\\500068_{YMD()}.png"

    //파일다운로드 콤보박스 클릭
    RPA CLICK_POINT location=file_download_combo after="wait:1s"  
    RPA KEY_IN keys=["down", "down", "enter"] after="wait:3s"
    
    //다른 이름 저장
    RPA click_point location=save_as_input, after="wait:1s"
    RPA key_in keys=["ctrl+a", "delete"]
    SET ymd = YMD()
    SET save_file_name = f"{save_folder}\\{ymd}_500068.csv"
    if file_exists(save_file_name) == True
        just file_delete(save_file_name)
        print f"기존 파일 삭제 {save_file_name}"
    else
        print f"기존 파일 없음 {save_file_name}"
    end_if
    RPA put_text text=save_file_name
    rpa key_in keys=["enter"] after="wait:10s"
    rpa key_in keys=["space","space"] after="wait:3s"
    just close_all_tabs(image_base_path)
end_function

function close_all_tabs(image_base_path)
    set tab_area = Region(392, 79, 857, 30) //탭영역
    set count = 1
    while True
        RPA find_image to_var="found_point" area=tab_area, from_file=f"{image_base_path}\\탭닫기.png", grayscale=True, confidence=0.8
        if found_point != None
            //LOG_INFO f"탭닫기 이미지 발견 {found_point}"
            RPA CLICK_POINT location=found_point, after="wait:1s"
        else
            LOG_INFO "탭닫기 이미지 발견 못함"
            RPA WAIT seconds=1
            break
        end_if
        set count = count + 1
        if count > 10
            break
        end_if
    end_while
end_function

MAIN
    LOG_INFO "=========================================================="
    LOG_INFO "KSD SAFE 프로그램 시작"
    LOG_INFO "=========================================================="

    // 애플리케이션 실행
    SET esafe_path = "C:\\Users\\PC\\AppData\\Roaming\\KSD SAFE\\LauncherKSD\\eSAFE2019.exe"
    SET process_name = "KSD.ApplicationBrowser.Shell.exe"
    SET image_base_path = "C:\\Users\\PC\\Pictures\\SophiaCapture\\esafe"
    SET esafe = Application(esafe_path)
    
    // 이름 이미지 저장
    SET cert_name = f"{image_base_path}\\cert_name.png"
    IMAGE create_text_image text="한국펀드" to_file=cert_name

    RPA APP_OPEN from_var="esafe", maximize=False, process_name=process_name

    LOG_INFO "-------로그인 시작"
    JUST login(image_base_path)
    LOG_INFO "------로그인 완료"
    
    rpa mouse_move x=1978, y= 1, duration=0.5
    //RPA WAIT seconds=15
    set refresh_image = f"{image_base_path}\\새로고침.png"
    RPA WAIT_IMAGE from_file=refresh_image, after="wait:10s", grayscale=True, confidence=0.8, area=Region(275, 74, 287, 255), timeout=(60*5)
    
    RPA CAPTURE to_file=f"{image_base_path}\\esafe.png"

    LOG_INFO "==========================500068 =>"
    JUST do_500068(image_base_path)
    LOG_INFO "<==========================500068"

    RPA KEY_IN keys=["alt+F4"], after="wait:1s"

    LOG_INFO "=========================================================="
    LOG_INFO ">>> KSD SAFE 종료"
    LOG_INFO "=========================================================="
    
    ON_EXCEPTION
        RPA app_close from_var="esafe" 
        PRINT "예외 발생"
        LOG_ERROR f">>> {$exception_message} exit code: {$exit_code}"
    END_EXCEPTION
END_MAIN
"""
#---------------------------
# 기본적인 사용
#---------------------------
script_lines = script.split("\n")
command_preprocssed_lines = CommandPreprocessor().preprocess(script_lines)
# for line in command_preprocssed_lines:
#     print(line)
parser = CommandParser()
parsed_commands = parser.parse(command_preprocssed_lines)

commandExecutor = CommandExecutor()

for command in parsed_commands:
    print("----------------------")
    print(command)
    commandExecutor.execute(command)
    print("----------------------")
