import pytest
import os
from lib.core.builtins.path_functions import PathFunctions
from lib.core.token import TokenType
from lib.core.datatypes.kavana_datatype import String

def test_path_join():
    """PATH_JOIN() 함수 테스트"""
    result = PathFunctions.PATH_JOIN("home", "user", "documents", "file.txt")
    expected_path = os.path.join("home", "user", "documents", "file.txt")
    assert result.type == TokenType.STRING
    assert result.data.value == expected_path

def test_path_basename():
    """PATH_BASENAME() 함수 테스트"""
    result = PathFunctions.PATH_BASENAME("/home/user/documents/file.txt")
    assert result.type == TokenType.STRING
    assert result.data.value == "file.txt"

    result = PathFunctions.PATH_BASENAME("C:\\Users\\Admin\\file.txt")
    assert result.type == TokenType.STRING
    assert result.data.value == "file.txt"

def test_path_dirname():
    """PATH_DIRNAME() 함수 테스트"""
    result = PathFunctions.PATH_DIRNAME("/home/user/documents/file.txt")
    assert result.type == TokenType.STRING
    assert result.data.value == "/home/user/documents"

    result = PathFunctions.PATH_DIRNAME("C:\\Users\\Admin\\file.txt")
    assert result.type == TokenType.STRING
    assert result.data.value == "C:\\Users\\Admin"
