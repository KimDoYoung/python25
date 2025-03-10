import pytest
from lib.core.datatypes.kavana_datatype import KavanaDataType
from lib.core.datatypes.list_type import ListType  # ListType이 있는 경로에 맞게 수정하세요.

def test_list_initialization():
    lst = ListType(1, 2, 3)
    assert lst.primitive == [1, 2, 3]
    assert lst.data_type == int

    lst_str = ListType("a", "b", "c")
    assert lst_str.primitive == ["a", "b", "c"]
    assert lst_str.data_type == str

    with pytest.raises(TypeError):
        ListType(1, "a", 3)  # 다른 타입 혼합

def test_append():
    lst = ListType(10, 20)
    lst.append(30)
    assert lst.primitive == [10, 20, 30]

    with pytest.raises(TypeError):
        lst.append("string")  # 타입이 다름

    nested_list = ListType(1, 2)
    with pytest.raises(TypeError):
        lst.append(nested_list)  # Nested ListType 금지

def test_insert():
    lst = ListType(1, 2, 4)
    lst.insert(2, 3)
    assert lst.primitive == [1, 2, 3, 4]

    with pytest.raises(IndexError):
        lst.insert(10, 5)  # 범위를 벗어난 인덱스

    with pytest.raises(TypeError):
        lst.insert(1, "a")  # 타입 불일치

def test_remove():
    lst = ListType(5, 10, 15)
    lst.remove(10)
    assert lst.primitive == [5, 15]

    with pytest.raises(ValueError):
        lst.remove(100)  # 없는 값 삭제 시도

def test_remove_at():
    lst = ListType("a", "b", "c")
    lst.remove_at(1)
    assert lst.primitive == ["a", "c"]

    with pytest.raises(IndexError):
        lst.remove_at(10)  # 범위를 벗어난 인덱스

def test_set():
    lst = ListType(1, 2, 3)
    lst.set(1, value=99)
    assert lst.primitive == [1, 99, 3]

    with pytest.raises(TypeError):
        lst.set(0, value="string")  # 타입 불일치

    with pytest.raises(IndexError):
        lst.set(10, value=100)  # 범위를 벗어난 인덱스

def test_get():
    lst = ListType(100, 200, 300)
    assert lst.get(1) == 200

    with pytest.raises(IndexError):
        lst.get(10)  # 범위를 벗어난 인덱스

def test_length():
    lst = ListType(7, 8, 9, 10)
    assert lst.length() == 4

def test_string_property():
    lst = ListType(1, 2, 3)
    assert lst.string == "[1, 2, 3]"

def test_primitive_property():
    lst = ListType(4, 5, 6)
    assert lst.primitive == [4, 5, 6]

def test_repr():
    lst = ListType(1, 2, 3)
    assert repr(lst) == "LIST(1, 2, 3)"
