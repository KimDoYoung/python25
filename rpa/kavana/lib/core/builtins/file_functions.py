from datetime import datetime
import os

from lib.core.datatypes.kavana_datatype import Boolean, Integer, String
from lib.core.exceptions.kavana_exception import KavanaFileNotFoundError
from lib.core.token import Token
from lib.core.token_type import TokenType


class FileFunctions:
    # @staticmethod
    # def FILES_IN_DIR(directory):
    #     ''' 파일들 리스트 '''
    #     return [f for f in os.listdir(directory) if os.path.isfile(os.path)]
    @staticmethod
    def FILE_READ(file_path: str) -> Token:
        """파일 읽기, String Token 반환"""
        if not os.path.isfile(file_path):
            raise KavanaFileNotFoundError(f"파일이 존재하지 않거나 디렉터리입니다: {file_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        return Token(data=String(content), type=TokenType.STRING)

    @staticmethod
    def FILE_WRITE(file_path: str, content: str) -> Token:
        """파일 쓰기: 성공시 True토큰"""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception as e:            
            return Token(data=Boolean(False), type=TokenType.BOOLEAN)

        return Token(data=Boolean(True), type=TokenType.BOOLEAN)

    @staticmethod
    def FILE_APPEND(file_path: str, content: str) -> Token:
        """파일 끝에 문자열 추가: 성공 시 True 토큰"""
        try:
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(content)
        except Exception:
            return Token(data=Boolean(False), type=TokenType.BOOLEAN)

        return Token(data=Boolean(True), type=TokenType.BOOLEAN)

    @staticmethod
    def FILE_EXISTS(file_path: str) -> Token:
        """파일 존재 여부 확인: 존재하면 True, 없으면 False"""
        import os
        exists = os.path.exists(file_path)
        return Token(data=Boolean(exists), type=TokenType.BOOLEAN)

    @staticmethod
    def FILE_DELETE(file_path: str) -> Token:
        """파일 삭제: 성공 시 True, 실패 시 False"""
        import os
        try:
            os.remove(file_path)
        except Exception:
            return Token(data=Boolean(False), type=TokenType.BOOLEAN)

        return Token(data=Boolean(True), type=TokenType.BOOLEAN)


    @staticmethod
    def FILE_SIZE(file_path: str) -> Token:
        """파일 크기 반환 (바이트)"""
        try:
            size = os.path.getsize(file_path)
            return Token(data=Integer(size), type=TokenType.INTEGER)
        except Exception:
            return Token(data=Integer(-1), type=TokenType.NUMBER)  # 오류 시 -1 반환

    @staticmethod
    def FILE_MODIFIED_TIME(file_path: str) -> Token:
        """파일 최종 수정 시간 반환 (YYYY-MM-DD HH:MM:SS 형식)"""
        try:
            timestamp = os.path.getmtime(file_path)
            mod_time = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
            return Token(data=String(mod_time), type=TokenType.STRING)
        except Exception:
            return Token(data=String(""), type=TokenType.STRING)  # 오류 시 빈 문자열 반환

    @staticmethod
    def FILE_TYPE(file_path: str) -> Token:
        """파일 유형 반환 (file / directory / none)"""
        if os.path.isfile(file_path):
            return Token(data=String("file"), type=TokenType.STRING)
        elif os.path.isdir(file_path):
            return Token(data=String("directory"), type=TokenType.STRING)
        return Token(data=String("none"), type=TokenType.STRING)  # 존재하지 않으면 "none"

