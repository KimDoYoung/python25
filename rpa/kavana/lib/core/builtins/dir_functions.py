import os
from lib.core.token import Token, TokenType, Boolean, String, List

class DirFunctions:
    @staticmethod
    def DIR_LIST(directory: str) -> Token:
        """특정 디렉토리의 파일 목록 반환"""
        try:
            files = os.listdir(directory)
            return Token(data=List([String(f) for f in files]), type=TokenType.LIST)
        except Exception:
            return Token(data=List([]), type=TokenType.LIST)  # 오류 시 빈 리스트 반환

    @staticmethod
    def DIR_EXISTS(directory: str) -> Token:
        """디렉토리 존재 여부 확인"""
        exists = os.path.isdir(directory)
        return Token(data=Boolean(exists), type=TokenType.BOOLEAN)

    @staticmethod
    def DIR_CREATE(directory: str) -> Token:
        """새 디렉토리 생성"""
        try:
            os.makedirs(directory, exist_ok=True)
            return Token(data=Boolean(True), type=TokenType.BOOLEAN)
        except Exception:
            return Token(data=Boolean(False), type=TokenType.BOOLEAN)

    @staticmethod
    def DIR_DELETE(directory: str) -> Token:
        """디렉토리 삭제 (비어 있어야 함)"""
        try:
            os.rmdir(directory)
            return Token(data=Boolean(True), type=TokenType.BOOLEAN)
        except Exception:
            return Token(data=Boolean(False), type=TokenType.BOOLEAN)
