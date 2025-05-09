# test_token_util.py

from lib.core.datatypes.hash_map import HashMap
from lib.core.datatypes.image import Image
from lib.core.datatypes.kavana_datatype import Boolean, Integer, String
from lib.core.datatypes.point import Point
from lib.core.datatypes.region import Region
from lib.core.token import ArrayToken, HashMapToken, StringToken, Token, TokenStatus
from lib.core.token_custom import ImageToken, PointToken, RegionToken
from lib.core.token_type import TokenType
from lib.core.token_util import TokenUtil
from tests.helper_func import create_test_image

def test_xy_to_point_token():
    pt = TokenUtil.xy_to_point_token(10, 20)
    assert isinstance(pt, PointToken)
    assert pt.type == TokenType.POINT
    assert pt.status == TokenStatus.EVALUATED
    assert isinstance(pt.data, Point)
    assert pt.data.x == 10
    assert pt.data.y == 20

def test_string_to_string_token():
    st = TokenUtil.string_to_string_token("test")
    assert isinstance(st, StringToken)
    assert st.type == TokenType.STRING
    assert isinstance(st.data, String)
    assert st.data.value == "test"

def test_region_to_token():
    st = TokenUtil.region_to_token((1, 2, 3, 4))
    assert isinstance(st, RegionToken)
    assert st.type == TokenType.REGION
    assert isinstance(st.data, Region)
    assert st.data.value == (1, 2, 3, 4)
    assert st.status == TokenStatus.EVALUATED

def test_integer_to_integer_token():
    it = TokenUtil.integer_to_integer_token(10)
    assert isinstance(it, Token)
    assert it.type == TokenType.INTEGER
    assert isinstance(it.data, Integer)
    assert it.data.value == 10

def test_boolean_to_boolean_token():
    bt = TokenUtil.boolean_to_boolean_token(True)
    assert isinstance(bt, Token)
    assert bt.type == TokenType.BOOLEAN
    assert isinstance(bt.data, Boolean)
    assert bt.data.value == True

def test_array_to_array_token():
    """리스트를 Token으로 변환하는 테스트"""
    array = []
    array.append(TokenUtil.string_to_string_token("aaa"))
    array.append(TokenUtil.string_to_string_token("bbb"))
    array.append(TokenUtil.string_to_string_token("ccc"))
    at = TokenUtil.array_to_array_token(array)
    assert isinstance(at, ArrayToken)
    assert at.type == TokenType.ARRAY
    list1 = at.data.value
    for item in list1:
        assert isinstance(item, StringToken)
        assert item.type == TokenType.STRING
        assert isinstance(item.data, String)
        assert item.data.value in ["aaa", "bbb", "ccc"]

    assert at.status == TokenStatus.EVALUATED

def test_image_to_image_token():
    """이미지 파일을 Token으로 변환하는 테스트"""
    path = create_test_image()
    image = Image(path)
    it = TokenUtil.image_to_image_token(image)
    assert isinstance(it, ImageToken)
    assert it.type == TokenType.IMAGE
    assert isinstance(it.data, Image)
    assert it.data == Image(path)  

def test_dict_to_hashmap_token():
    """딕셔너리를 Token으로 변환하는 테스트"""
    dict1 = {
        "key1": 1,
        "key2": 2,
        "key3": [1, 2, 3],
        "key4": {
            "key5": 5,
            "key6": 6
        }
    }
    ht = TokenUtil.dict_to_hashmap_token(dict1)
    assert isinstance(ht, HashMapToken)
    assert ht.type == TokenType.HASH_MAP
    assert isinstance(ht.data, HashMap)
    assert ht.status == TokenStatus.EVALUATED
    map1 = ht.data
    assert map1.get("key1").data.value == 1
    assert map1.get("key2").data.value == 2
    array1 = map1.get("key3").data
    int_array = []
    for int_token in array1.value:
        assert isinstance(int_token, Token)
        assert int_token.type == TokenType.INTEGER
        int_array.append(int_token.data.value)
    
    assert int_array == [1, 2, 3]