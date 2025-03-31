import pytest
from lib.core.datatypes.array import Array
from lib.core.datatypes.hash_map import HashMap
from lib.core.datatypes.kavana_datatype import Integer, String

def test_array_basic():
    arr = Array([Integer(1), Integer(2), Integer(3)])
    assert arr.length() == 3
    assert arr.primitive == [1, 2, 3]
    assert isinstance(arr.value[0], Integer)

def test_array_type_error():
    with pytest.raises(Exception):  # 실제로는 KavanaTypeError가 더 좋음
        Array(Integer(1), String("oops"))  # 다른 타입 섞으면 에러

def test_hashmap_basic():
    hm = HashMap(value={
        "name": String("Alice"),
        "age": Integer(30)
    })
    assert hm.primitive == {"name": "Alice", "age": 30}
    assert isinstance(hm.get("name"), String)
    assert hm.get("age").primitive == 30

def test_array_of_hashmaps():
    data = [
        HashMap(value={"id": Integer(1), "name": String("Alice")}),
        HashMap(value={"id": Integer(2), "name": String("Bob")}),
    ]
    arr = Array(data)
    assert arr.primitive == [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
    ]
    assert isinstance(arr.value[1], HashMap)
    assert arr.value[0].get("name").primitive == "Alice"


def test_hashmap_basic():
    hm = HashMap()
    hm.set("name", String("Alice"))
    hm.set("age", Integer(30))

    assert hm.get("name").primitive == "Alice"
    assert hm.contains("age")
    assert not hm.contains("gender")

    assert hm.primitive == {"name": "Alice", "age": 30}
    assert isinstance(hm.string, str)
