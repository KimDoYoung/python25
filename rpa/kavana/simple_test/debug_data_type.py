from lib.core.datatypes.array import Array
from lib.core.datatypes.hash_map import HashMap
from lib.core.datatypes.kavana_datatype import Integer, NoneType, String
from lib.core.token import NoneToken
from lib.core.token_type import TokenType


arr = Array([Integer(1), Integer(2), Integer(3)])
assert arr.length() == 3
assert arr.primitive == [1, 2, 3]
assert isinstance(arr.value[0], Integer)
print (arr.primitive)
print("OK")

hm = HashMap(value={
    "name": String("Alice"),
    "age": Integer(30)
})
assert hm.primitive == {"name": "Alice", "age": 30}
assert isinstance(hm.get("name"), String)
assert hm.get("age").primitive == 30
print(hm.primitive)

nt = NoneToken()
assert nt.data == NoneType()
assert nt.data.value == None
assert nt.type == TokenType.NONE
print(nt)

