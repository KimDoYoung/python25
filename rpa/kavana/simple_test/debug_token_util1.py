import json
from lib.core.datatypes.hash_map import HashMap
from lib.core.token_type import TokenType
from lib.core.token_util import TokenUtil

if __name__ == "__main__":
    # 테스트할 JSON 문자열
    json_str = '''
    {
        "response": {
            "header": {
                "resultCode": "00",
                "resultMsg": "OK"
            },
            "body": {
                "items": [
                    {"name": "a", "value": 1},
                    {"name": "b", "value": 2}
                ]
            }
        }
    }
    '''

    # 문자열 → 파이썬 dict 변환
    data = json.loads(json_str)

    # dict → HashMapToken 변환
    token = TokenUtil.dict_to_hashmap_token(data)
    assert token.type == TokenType.HASH_MAP, "HashMapToken 변환 실패"
    assert isinstance(token.data, HashMap), "HashMapToken 변환 실패"
    
    # 변환 결과 출력 (repr 사용 시 내부 구조까지 보기 좋음)
    print("🔍 HashMapToken 변환 결과:")
    print(repr(token))
    print("➡️ 실제 데이터 구조:")
    print(token.data.primitive)

    # Array 테스트도 해보자
    array_data = [1, 2, 3, 4]
    array_token = TokenUtil.list_to_array_token(array_data)
    print("\n🔍 ArrayToken 변환 결과:")
    print(repr(array_token))
    print("➡️ 실제 데이터 구조:")
    print(array_token.data.value)  # 내부 Array 객체의 value 출력
