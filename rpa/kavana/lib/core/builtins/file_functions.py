from datetime import datetime
import glob
import hashlib
import os
import shutil
from typing import List

from lib.core.datatypes.kavana_datatype import Boolean, Integer, String
from lib.core.datatypes.array import Array
from lib.core.datatypes.ymd_time import YmdTime
from lib.core.exceptions.kavana_exception import KavanaException, KavanaFileNotFoundError
from lib.core.token import StringToken, Token
from lib.core.token_type import TokenType


class FileFunctions:
    ''' 파일 관련 내장 함수들 '''

    executor = None  # ✅ 클래스 변수로 executor 저장

    @staticmethod
    def set_executor(executor_instance):
        FileFunctions.executor = executor_instance

    @staticmethod
    def FILE_READ(file_path: str) -> Token:
        """파일 읽기, String Token 반환"""
        if not os.path.isfile(file_path):
            raise KavanaFileNotFoundError(f"파일이 존재하지 않거나 디렉터리입니다: {file_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        return StringToken(data=String(content), type=TokenType.STRING)

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
            return Token(data=Integer(-1), type=TokenType.INTEGER)  # 오류 시 -1 반환

    @staticmethod
    def FILE_MODIFIED_TIME(file_path: str) -> Token:
        """파일 최종 수정 시간 반환 (YYYY-MM-DD HH:MM:SS 형식)"""
        try:
            timestamp = os.path.getmtime(file_path)
            mod_time = datetime.fromtimestamp(timestamp)
            return Token(data=YmdTime.from_datetime(mod_time), type=TokenType.YMDTIME)
        except Exception:
            raise KavanaException(f"파일의 최종 변경시각을 가져 오지 못했습니다: {file_path}")

    @staticmethod
    def FILE_TYPE(file_path: str) -> Token:
        """파일 유형 반환 (file / directory / none)"""
        if os.path.isfile(file_path):
            return StringToken(data=String("file"), type=TokenType.STRING)
        elif os.path.isdir(file_path):
            return StringToken(data=String("directory"), type=TokenType.STRING)
        return StringToken(data=String("none"), type=TokenType.STRING)  # 존재하지 않으면 "none"


    @staticmethod
    def FILE_COPY(src: str, dest: str) -> Token:
        """파일 복사"""
        try:
            shutil.copy2(src, dest)  # 메타데이터까지 복사
            return Token(data=Boolean(True), type=TokenType.BOOLEAN)
        except Exception:
            return Token(data=Boolean(False), type=TokenType.BOOLEAN)

    @staticmethod
    def FILE_MOVE(src: str, dest: str) -> Token:
        """파일 이동/이름 변경"""
        try:
            shutil.move(src, dest)
            return Token(data=Boolean(True), type=TokenType.BOOLEAN)
        except Exception:
            return Token(data=Boolean(False), type=TokenType.BOOLEAN)

    @staticmethod
    def FILE_HASH(file_path: str, algorithm: str) -> Token:
        """파일의 해시 값 계산 (MD5, SHA256)"""
        hash_func = {
            "md5": hashlib.md5,
            "sha256": hashlib.sha256
        }.get(algorithm.lower())

        if hash_func is None:
            return StringToken(data=String(""), type=TokenType.STRING)  # 지원되지 않는 알고리즘

        try:
            with open(file_path, "rb") as f:
                hasher = hash_func()
                while chunk := f.read(8192):
                    hasher.update(chunk)
            return StringToken(data=String(hasher.hexdigest()), type=TokenType.STRING)
        except Exception:
            return StringToken(data=String(""), type=TokenType.STRING)

    @staticmethod
    def FILE_LINES(file_path: str) -> Token:
        """파일의 각 줄을 리스트로 반환"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = [String(line.strip()) for line in f.readlines()]
            return Token(data=Array(lines), type=TokenType.ARRAY)
        except Exception:
            return Token(data=Array([]), type=TokenType.ARRAY)

    @staticmethod
    def FILE_FIND(directory: str, pattern: str) -> Token:
        """특정 디렉토리에서 패턴과 일치하는 파일 찾기"""
        try:
            files = glob.glob(os.path.join(directory, pattern))
            return Token(data=Array([String(os.path.basename(f)) for f in files]), type=TokenType.ARRAY)
        except Exception:
            return Token(data=Array([]), type=TokenType.ARRAY)

