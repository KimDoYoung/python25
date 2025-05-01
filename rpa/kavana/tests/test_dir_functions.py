import os
import shutil
import pytest
from lib.core.builtins.dir_functions import DirFunctions
from lib.core.token_type import TokenType

# 테스트용 디렉토리 이름
TEST_DIR = "test_temp_dir"

def setup_module(module):
    # 테스트 전 정리
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)

def teardown_module(module):
    # 테스트 후 정리
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)

def test_DIR_CREATE():
    token = DirFunctions.DIR_CREATE(TEST_DIR)
    assert token.data.value is True
    assert os.path.isdir(TEST_DIR)

def test_DIR_EXISTS_true():
    token = DirFunctions.DIR_EXISTS(TEST_DIR)
    assert token.data.value is True

def test_DIR_EXISTS_false():
    token = DirFunctions.DIR_EXISTS("non_existing_dir")
    assert token.data.value is False

def test_DIR_LIST():
    # 테스트 파일 생성
    filenames = ["file1.txt", "file2.txt"]
    for fname in filenames:
        with open(os.path.join(TEST_DIR, fname), 'w') as f:
            f.write("test")

    token = DirFunctions.DIR_LIST(TEST_DIR)
    assert token.type == TokenType.ARRAY
def test_DIR_DELETE():
    # 디렉토리 비워야 삭제 가능
    for f in os.listdir(TEST_DIR):
        os.remove(os.path.join(TEST_DIR, f))

    token = DirFunctions.DIR_DELETE(TEST_DIR)
    assert token.data.value is True
    assert not os.path.exists(TEST_DIR)

def test_DIR_DELETE_fail():
    os.makedirs(TEST_DIR, exist_ok=True)
    with open(os.path.join(TEST_DIR, "dummy.txt"), "w") as f:
        f.write("test")

    token = DirFunctions.DIR_DELETE(TEST_DIR)
    assert token.data.value is False
