# debug_token_util.py

import json
from typing import List
from lib.core.datatypes.hash_map import HashMap
from lib.core.token_util import TokenUtil

def json_str_to_hashmap(json_str: str) -> HashMap:
    from lib.core.token_util import TokenUtil
    import json

    try:
        # 문자열을 Python dict/list 등으로 파싱
        parsed = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 파싱 오류: {e}")

    # TokenUtil을 사용하여 KavanaDataType으로 변환
    kavana_obj = TokenUtil.primitive_to_kavana(parsed)

    if not isinstance(kavana_obj, HashMap):
        raise TypeError("JSON 루트 객체는 반드시 HashMap이어야 합니다.")

    return kavana_obj

def test1():
    json_str = "{'response': {'header': {'resultCode': '00', 'resultMsg': 'NORMAL SERVICE.'}, 'body': {'items': {'item': [{'dateKind': '02', 'dateName': '4·3희생자 추념일', 'isHoliday': 'N', 'locdate': '20250403', 'seq': '1'}, {'dateKind': '02', 'dateName': '예비군의 날', 'isHoliday': 'N', 'locdate': '20250404', 'seq': '2'}, {'dateKind': '02', 'dateName': '식목일', 'isHoliday': 'N', 'locdate': '20250405', 'seq': '1'}, {'dateKind': '02', 'dateName': '보건의 날', 'isHoliday': 'N', 'locdate': '20250407', 'seq': '1'}, {'dateKind': '02', 'dateName': '대한민국임시정부 수립기념일', 'isHoliday': 'N', 'locdate': '20250411', 'seq': '1'}, {'dateKind': '02', 'dateName': '도시농업의 날', 'isHoliday': 'N', 'locdate': '20250411', 'seq': '2'}, {'dateKind': '02', 'dateName': '4·19혁명 기념일', 'isHoliday': 'N', 'locdate': '20250419', 'seq': '1'}, {'dateKind': '02', 'dateName': '장애인의 날', 'isHoliday': 'N', 'locdate': '20250420', 'seq': '2'}, {'dateKind': '02', 'dateName': '과학의 날', 'isHoliday': 'N', 'locdate': '20250421', 'seq': '1'}, {'dateKind': '02', 'dateName': '정보통신의 날', 'isHoliday': 'N', 'locdate': '20250422', 'seq': '1'}]}, 'numOfRows': '10', 'pageNo': '1', 'totalCount': '13'}}}"

    #json_str 을 dict 로 변환
    json_str = json_str.replace("'", "\"")
    json_dict = json.loads(json_str)  # json.loads 사용
    print(json_dict)
    item_list = (json_dict["response"]["body"]["items"]["item"])
    for item1 in item_list:
        print (f"dateKind: {item1['dateKind']}, dateName: {item1['dateName']}, isHoliday: {item1['isHoliday']}, locdate: {item1['locdate']}, seq: {item1['seq']}")

    kavana_hashmap = json_str_to_hashmap(json_str)
    print(kavana_hashmap.get("response"))
    print(kavana_hashmap.get("response").get("header"))
    print(kavana_hashmap.get("response").get("header").get("resultCode"))
    print(kavana_hashmap.get("response").get("body").get("items").get("item"))
    

if __name__ == "__main__":
    test1()