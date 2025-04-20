# Array와 HashMap

## 변경

- ListType -> Array
- ListExToken -> ArrayToken
- ListIndexToken -> AccessIndexToken

## HashMap도입

1. HashMap
2. HashMapToken

```kavana
SET list = [1,2,3]
SET list[1] = 4
SET map = {"a":1,"b":2,"c":3}
SET map["a"] = 4
```

## parsing

```kvs
SET list1 = [1,2,3]
SET map1 = {
    "a":1, "b":2
}
SET v1 = list1[0]
SET v2 = map1["a"]

SET list2 = [
    ["a","b","c"],
    ["d","e","f"]
]
SET map2 = {
    "k1" :{
        "key1": [1,2,3],
        "key2": {
            "key21": "abc"
        }
    }
}
SET v3 = list2[0][2-1]
SET v4 = map2["k1"]["key2"]
SET v5 = map2["k1"]["key2"]["key21"]


```
