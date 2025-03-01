from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union

from lib.core.token_type import TokenType

@dataclass
class Token:
    value: Union[str, int, float, bool, None, datetime]  # ✅ 다양한 타입 지원
    type: TokenType  # ✅ 토큰 유형
    line: Optional[int] = None  # ✅ 기본값을 None으로 설정
    column: Optional[int] = None  # ✅ 기본값을 None으로 설정

    def __repr__(self):
        """디버깅을 위한 문자열 표현"""
        return f"Token(value={self.value}, type={self.type}, line={self.line}, column={self.column})"
