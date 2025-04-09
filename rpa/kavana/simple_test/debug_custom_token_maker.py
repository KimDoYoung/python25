from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor
from lib.core.custom_token_maker import CustomTokenMaker
from lib.core.token_type import TokenType
from lib.core.token import Token
from lib.core.datatypes.kavana_datatype import String



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

def debug_token_image():
    # 예: Image(base_dir + "1.png")

    try:
        tokens, start_idx = get_tokens('WINDOW(base_dir + "1.png")')
        # tokens, start_idx = get_tokens('Window(substr("abcdef",1,2) + ".png")')
        result_token, next_idx = CustomTokenMaker.custom_object_token(tokens, start_idx, TokenType.WINDOW)
        print("✅ ImageToken 생성 완료")
        print(f"  표현식 토큰 수: {len(result_token.expressions[0])}")
        print(f"  표현식 내용: {[t.data.value if t.data else t.type for t in result_token.expressions[0]]}")
        print(f"  다음 토큰 인덱스: {next_idx}")

        tokens, start_idx = get_tokens('POINT(10+2,(3*2)+1)')
        # tokens, start_idx = get_tokens('Window(substr("abcdef",1,2) + ".png")')
        result_token, next_idx = CustomTokenMaker.custom_object_token(tokens, start_idx, TokenType.POINT)
        print("✅ PointToken 생성 완료")
        print(f"  표현식 토큰 수: {len(result_token.expressions[0])}")
        print(f"  표현식 토큰 수: {len(result_token.expressions[1])}")
        print(f"  표현식 내용: {[t.data.value if t.data else t.type for t in result_token.expressions[0]]}")
        print(f"  다음 토큰 인덱스: {next_idx}")

        tokens, start_idx = get_tokens('Rectangle(10+1,20+1,(30+2),(40)+2)')
        # tokens, start_idx = get_tokens('Window(substr("abcdef",1,2) + ".png")')
        result_token, next_idx = CustomTokenMaker.custom_object_token(tokens, start_idx, TokenType.RECTANGLE)
        print("✅ PointToken 생성 완료")
        print(f"  표현식 토큰 수: {len(result_token.expressions[0])}")
        print(f"  표현식 토큰 수: {len(result_token.expressions[1])}")
        print(f"  표현식 토큰 수: {len(result_token.expressions[2])}")
        print(f"  표현식 토큰 수: {len(result_token.expressions[3])}")
        print(f"  표현식 내용: {[t.data.value if t.data else t.type for t in result_token.expressions[0]]}")
        print(f"  표현식 내용: {[t.data.value if t.data else t.type for t in result_token.expressions[1]]}")
        print(f"  표현식 내용: {[t.data.value if t.data else t.type for t in result_token.expressions[2]]}")
        print(f"  표현식 내용: {[t.data.value if t.data else t.type for t in result_token.expressions[3]]}")
        print(f"  다음 토큰 인덱스: {next_idx}")

    except Exception as e:
        print("❌ 오류 발생:", e)


if __name__ == "__main__":
    debug_token_image()
