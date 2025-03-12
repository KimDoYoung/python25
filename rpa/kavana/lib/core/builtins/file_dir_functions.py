import os

from lib.core.datatypes.kavana_datatype import String
from lib.core.token import Token
from lib.core.token_type import TokenType


class FileDirFunctions:
    # @staticmethod
    # def FILES_IN_DIR(directory):
    #     ''' 파일들 리스트 '''
    #     return [f for f in os.listdir(directory) if os.path.isfile(os.path)]
    @staticmethod
    def FILE_READ(file_path: str) -> Token:
        ''' 파일 읽기 '''
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"파일이 아닙니다: {file_path}")
        
        result = ""
        with open(file_path, "r", encoding="utf-8") as f:
            result = f.read()
        return Token(data=String(result), type=TokenType.STRING)
        