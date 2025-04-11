# debug_token_util.py

from typing import List
from lib.core.token_util import TokenUtil

def debug_list_to_array_token(a : List):
    print("=== list_to_array_token 디버그 ===")
    test_data = a
    array_token = TokenUtil.list_to_array_token(test_data)
    print("▶ ArrayToken:")
    print(f"  type: {type(array_token)}")
    print(f"  data: {array_token.data}")
    print(f"  primitive: {array_token.data.primitive}")
    print(f"  string: {array_token.data.string}")
    print(f"  status: {array_token.status}")
    print()


def debug_dict_to_hashmap_token():
    print("=== dict_to_hashmap_token 디버그 ===")
    test_data = {"a": 1, "b": True, "c": "hello"}
    hash_map_token = TokenUtil.dict_to_hashmap_token(test_data)
    print("▶ HashMapToken:")
    print(f"  type: {type(hash_map_token)}")
    print(f"  data: {hash_map_token.data}")
    print(f"  primitive: {hash_map_token.data.primitive}")
    print(f"  string: {hash_map_token.data.string}")
    print(f"  status: {hash_map_token.status}")
    print()

if __name__ == "__main__":
    debug_list_to_array_token([1,2,3])
    debug_list_to_array_token([])
    debug_dict_to_hashmap_token()
