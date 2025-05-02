import pytest

from lib.core.command_parser import CommandParser
from lib.core.command_preprocessor import PreprocessedLine
from lib.core.token_type import TokenType
from tests.helper_func import get_raw_tokens, get_tokens, get_command

@pytest.fixture
def parser():
    return CommandParser()

def test_command_parser0():
    ''' set i = -1 '''
    s = [
        "set i = -1",
        "set i = 1 + -1",
        "set i = 1 - 10",
        "set i = 1 +-1",
        "set i = 1 ++1",
        "set c = 2+3+(4*5)"
    ]    
    for str in s:
        commands = get_command(str)
        cmd = commands[0]['cmd']
        args = commands[0]['args']
        # print (commands[0]['cmd'])
        print ("\n--------------------------------")
        for token in args:
            print (token.type, token.data.value)
        print ("--------------------------------")
        # assert cmd == "SET"
        # assert len (args) == 3



def test_command_parser1():
    commands = get_command("set i = 1 + 1")
    cmd = commands[0]['cmd']
    args = commands[0]['args']
    # print (commands[0]['cmd'])
    assert cmd == "SET"
    assert len (args) == 5

def test_command_parser2(parser):
    ppLine = PreprocessedLine("SET i = 1 + 1", 1, 1)
    tokens = parser.pre_process_tokens(ppLine)
    assert len(tokens) == 6

def test_parse_string_token(parser):
    ''' parse_string_token() 테스트 '''
    str = "r\"\"\"hello world\"\"\""

    token = parser.parse_string_token(str,0,1)
    assert token.type == TokenType.STRING 


def test_find_matching_brace(parser):
    ''' find_matching_brace() 테스트 '''
    str = "{ 1: 2 }"
    tokens = get_raw_tokens(str)
    result = parser.find_matching_brace(tokens, 0)
    assert result == 4

@pytest.mark.parametrize("test_str1", [
    "a[1]",
    "arr[10]",
    "matrix[i][j]",
    "data[index + 1]",
    "list[func(x)]"
])
def test_make_access_index_token(parser, test_str1):
    ''' make_access_index_token() 테스트 '''
    tokens = get_raw_tokens(test_str1)
    result,_ = parser.make_access_index_token(tokens, 0)
    assert result.type == TokenType.ACCESS_INDEX

