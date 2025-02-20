import random
from datetime import datetime

class BuiltinFunctions:
    @staticmethod
    def LENGTH(s: str) -> int:
        return len(s)
    
    @staticmethod
    def SUBSTR(s: str, start: int, length: int) -> str:
        return s[start:start + length]
    
    @staticmethod
    def CURRENT_DATETIME() -> datetime:
        return datetime.now()
    
    @staticmethod
    def RANDOM(min_val: int, max_val: int) -> int:
        return random.randint(min_val, max_val)

    @staticmethod
    def DATE_FORMAT(date_obj: datetime, format_str: str) -> str:
        return date_obj.strftime(format_str)

# 테스트 코드
if __name__ == "__main__":
    print("LENGTH('hello'):", BuiltinFunctions.LENGTH("hello"))
    print("SUBSTR('hello', 1, 3):", BuiltinFunctions.SUBSTR("hello", 1, 3))
    print("CURRENT_DATETIME():", BuiltinFunctions.CURRENT_DATETIME())
    print("RANDOM(1, 10):", BuiltinFunctions.RANDOM(1, 10))
    print("DATE_FORMAT(CURRENT_DATETIME(), '%Y-%m-%d'):", 
          BuiltinFunctions.DATE_FORMAT(BuiltinFunctions.CURRENT_DATETIME(), '%Y-%m-%d'))
