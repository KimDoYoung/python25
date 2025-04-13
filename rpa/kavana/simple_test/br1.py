from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    BROWSER OPEN url="https://haruta.co.kr/product/list.html?cate_no=52"
    BROWSER WAIT seconds=5
    BROWSER WAIT select=".prdList" select_by="css" until="present", timeout=10
    BROWSER EXTRACT select=".thumb" select_by="css" within=".prdList" attr="src" to_var="image_urls"
    print image_urls
    BROWSER click select=".buy-btn" within=".product" select_by="css" scroll_first=True click_js=False


    BROWSER PUT_TEXT select="#input" within=".product" select_by="css" text="Hello, World!" 
    BROWSER WAIT seconds=5
    BROWSER GET_TEXT select="#input" within=".product" select_by="css" scroll_first=True to_var="output_text"
    PRINT output_text
    BROWSER CAPTURE to_file="screenshot.png"
    BROWSER EXECUTE_JS script="alert('Hello, World!')"
    BROWSER switch_iframe select="iframe" select_by="css" within=".product"
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
