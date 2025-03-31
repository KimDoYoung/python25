from lib.core.datatypes.array import Array
from lib.core.datatypes.hash_map import HashMap
from lib.core.datatypes.kavana_datatype import Integer, String


arr = Array(Integer(1), Integer(2), Integer(3))
assert len(arr.data) == 3
assert arr.primitive == [1, 2, 3]
assert isinstance(arr.data[0], Integer)
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