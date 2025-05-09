from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor, PreprocessedLine
from lib.core.token_type import TokenType
from PIL import Image, ImageDraw, ImageFont
import tempfile


def get_tokens(s:str):
    s = "SET i = " +s
    s = "MAIN\n" + s + "\nEND_MAIN"
    lines = [s.strip() for s in s.split("\n") if s.strip()]
    command_preprocssed_lines = CommandPreprocessor().preprocess(lines)
    parsed_commands = CommandParser().parse(command_preprocssed_lines)
    tokens = parsed_commands[0]["args"]
    # token.type = TokenType.ASSIGN을 찾아서 그 다음 번호를 반환
    start_idx = 0
    for i, token in enumerate(tokens):
        if token.type == TokenType.ASSIGN:
            start_idx = i +1
            break
    return tokens,start_idx

def get_command(s:str):
    s = "MAIN\n" + s + "\nEND_MAIN"
    lines = [s.strip() for s in s.split("\n") if s.strip()]
    command_preprocssed_lines = CommandPreprocessor().preprocess(lines)
    parsed_commands = CommandParser().parse(command_preprocssed_lines)
    return parsed_commands
    # tokens = parsed_commands[0]["args"]
    # return tokens

def get_raw_tokens(s):
    ''' get_raw_tokens('{1:2}')와 같이 호출, tokens를 반환 '''
    ppLine = PreprocessedLine(s, 1, 1)
    return CommandParser().pre_process_tokens(ppLine)

def create_test_image() -> str:
    """ PILImage로 이미지 생성,path를 리턴"""
        # 1. 흰색 배경의 400x200 이미지 생성
    img = Image.new('RGB', (400, 200), color='white')

    # 2. 이미지에 그리기 위한 객체 생성
    draw = ImageDraw.Draw(img)

    # 3. 텍스트 작성 (기본 폰트 사용)
    text = "Hello, 이미지 생성!"
    draw.text((50, 80), text, fill='black')

    # 4. 빨간색 사각형 그리기
    draw.rectangle([30, 30, 100, 100], outline='red', width=3)

    # 5. 이미지 저장
    # 임시 파일 생성``
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    temp_file_path = temp_file.name
    temp_file.close()
    img.save(temp_file_path)
    return temp_file_path