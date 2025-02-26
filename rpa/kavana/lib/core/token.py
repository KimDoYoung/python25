from dataclasses import dataclass

from lib.core.datatypes.token_type import TokenType

@dataclass
class Token:
    value: str  # 토큰 값 (예: "PRINT", "IF", "123")
    type: TokenType  # 토큰 유형
    line: int = 0  # 해당 토큰이 위치한 줄 번호
    column: int = 0  # 해당 토큰이 위치한 컬럼 번호
