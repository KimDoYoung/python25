import os
from lib.core.datatypes.kavana_datatype import String
from lib.core.token import StringToken, Token
from lib.core.token_type import TokenType

class PathFunctions:
    ''' 경로 관련 내장 함수들 '''
    executor = None  # ✅ 클래스 변수로 executor 저장

    @staticmethod
    def set_executor(executor_instance):
        PathFunctions.executor = executor_instance
        
    @staticmethod
    def PATH_JOIN(*paths: str) -> Token:
        """여러 경로 요소를 결합하여 반환"""
        joined_path = os.path.join(*paths)
        return StringToken(data=String(joined_path), type=TokenType.STRING)

    @staticmethod
    def PATH_BASENAME(file_path: str) -> Token:
        """경로에서 파일명만 반환"""
        basename = os.path.basename(file_path)
        return StringToken(data=String(basename), type=TokenType.STRING)

    @staticmethod
    def PATH_DIRNAME(file_path: str) -> Token:
        """경로에서 디렉토리명만 반환"""
        dirname = os.path.dirname(file_path)
        return StringToken(data=String(dirname), type=TokenType.STRING)