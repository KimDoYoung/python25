from dataclasses import dataclass, field
from typing import List, Optional, Type
from lib.core.datatypes.kavana_datatype import KavanaDataType
from lib.core.exceptions.kavana_exception import KavanaIndexError, KavanaTypeError, KavanaValueError
from lib.core.datatypes.type_util import deep_primitive, deep_string, deep_token_string


@dataclass
class Array(KavanaDataType):
    value: List[KavanaDataType] = field(default_factory=list)
    data_type: Optional[Type] = None

    def __post_init__(self):
        if self.value:
            self.data_type = type(self.value[0])
            if not all(isinstance(v, self.data_type) for v in self.value):
                raise KavanaTypeError("배열의 요소는 모두 동일한 데이터 타입이어야 합니다")

    def _validate_type(self, item):
        if self.data_type is None:
            self.data_type = type(item)
        elif not isinstance(item, self.data_type):
            raise KavanaTypeError("배열의 요소는 모두 동일한 데이터 타입이어야 합니다")

    def append(self, item):
        self._validate_type(item)
        self.value.append(item)

    def insert(self, index, item):
        self._validate_type(item)
        if 0 <= index <= len(self.value):
            self.value.insert(index, item)
        else:
            raise KavanaIndexError("배열의 인덱스가 범위를 벗어났습니다.")

    def remove(self, item):
        if item in self.value:
            self.value.remove(item)
        else:
            raise KavanaValueError("배열의 값을 찾을 수 없습니다.")

    def remove_at(self, index):
        if 0 <= index < len(self.value):
            del self.value[index]
        else:
            raise KavanaIndexError("배열의 인덱스가 범위를 벗어났습니다.")

    def set(self, row, col=None, token=None):
        self._validate_type(token)
        if col is None:
            if 0 <= row < len(self.value):
                self.value[row] = token
            else:
                raise KavanaIndexError("리스트의 인덱스가 범위를 벗어났습니다")
        else:
            sublist = self.value[row]
            if not isinstance(sublist, list):
                raise KavanaTypeError("2차원 배열이 아닙니다")
            if 0 <= col < len(sublist):
                sublist[col] = token
            else:
                raise KavanaIndexError("2차원 배열의 인덱스가 범위를 벗어났습니다")


    def get(self, row):
        if 0 <= row < len(self.value):
            return self.value[row]
        else:
            raise KavanaIndexError("배열의 인덱스를 벗어났습니다(get)")


    def length(self):
        return len(self.value)

    @property
    def primitive(self):
        return deep_primitive(self.value)

    @property
    def string(self):
        return deep_token_string(self.value)

    def __str__(self):
        return self.string

    def __repr__(self):
        return f"[{', '.join(repr(v) for v in self.value)}]"
    #-------------------------- iterable --------------------------
    def __iter__(self):
        return iter(self.value)

    def __getitem__(self, index):
        return self.value[index]

    def __len__(self):
        return len(self.value)