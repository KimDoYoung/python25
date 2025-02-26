def format_pretty(parsed_commands):
    """
    ✅ Kavana 스크립트를 예쁘게 포맷팅하는 함수 (Depth 적용)
    - 키워드(명령어)는 대문자로 변환
    - 변수명은 소문자로 변환
    - 블록 구조(IF, FOR, WHILE 등)는 들여쓰기 적용
    """
    formatted_lines = []
    keywords = {"IF", "ELSE", "WHILE", "FOR", "FUNCTION", "RETURN", "INCLUDE", "LOAD", 
                "BREAK", "CONTINUE", "MAIN", "END_MAIN", "END_IF", "END_WHILE", "END_FOR"}
    indentation_level = 0  # ✅ 들여쓰기 레벨 (Depth)

    for command in parsed_commands:
        cmd = command["cmd"]
        args = command["args"]

        # ✅ 키워드는 대문자로 변환
        if cmd in keywords:
            cmd = cmd.upper()
        else:
            cmd = cmd.lower()  # ✅ 키워드가 아니면 소문자로 변환 (변수명)

        # ✅ 변수명 및 키워드 변환
        formatted_args = []
        for arg in args:
            if arg.upper() in keywords:
                formatted_args.append(arg.upper())  # ✅ 키워드는 대문자
            elif arg.isidentifier():  # ✅ 변수명은 소문자
                formatted_args.append(arg.lower())
            else:
                formatted_args.append(arg)  # ✅ 숫자, 문자열 그대로 유지

        # ✅ 블록 종료 키워드(`END_IF`, `END_FOR` 등)는 들여쓰기 감소
        if cmd.startswith("END_"):
            indentation_level -= 1

        # ✅ 들여쓰기 적용 후 명령어 추가
        formatted_lines.append("    " * indentation_level + f"{cmd} {' '.join(formatted_args)}")

        # ✅ 블록 시작 키워드(`IF`, `FOR`, `WHILE` 등)는 들여쓰기 증가
        if cmd in {"IF", "FOR", "WHILE", "FUNCTION"}:
            indentation_level += 1

    return "\n".join(formatted_lines)
