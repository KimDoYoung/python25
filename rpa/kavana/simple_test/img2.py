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
    //print "resized done"
    //IMAGE clip area=Region(0, 0, 100, 100) from_file=f"{base_dir}/1.png" to_file=f"{base_dir}/4.png"
    //print "clipped done"
    //IMAGE to_gray from_file=f"{base_dir}/1.png" to_file=f"{base_dir}/5.png"
    //print "to_gray done"
    //IMAGE convert_to mode="1" from_file=f"{base_dir}/1.png" to_file=f"{base_dir}/6.png"
    //print "convert_to done"
    //IMAGE rotate angle=90 from_file=f"{base_dir}/1.png" to_file=f"{base_dir}/7.png"
    //print "rotate done"
    //IMAGE blur from_file=f"{base_dir}/1.png" to_file=f"{base_dir}/8.png" radius=5.0
    //print "blur done"
    //IMAGE threshold level=128 from_file=f"{base_dir}/1.png" to_file=f"{base_dir}/9.png"
    //print "threshold done"
    SET name = "홍길동"
    Image create_text_image text=name font_size=12 to_file=f"{base_dir}/{name}.png"
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
