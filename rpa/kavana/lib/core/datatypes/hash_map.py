from typing import Union, Dict, TYPE_CHECKING
from dataclasses import dataclass, field
from typing import Dict, Union

from lib.core.datatypes.kavana_datatype import KavanaDataType
from lib.core.exceptions.kavana_exception import KavanaKeyError


if TYPE_CHECKING:
    from lib.core.token import Token  # 타입 검사용

@dataclass
class HashMap(KavanaDataType):
    value: Dict[Union[str, int], KavanaDataType] = field(default_factory=dict)

    def get(self, key: str | int) -> 'Token':
        if key not in self.value:
            raise KavanaKeyError(f"키 '{key}'를 발견할 수 없습니다.")
        return self.value[key]

    def set(self, key: Union[str, int], val: 'Token') -> None:
        if not isinstance(val, Token):
            raise KavanaTypeError("HashMap의 값은 토큰이어야 합니다.")
        self.value[key] = val

    def remove(self, key: str|int) -> None:
        if key in self.value:
            del self.value[key]

    def contains(self, key: str|int) -> bool:
        return key in self.value

    @property
    def primitive(self):
        """Python dict로 변환"""
        return {k: v.primitive for k, v in self.value.items()}

    @property
    def string(self):
        """문자열 표현"""
        return str({k: v.string for k, v in self.value.items()})
