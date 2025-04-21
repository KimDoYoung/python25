from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    //------------------------------------------
    // 기본 데이터 타입
    //------------------------------------------
    SET i = 10
    SET f = 12.34
    SET s = "Hello"
    SET b = not True
    SET n = None
    SET array1 = ["Hello", "Kavana", "!"] // 요소는 같은 데이터 타입이어야 함
    SET array2 = [ // 2중배열까지만 가능
        [1,2,3],
        [4,5,6],
        [7,8,9]
    ]
    SET map1 = {
        "name": "Kavana",
        "age": 10,
        "isAlive": True,
        "address": {
            "city": "Seoul",
            "country": "Korea"
        }
    }
    PRINT type_of(i), type_of(f), type_of(s), type_of(b), type_of(n), type_of(array1), type_of(array2), type_of(map1)
    //------------------------------------------
    // 날짜 및 시간 데이터 타입
    //------------------------------------------
    SET ymd = Ymd(2025, 4, 21)
    SET ymdtime = YmdTime(2025, 4, 21, 12, 34, 56)
    //------------------------------------------
    // RPA용 데이터 타입
    //------------------------------------------
    SET pt = Point(10,20)
    SET rect = Rectangle(10,20,30,40)
    SET reg = Region(1,1,30,40)
    SET app = Application("notepad.exe")
    SET win = Window("제목없음")
    SET img = Image(r"c:\\tmp\\1.png")
    PRINT type_of(pt), type_of(rect), type_of(reg), type_of(app), type_of(win), type_of(img) 
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
