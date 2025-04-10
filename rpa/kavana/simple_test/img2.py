from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    SET base_dir = "C:/Users/PC/Pictures/"
    //SET base_dir = "C:/Users/KOREA/Pictures/"
    SET img1 = Image(base_dir + "1.png")
    //IMAGE save from_var="img1" to_file=f"{base_dir}/2.png"
    //IMAGE resize from_var="img1" to_var="img2" width=400
    //IMAGE save from_var="img2" to_file=f"{base_dir}/3.png"
    //IMAGE resize from_var="img1" to_var="img2" factor=0.5
    IMAGE clip region=Region(0, 0, 100, 100) from_file=f"{base_dir}/1.png" to_file=f"{base_dir}/4.png"
    IMAGE to_gray from_file=f"{base_dir}/1.png" to_file=f"{base_dir}/5.png"
    IMAGE convert_to mode="1" from_file=f"{base_dir}/1.png" to_file=f"{base_dir}/6.png"
    IMAGE rotate angle=90 from_file=f"{base_dir}/1.png" to_file=f"{base_dir}/7.png"
    IMAGE blur from_file=f"{base_dir}/1.png" to_file=f"{base_dir}/8.png" radius=5 
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
