from lib.core.token_type import TokenType


def format_pretty(parsed_commands, keywords=None):
    """
    ✅ Kavana 스크립트를 예쁘게 포맷팅하는 함수 (Depth 적용)
    - 키워드(명령어)는 대문자로 변환
    - 변수명은 소문자로 변환
    - 블록 구조(IF, FOR, WHILE 등)는 들여쓰기 적용
    """
    formatted_lines = []
    indentation_level = 0  # ✅ 들여쓰기 레벨 (Depth)

    for tokens in parsed_commands:
        cmd = tokens[0].data.string  # ✅ 명령어는 대문자로 변환
        args = tokens[1:]  # ✅ 나머지는 `Token` 리스트 그대로 유지        

        # ✅ 키워드는 대문자로 변환
        if cmd.upper() in keywords:
            cmd = cmd.upper()

        # ✅ 변수명 및 키워드 변환
        formatted_args = []
        for arg in args:
            if arg.data.string.upper() in keywords:
                formatted_args.append(arg.upper())  # ✅ 키워드는 대문자
            else:
                formatted_args.append(arg)  # ✅ 숫자, 문자열 그대로 유지

        # ✅ 블록 종료 키워드(`END_IF`, `END_FOR` 등)는 들여쓰기 감소
        if cmd.upper().startswith("END_"):
            indentation_level -= 1

        # ✅ 들여쓰기 적용 후 명령어 추가
        # formatted_lines.append("    " * indentation_level + f"{cmd} {' '.join(token.data.string for token in formatted_args)}")
        formatted_lines.append(
            "    " * indentation_level + 
            f"{cmd} {' '.join(f'\"{token.data.string}\"' if token.type == TokenType.STRING else token.data.string for token in formatted_args)}"
        )


        # ✅ 블록 시작 키워드(`IF`, `FOR`, `WHILE` 등)는 들여쓰기 증가
        if cmd in {"MAIN", "ON_EXCEPTION", "IF", "FOR", "WHILE", "FUNCTION"}:
            indentation_level += 1

    return "\n".join(formatted_lines)
