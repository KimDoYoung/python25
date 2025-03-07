import pytest
from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import CommandPreprocessor
from lib.core.token import Token, ListExToken
from lib.core.token_type import TokenType
from lib.core.datatypes.kavana_datatype import String, Integer
from lib.core.datatypes.list_type import ListType

@pytest.mark.parametrize("script, expected_parsed", [
    (
        "SET a = [1,2,3]",
        {
            "cmd": "SET",
            "args": [
                Token(data=String("a"), type=TokenType.IDENTIFIER),
                Token(data=String("="), type=TokenType.OPERATOR),
                ListExToken(
                    data=ListType([]),
                    element_expresses=[
                        [Token(data=Integer(1), type=TokenType.INTEGER)],
                        [Token(data=Integer(2), type=TokenType.INTEGER)],
                        [Token(data=Integer(3), type=TokenType.INTEGER)],
                    ],
                    status="Parsed"
                )
            ]
        }
    )
])
def test_command_parser(script, expected_parsed):
    """ ✅ 파싱된 결과 검증 """

    # ✅ 1. 전처리 & 파싱
    script_lines = script.split("\n")
    processed_lines = CommandPreprocessor().preprocess(script_lines)
    parsed_commands = CommandParser().parse(processed_lines)

    # 🔍 **명령어 이름 비교**
    assert parsed_commands[0]["cmd"] == expected_parsed["cmd"], \
        f"\nExpected Command: {expected_parsed['cmd']}\nGot: {parsed_commands[0]['cmd']}"

    # 🔍 **인자 리스트 비교 (`ListExToken` 포함)**
    parsed_args = parsed_commands[0]["args"]
    expected_args = expected_parsed["args"]

    assert len(parsed_args) == len(expected_args), \
        f"\nExpected Args Length: {len(expected_args)}\nGot: {len(parsed_args)}"

    for i, (parsed_arg, expected_arg) in enumerate(zip(parsed_args, expected_args)):
        if isinstance(expected_arg, ListExToken):
            assert isinstance(parsed_arg, ListExToken), \
                f"\nExpected ListExToken at index {i}\nGot: {parsed_arg}"

            # ✅ `ListExToken` 내부 요소 비교
            assert len(parsed_arg.element_expresses) == len(expected_arg.element_expresses), \
                f"\nListExToken Mismatch at index {i}\nExpected: {expected_arg}\nGot: {parsed_arg}"

            for j, (parsed_expr, expected_expr) in enumerate(zip(parsed_arg.element_expresses, expected_arg.element_expresses)):
                assert [(t.data.value, t.type) for t in parsed_expr] == [(t.data.value, t.type) for t in expected_expr], \
                    f"\nListExToken Element Mismatch at index {i}, element {j}\nExpected: {expected_expr}\nGot: {parsed_expr}"
        else:
            assert (parsed_arg.data.value, parsed_arg.type) == (expected_arg.data.value, expected_arg.type), \
                f"\nExpected Arg at index {i}: {expected_arg}\nGot: {parsed_arg}"
