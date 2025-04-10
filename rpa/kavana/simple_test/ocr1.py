from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    SET r1 = Region(6, 26, 60, 21) // 계좌번호
    SET r2 = Region(215, 27, 63, 16) // 비밀번호
    SET r3 = Region(136, 76, 143, 21) // 예수금 금액

    SET base_dir = "C:/Users/PC/Pictures/"
    //SET base_dir = "C:/Users/KOREA/Pictures/"
    SET filename = "efriend1.png"
    SET img1 = Image(base_dir + filename)

    //OCR read from_file=f"{base_dir}{filename}" area=r1 to_var="account" 
    //print f"계좌번호 : {account}"

    //OCR find text="비밀번호" from_file=f"{base_dir}{filename}"  to_var="password_point"
    //print f"비밀번호 : {password_point}"
    SET r4 = Region(285, 78, 133, 199) // 텍스트들

    SET ocr_info = {
        "gray": False,
        "threshold": "none",
        "blur": False,
        "resize": 1.5,
        "invert": False  // 배경 어두운 경우
    }

    OCR get_all with=ocr_info preprocess=True from_file=f"{base_dir}{filename}" area=r4 to_var="texts"
    for text in texts
        print text
    END_FOR
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
