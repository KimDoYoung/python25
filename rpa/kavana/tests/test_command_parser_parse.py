import pytest
from lib.core.command_parser import CommandParser
from lib.core.token import Token
from lib.core.token_type import TokenType

@pytest.mark.parametrize("script_lines, expected_commands", [
    # ✅ 1. 단순 변수 할당 테스트
    ([  
        "MAIN",
        "SET a = 10",
        "END_MAIN"
     ], [
        {"cmd": "SET", "args": [
            Token(value="a", type=TokenType.IDENTIFIER, line=2, column=4),  # ✅ line=2로 수정
            Token(value="=", type=TokenType.OPERATOR, line=2, column=6),  # ✅ line=2로 수정
            Token(value="10", type=TokenType.INTEGER, line=2, column=8),  # ✅ line=2로 수정
        ]}
    ]),
    # ✅ 1. FOR 루프가 포함된 테스트
    ([
        "MAIN",
        "    SET a = 10",
        "    FOR i = 1 TO a STEP 2",
        "        PRINT \"{i}\"",
        "    END_FOR",
        "END_MAIN"
    ], [
        {"cmd": "SET", "args": [
            Token(value="a", type=TokenType.IDENTIFIER, line=2, column=8),
            Token(value="=", type=TokenType.OPERATOR, line=2, column=10),
            Token(value="10", type=TokenType.INTEGER, line=2, column=12),
        ]},
        {"cmd": "FOR_BLOCK", "body": [
            {"cmd": "FOR", "args": [
                Token(value="i", type=TokenType.IDENTIFIER, line=3, column=8),
                Token(value="=", type=TokenType.OPERATOR, line=3, column=10),
                Token(value="1", type=TokenType.INTEGER, line=3, column=12),
                Token(value="TO", type=TokenType.TO, line=3, column=14),
                Token(value="a", type=TokenType.IDENTIFIER, line=3, column=17),
                Token(value="STEP", type=TokenType.STEP, line=3, column=19),
                Token(value="2", type=TokenType.INTEGER, line=3, column=24),
            ]},
            {"cmd": "PRINT", "args": [
                Token(value="\"{i}\"", type=TokenType.STRING, line=4, column=12),
            ]},
        ]}
    ]),    

])
def test_command_parser(script_lines, expected_commands):
    """✅ `CommandParser.parse()`가 올바르게 동작하는지 검증"""
    parser = CommandParser(script_lines)
    parsed_commands = parser.parse()
    
    assert len(parsed_commands) == len(expected_commands), f"Expected {len(expected_commands)} commands, but got {len(parsed_commands)}"

    for i in range(len(parsed_commands)):
        assert parsed_commands[i]["cmd"] == expected_commands[i]["cmd"], f"Mismatch at index {i}: expected '{expected_commands[i]['cmd']}', got '{parsed_commands[i]['cmd']}'"
        assert parsed_commands[i]["args"] == expected_commands[i]["args"], f"Args mismatch at index {i}: expected '{expected_commands[i]['args']}', got '{parsed_commands[i]['args']}'"
