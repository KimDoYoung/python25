from typing import Union, Dict, TYPE_CHECKING
from dataclasses import dataclass, field

from lib.core.datatypes.kavana_datatype import KavanaDataType
from lib.core.datatypes.type_util import deep_primitive
from lib.core.exceptions.kavana_exception import (
    KavanaKeyError, KavanaTypeError
)

if TYPE_CHECKING:
    from lib.core.token import Token  # 타입 힌트 용도


@dataclass
class HashMap(KavanaDataType):
    value: Dict[Union[str, int], KavanaDataType] = field(default_factory=dict)

    def get(self, key: Union[str, int]) -> KavanaDataType:
        """키로 값 조회. 존재하지 않으면 에러 발생."""
        if key not in self.value:
            raise KavanaKeyError(f"키 '{key}'를 발견할 수 없습니다.")
        return self.value[key]

    def set(self, key: Union[str, int], val: KavanaDataType) -> None:
        """키에 값 설정. 값은 반드시 KavanaDataType이어야 함."""
        if not isinstance(val, KavanaDataType):
            raise KavanaTypeError("HashMap의 값은 KavanaDataType 인스턴스여야 합니다.")
        self.value[key] = val

    def remove(self, key: Union[str, int]) -> None:
        """키가 존재할 경우 제거"""
        if key in self.value:
            del self.value[key]
        else:
            raise KavanaKeyError(f"키 '{key}'를 삭제할 수 없습니다. 존재하지 않습니다.")

    def contains(self, key: Union[str, int]) -> bool:
        return key in self.value

    @property
    def primitive(self) -> dict:
        """Python 기본 dict로 변환"""
        return deep_primitive(self.value)

    @property
    def string(self) -> str:
        """문자열 표현"""
        return str({k: v.string for k, v in self.value.items()})

    def __repr__(self) -> str:
        """디버깅용 표현"""
        pairs = ", ".join(f"{k}: {v}" for k, v in self.value.items())
        return f"{{{pairs}}}"

# from typing import Union, Dict, TYPE_CHECKING
# from dataclasses import dataclass, field
# from typing import Dict, Union

# from lib.core.datatypes.kavana_datatype import KavanaDataType
# from lib.core.datatypes.type_util import deep_primitive
# from lib.core.exceptions.kavana_exception import KavanaKeyError


# if TYPE_CHECKING:
#     from lib.core.token import Token  # 타입 검사용

# @dataclass
# class HashMap(KavanaDataType):
#     value: Dict[Union[str, int], KavanaDataType] = field(default_factory=dict)

#     def get(self, key: str | int) -> 'Token':
#         if key not in self.value:
#             raise KavanaKeyError(f"키 '{key}'를 발견할 수 없습니다.")
#         return self.value[key]

#     def set(self, key: Union[str, int], val: 'Token') -> None:
#         if not isinstance(val, Token):
#             raise KavanaTypeError("HashMap의 값은 토큰이어야 합니다.")
#         self.value[key] = val

#     def remove(self, key: str|int) -> None:
#         if key in self.value:
#             del self.value[key]

#     def contains(self, key: str|int) -> bool:
#         return key in self.value

#     @property
#     def primitive(self):
#         """Python dict로 변환"""
#         return deep_primitive(self.value)

#     @property
#     def string(self):
#         """문자열 표현"""
#         return str({k: v.string for k, v in self.value.items()})

