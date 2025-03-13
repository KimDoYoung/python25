import os

from lib.core.datatypes.kavana_datatype import Boolean, String
from lib.core.token import Token
from lib.core.token_type import TokenType


class FileDirFunctions:
    # @staticmethod
    # def FILES_IN_DIR(directory):
    #     ''' 파일들 리스트 '''
    #     return [f for f in os.listdir(directory) if os.path.isfile(os.path)]
    @staticmethod
    def FILE_READ(file_path: str) -> Token:
        """파일 읽기"""
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"파일이 존재하지 않거나 디렉터리입니다: {file_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        return Token(data=String(content), type=TokenType.STRING)

    @staticmethod
    def FILE_WRITE(file_path: str, content: str) -> Token:
        """파일 쓰기"""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:            
            return Token(data=Boolean(False), type=TokenType.BOOLEAN)

        return Token(data=Boolean(True), type=TokenType.BOOLEAN)
