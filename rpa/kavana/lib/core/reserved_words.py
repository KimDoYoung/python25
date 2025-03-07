class ReservedWords:
    _keywords = {
        "True", "False", "None",
        "INCLUDE", "ENV_LOAD", "MAIN", "END_MAIN",
        "SET","GLOBAL",
        "AND", "OR", "NOT",
        "IF", "ELSE", "ELSEIF", "END_IF", "WHILE", "END_WHILE",
        "FOR", "TO", "STEP", "END_FOR", "FUNCTION", "END_FUNCTION",
        "RETURN", "PRINT"
    }

    @classmethod
    def is_reserved(cls, word: str) -> bool:
        """주어진 단어가 예약어인지 확인"""
        return word.upper() in cls._keywords

    @classmethod
    def add_reserved(cls, word: str):
        """새로운 예약어 추가 (확장 가능)"""
        cls._keywords.add(word.upper())

    @classmethod
    def remove_reserved(cls, word: str):
        """예약어 제거 (필요할 경우)"""
        cls._keywords.discard(word.upper())

    @classmethod
    def get_all_reserved(cls):
        """모든 예약어 리스트 반환"""
        return sorted(cls._keywords)
