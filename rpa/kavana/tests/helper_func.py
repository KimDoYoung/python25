from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor
from lib.core.token_type import TokenType



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

def get_tokens_of_line(s:str):
    s = "MAIN\n" + s + "\nEND_MAIN"
    lines = [s.strip() for s in s.split("\n") if s.strip()]
    command_preprocssed_lines = CommandPreprocessor().preprocess(lines)
    parsed_commands = CommandParser().parse(command_preprocssed_lines)
    tokens = parsed_commands[0]["args"]
    return tokens