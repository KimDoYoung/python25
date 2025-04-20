from typing import Union, Dict, TYPE_CHECKING
from dataclasses import dataclass, field

from lib.core.datatypes.kavana_datatype import KavanaDataType
from lib.core.datatypes.type_util import deep_primitive, deep_token_string
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
            raise KavanaTypeError("HashMap의 값은  KavanaDataType 인스턴스여야 합니다.")
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
        return deep_token_string(self.value)

    def __str__(self):
        return self.string

    def __repr__(self):
        return f"{{{', '.join(f'{k}: {repr(v)}' for k, v in self.value.items())}}}"
