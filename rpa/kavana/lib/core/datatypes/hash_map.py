from dataclasses import dataclass, field
from typing import Dict

from lib.core.datatypes.kavana_datatype import KavanaDataType

@dataclass
class HashMap(KavanaDataType):
    value: Dict[str, KavanaDataType] = field(default_factory=dict)

    def get(self, key: str) -> KavanaDataType:
        if key not in self.value:
            raise KeyError(f"Key '{key}' not found in HashMap")
        return self.value[key]

    def set(self, key: str, val: KavanaDataType) -> None:
        if not isinstance(key, str):
            raise TypeError("HashMap key must be a string")
        self.value[key] = val

    def remove(self, key: str) -> None:
        if key in self.value:
            del self.value[key]

    def contains(self, key: str) -> bool:
        return key in self.value

    @property
    def primitive(self):
        """Python dict로 변환"""
        return {k: v.primitive for k, v in self.value.items()}

    @property
    def string(self):
        """문자열 표현"""
        return str({k: v.string for k, v in self.value.items()})
