# ---------------------------------------------
# pytest 테스트 함수
# ---------------------------------------------
import pytest
from lib.core.datatypes.hash_map import HashMap
from lib.core.token import HashMapToken
from lib.core.token_type import TokenType


def test_hash_map_token_creation():
    # 준비
    a = {"a": 1, "b": 2}
    hashmap = HashMap(a)

    # 실행
    token = HashMapToken(data=hashmap)

    # 검증
    assert token.data == hashmap
    assert token.type == TokenType.HASH_MAP
    assert token.status == "Parsed"
    assert isinstance(token.key_express_map, dict)

def test_hash_map_token_invalid_data_type():
    with pytest.raises(TypeError):
        HashMapToken(data={"not": "a HashMap object"})  # 잘못된 타입