from typing import Optional
from lib.core.exceptions.kavana_exception import KavanaValueError
from lib.core.token import Token


class ConstantRegistry:
    """✅ 글로벌 상수를 저장하는 레지스트리"""
    _constants = {}

    @classmethod
    def define_constant(cls, name: str, value:Token):
        """✅ `CONST` 정의 (이미 존재하면 오류 발생)"""
        name = name.upper()
        if name in cls._constants:
            # raise KavanaValueError(f"상수 {name}은 이미 정의되어 있습니다.")
            return
        cls._constants[name] = value

    @classmethod
    def get(cls, name: str) -> Optional[Token]:
        """✅ 상수 값 가져오기 (없으면 None)"""
        return cls._constants.get(name)

    @classmethod
    def is_constant(cls, name: str):
        """✅ 상수 여부 확인"""
        return name.upper() in cls._constants
