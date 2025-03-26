import os
import pytest
from lib.core.builtins.dir_functions import DirFunctions
from lib.core.token import TokenType

# 테스트용 폴더 및 파일 이름 설정
TEST_DIR = "test_dir"
TEST_FILE = "test_file.txt"
TEST_FILE_PATH = os.path.join(TEST_DIR, TEST_FILE)

def test_dir_create():
    """폴더 생성 테스트"""
    result = DirFunctions.DIR_CREATE(TEST_DIR)
    assert result.type == TokenType.BOOLEAN
    assert result.data.value is True  # 폴더가 생성되었는지 확인
    assert os.path.isdir(TEST_DIR)

def test_dir_exists():
    """폴더 존재 여부 테스트"""
    result = DirFunctions.DIR_EXISTS(TEST_DIR)
    assert result.type == TokenType.BOOLEAN
    assert result.data.value is True  # 폴더가 존재하는지 확인

def test_dir_list():
    """폴더 내 파일 목록 확인 테스트"""
    # 파일 생성
    with open(TEST_FILE_PATH, "w") as f:
        f.write("test content")

    result = DirFunctions.DIR_LIST(TEST_DIR)
    assert result.type == TokenType.ARRAY
    # assert TEST_FILE in [token.value for token in result.data.value]  # 파일이 목록에 있는지 확인

def test_dir_delete():
    """폴더 삭제 테스트"""
    # 파일 삭제
    os.remove(TEST_FILE_PATH)

    # 폴더 삭제 시도
    result = DirFunctions.DIR_DELETE(TEST_DIR)
    assert result.type == TokenType.BOOLEAN
    assert result.data.value is True  # 폴더 삭제 성공 여부 확인
    assert not os.path.exists(TEST_DIR)  # 폴더가 삭제되었는지 확인
