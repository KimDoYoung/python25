from lib.core.command_executor import CommandExecutor
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor

# 대입
script = """
MAIN
    SET content = \"\"\"
나는 반딧불

나는 내가 빛나는 별인줄 알았어요
한번도 의삼한 적 없었죠

몰랐어요. 난 내가 벌레라는 것을
그래도 괜찮아 난 눈부시니까

하늘에서 떨어진 별인 줄 알았어요
소원을 들어주는 작은 별

몰랐어요. 난 내가 개똥벌레라는 것을
그래도 괜찮아 나는 빛날테니까
    \"\"\"
    SET file_path = FILE_TEMP_NAME(".txt")
    JUST File_WRITE(file_path, content)
    PRINT f"파일에 쓰기 완료 : {file_path}"
    SET exists = File_EXISTS(file_path)
    IF exists
        PRINT f"{file_path} 파일이 존재합니다."
    ELSE
        PRINT f"{file_path} 파일이 존재하지 않습니다." 
    END_IF
    JUST File_APPEND(file_path, "---->전국민 위로송")
    SET read_content = File_READ(file_path)
    PRINT read_content
    PRINT "---------------------------------------"
    SET lines = File_LINES(file_path)
    SET line_count = LENGTH(lines)
    SET line_number = 1
    FOR line IN lines:
        PRINT f"{line_number}: {line}"
        SET line_number = line_number + 1
    END_FOR
    PRINT f"총 줄 수: {line_count}"
    PRINT "---------------------------------------"
    SET hash = File_HASH(file_path, "sha256")
    PRINT f"파일 Hash코드: {hash}"
    SET copied = File_COPY(file_path, file_path + ".copy")
    PRINT f"파일 복사 완료: {copied}"
    SET moved = File_MOVE(file_path + ".copy", file_path + ".moved")
    PRINT f"파일 이동 완료: {moved}"
    SET deleted = File_DELETE(file_path + ".moved")
    PRINT f"파일 삭제 완료: {deleted}"
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
