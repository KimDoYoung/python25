import pytest

from lib.core.command_parser import CommandParser
from lib.core.token_type import TokenType
from tests.helper_func import get_tokens, get_tokens_of_line

@pytest.fixture
def parser():
    return CommandParser()

def test_command_parser1():
    tokens = get_tokens_of_line("set i = 1+1")
    tokens[0].type == TokenType.IDENTIFIER
    for token in tokens:
        print(token.type)