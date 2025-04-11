from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    BROWSER OPEN url="https://haruta.co.kr/product/list.html?cate_no=52"
    //BROWSER WAIT seconds=5
    BROWSER WAIT select=".prdList" select_by="css" until="present", timeout=10
    BROWSER EXTRACT select=".thumb" select_by="css" within=".prdList" attr="src" to_var="image_urls"
    print image_urls
    //BROWSER CLICK selector="" selector_type="css"
    //BROWSER TYPE selector="#input" text="Hello, World!"
    //BROWSER WAIT seconds=5
    //BROWSER GET_TEXT selector="#output" to_var="output_text"
    //PRINT output_text
    //BROWSER CAPTURE filename="screenshot.png"
    BROWSER CLOSE
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
