import os
import pytest
import hashlib
from lib.core.builtins.file_functions import FileFunctions
from lib.core.token import TokenType
from lib.core.datatypes.kavana_datatype import String, Boolean, Integer

# 테스트용 파일 및 디렉토리 설정
TEST_DIR = "test_dir"
TEST_FILE = "test_file.txt"
TEST_FILE_PATH = os.path.join(TEST_DIR, TEST_FILE)
COPY_FILE_PATH = os.path.join(TEST_DIR, "copied_file.txt")
MOVED_FILE_PATH = os.path.join(TEST_DIR, "moved_file.txt")
TEST_CONTENT = "Hello, this is a test."

@pytest.fixture(scope="function", autouse=True)
def setup_teardown():
    """테스트 전에 폴더 및 파일 생성, 테스트 후 정리"""
    os.makedirs(TEST_DIR, exist_ok=True)
    with open(TEST_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(TEST_CONTENT)
    yield
    # 테스트 후 파일 및 폴더 정리
    if os.path.exists(TEST_FILE_PATH):
        os.remove(TEST_FILE_PATH)
    if os.path.exists(COPY_FILE_PATH):
        os.remove(COPY_FILE_PATH)
    if os.path.exists(MOVED_FILE_PATH):
        os.remove(MOVED_FILE_PATH)
    os.rmdir(TEST_DIR)

    from unittest.mock import Mock

    class MockExecutor:
        def execute(self, *args, **kwargs):
            return Mock()
        def log_command(self, *args, **kwargs):
            pass

    FileFunctions.executor = MockExecutor()

def test_file_write():
    """파일 쓰기 테스트"""
    result = FileFunctions.FILE_WRITE(TEST_FILE_PATH, "New Content")
    assert result.type == TokenType.BOOLEAN
    assert result.data.value is True

def test_file_exists():
    """파일 존재 여부 테스트"""
    result = FileFunctions.FILE_EXISTS(TEST_FILE_PATH)
    assert result.type == TokenType.BOOLEAN
    assert result.data.value is True

def test_file_read():
    """파일 읽기 테스트"""
    result = FileFunctions.FILE_READ(TEST_FILE_PATH)
    assert result.type == TokenType.STRING
    assert result.data.value == TEST_CONTENT


def test_file_copy():
    """파일 복사 테스트"""
    result = FileFunctions.FILE_COPY(TEST_FILE_PATH, COPY_FILE_PATH)
    assert result.type == TokenType.BOOLEAN
    assert result.data.value is True
    assert os.path.exists(COPY_FILE_PATH)

def test_file_move():
    """파일 이동 테스트"""
    result = FileFunctions.FILE_MOVE(TEST_FILE_PATH, MOVED_FILE_PATH)
    assert result.type == TokenType.BOOLEAN
    assert result.data.value is True
    assert os.path.exists(MOVED_FILE_PATH)
    assert not os.path.exists(TEST_FILE_PATH)

def test_file_hash():
    """파일 해시 값 테스트 (MD5)"""
    expected_hash = hashlib.md5(TEST_CONTENT.encode()).hexdigest()
    result = FileFunctions.FILE_HASH(TEST_FILE_PATH, "md5")
    assert result.type == TokenType.STRING
    assert result.data.value == expected_hash

def test_file_lines():
    """파일 줄 단위 읽기 테스트"""
    with open(TEST_FILE_PATH, "w", encoding="utf-8") as f:
        f.write("line1\nline2\nline3")

    result = FileFunctions.FILE_LINES(TEST_FILE_PATH)
    assert result.type == TokenType.ARRAY
    # r = [item.data.value for item in result.data]
    # print(r)
    # assert r == ["line1", "line2", "line3"]

def test_file_delete():
    """파일 삭제 테스트"""
    result = FileFunctions.FILE_DELETE(TEST_FILE_PATH)
    assert result.type == TokenType.BOOLEAN
    assert result.data.value is True
    assert not os.path.exists(TEST_FILE_PATH)

def test_file_append():
    """파일 끝에 문자열 추가 테스트"""
    append_content = " Appended Content"
    result = FileFunctions.FILE_APPEND(TEST_FILE_PATH, append_content)
    assert result.type == TokenType.BOOLEAN
    assert result.data.value is True

    with open(TEST_FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == TEST_CONTENT + append_content

def test_file_info():
    """파일 정보 반환 테스트"""
    result = FileFunctions.FILE_INFO(TEST_FILE_PATH)
    assert result.type == TokenType.HASH_MAP
    file_info = result.data.value
    assert file_info["name"].data.value == TEST_FILE
    assert file_info["size"].data.value == len(TEST_CONTENT)
    assert "modified_time" in file_info

def test_file_find():
    """디렉토리에서 패턴과 일치하는 파일 찾기 테스트"""
    result = FileFunctions.FILE_FIND(TEST_DIR, "*.txt")
    assert result.type == TokenType.ARRAY
    file_list = [item.data.value for item in result.data.value]
    # print (file_list)
    # assert any(TEST_FILE in file["name"] for file in file_list)

def test_file_temp_name():
    """임시 파일 이름 생성 테스트"""
    suffix = ".tmp"
    result = FileFunctions.FILE_TEMP_NAME(suffix)
    assert result.type == TokenType.STRING
    temp_file_name = result.data.value
    assert temp_file_name.endswith(suffix)
    assert os.path.exists(temp_file_name)
    os.remove(temp_file_name)