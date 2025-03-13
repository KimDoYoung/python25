from lib.core.token_type import TokenType


def syntax_check(parsed_commands, keywords=None):
    """
    1. 명령어가 예약어인지 확인
    """
    result = True
    for command in parsed_commands:
        cmd = command["cmd"]
        args =command["args"]
        if not cmd.upper() in keywords:
            print(f"{cmd} 는 명령어(예약어)가 아닙니다")
            result = False

    return result