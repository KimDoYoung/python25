import os
from lib.core.datatypes.kavana_datatype import String
from lib.core.token import Token
from lib.core.token_type import TokenType


class PathFunctions:
    @staticmethod
    def PATH_JOIN(*paths: str) -> Token:
        """여러 경로 요소를 결합하여 반환"""
        joined_path = os.path.join(*paths)
        return Token(data=String(joined_path), type=TokenType.STRING)

    @staticmethod
    def PATH_BASENAME(file_path: str) -> Token:
        """경로에서 파일명만 반환"""
        basename = os.path.basename(file_path)
        return Token(data=String(basename), type=TokenType.STRING)

    @staticmethod
    def PATH_DIRNAME(file_path: str) -> Token:
        """경로에서 디렉토리명만 반환"""
        dirname = os.path.dirname(file_path)
        return Token(data=String(dirname), type=TokenType.STRING)