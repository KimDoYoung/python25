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
from lib.core.token import NoneToken, StringToken, Token
from lib.core.token_type import TokenType
from lib.core.token_util import TokenUtil


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
            return TokenUtil.boolean_to_boolean_token(True)  # 성공 시 True 토큰 반환    
        except Exception as e:
            FileFunctions.executor.log_command("ERROR", f"FILE_WRITE: Error writing to file: {file_path}, Error: {e}")  
            return TokenUtil.boolean_to_boolean_token(False)  # 실패 시 False 토큰 반환

    @staticmethod
    def FILE_APPEND(file_path: str, content: str) -> Token:
        """파일 끝에 문자열 추가: 성공 시 True 토큰"""
        try:
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(content)
            return TokenUtil.boolean_to_boolean_token(True)  # 성공 시 True 토큰 반환
        except Exception as e:
            FileFunctions.executor.log_command("ERROR", f"FILE_APPEND: Error appending to file: {file_path}, Error: {e}")  
            
            return TokenUtil.boolean_to_boolean_token(False)

    @staticmethod
    def FILE_EXISTS(file_path: str) -> Token:
        """파일 존재 여부 확인: 존재하면 True, 없으면 False"""
        import os
        exists = os.path.exists(file_path)
        return TokenUtil.boolean_to_boolean_token(exists)  # 존재 여부를 Boolean으로 반환

    @staticmethod
    def FILE_DELETE(file_path: str) -> Token:
        """파일 삭제: 성공 시 True, 실패 시 False"""
        import os
        try:
            os.remove(file_path)
            return TokenUtil.boolean_to_boolean_token(True)  # 성공 시 True 토큰 반환
        except Exception as e:
            FileFunctions.executor.log_command("ERROR", f"FILE_DELETE: Error deleting file: {file_path}, Error: {e}")
            # 파일이 존재하지 않거나 디렉토리인 경우 False 반환
            return TokenUtil.boolean_to_boolean_token(False)  # 실패 시 False 토큰 반환

    @staticmethod
    def FILE_INFO(file_path: str) -> Token:
        """파일 정보 반환 (이름, 크기, 수정 시간)"""
        try:
            file_info = {
                "name": os.path.basename(file_path),
                "size": os.path.getsize(file_path),
                "modified_time": datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),
            }
            hash_map_token = TokenUtil.dict_to_hashmap_token(file_info)  # 딕셔너리를 해시맵 토큰으로 변환
            return hash_map_token
        except Exception as e:
            FileFunctions.executor.log_command("ERROR", f"FILE_INFO: Error getting file info: {file_path}, Error: {e}")
            return NoneToken()  # 오류 시 None 반환

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
        except Exception as e:
            FileFunctions.executor.log_command("ERROR", f"FILE_MOVE: Error moving file: {src} to {dest}, Error: {e}")
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
        except Exception as e:
            FileFunctions.executor.log_command("ERROR", f"FILE_HASH: Error calculating hash for file: {file_path}, Error: {e}")
            return StringToken(data=String(""), type=TokenType.STRING)

    @staticmethod
    def FILE_LINES(file_path: str) -> Token:
        """파일의 각 줄을 리스트로 반환"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = [String(line) for line in f.readlines()]
            return TokenUtil.array_to_array_token(lines)  # 리스트를 Array Token으로 변환
        except Exception as e:
            FileFunctions.executor.log_command("ERROR", f"FILE_LINES: Error reading file lines: {file_path}, Error: {e}")
            return TokenUtil.array_to_array_token([])  # 오류 시 빈 리스트 반환

    @staticmethod
    def FILE_FIND(directory: str, pattern: str) -> Token:
        """특정 디렉토리에서 패턴과 일치하는 파일 찾기"""
        try:
            files = glob.glob(os.path.join(directory, pattern))
            file_info_list = []

            for file_name in files:
                file_path = os.path.join(directory, file_name)
                file_info = {
                    "name": file_name,
                    "is_directory": os.path.isdir(file_path),
                    "size": os.path.getsize(file_path) if os.path.isfile(file_path) else 0,
                    "modified_time": datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),
                }
                file_info_list.append(file_info)               
            return TokenUtil.array_to_array_token(file_info_list)  # 리스트를 Array Token으로 변환
        except Exception as e:
            FileFunctions.executor.log_command("ERROR", f"FILE_FIND: Error finding files in directory: {directory}, Error: {e}")
            return Token(data=Array([]), type=TokenType.ARRAY)


    @staticmethod
    def FILE_TEMP_NAME(suffix: str) -> Token:
        """특정 확장자를 가진 임시 파일 이름 생성"""
        import tempfile
        import os

        try:
            # 임시 디렉토리에서 고유한 파일 이름 생성
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            tmp_file_name = tmp_file.name
            tmp_file.close()  # 파일을 닫고 삭제하지 않도록 설정

            # 반환: 임시 파일 이름을 StringToken으로 반환
            return StringToken(data=String(tmp_file_name), type=TokenType.STRING)
        except Exception as e:
            FileFunctions.executor.log_command("ERROR", f"FILE_TMP_NAME_WITH_SUFFIX: Error creating temp file with suffix '{suffix}', Error: {e}")
            return NoneToken()  # 오류 시 None 반환