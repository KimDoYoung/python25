from datetime import datetime
import os
from pathlib import Path
import tempfile
from lib.core.datatypes.kavana_datatype import Boolean
from lib.core.datatypes.array import Array
from lib.core.token import Token, TokenType,  String
from lib.core.token_util import TokenUtil

class DirFunctions:
    ''' 디렉토리 관련 내장 함수들 '''
    executor = None  # ✅ 클래스 변수로 executor 저장

    @staticmethod
    def set_executor(executor_instance):
        DirFunctions.executor = executor_instance

    @staticmethod
    def DIR(name: str) -> Token:
        """디렉토리 경로 반환"""
        name = name.lower()
        
        if name in ("~", "home","사용자홈","사용자","userhome"):
            directory = os.path.expanduser("~")
        elif name == "Pictures" or name == "사진":
            directory = str(Path.home() / "Pictures")
        elif name == "temp" or name == "임시":
            directory = tempfile.gettempdir()
        elif name == "desktop" or name == "바탕화면":
            directory = str(Path.home() / "Desktop")
        elif name == "documents" or name == "문서":
            directory = str(Path.home() / "Documents")
        elif name == "downloads" or name == "다운로드":
            directory = str(Path.home() / "Downloads")
        elif name == "appdata" or name == "앱데이터":
            directory = os.environ.get("APPDATA", "")
        elif name == "cwd" or name == "current" or name == "현재":
            directory = os.getcwd()
        else:
            # 기본은 직접 지정한 경로로 취급
            directory = os.path.abspath(os.path.expanduser(name))        
        try:
            if os.path.isdir(directory):
                return Token(data=String(directory), type=TokenType.STRING)
            else:
                DirFunctions.executor.log_command("ERROR", f"DIR: {directory} is not a directory.")
                return Token(data=String(""), type=TokenType.STRING)
        except Exception as e:
            DirFunctions.executor.log_command("ERROR", f"DIR: Error getting directory: {e}")
            return Token(data=String(""), type=TokenType.STRING)

    @staticmethod
    def DIR_LIST(directory: str) -> Token:
        """특정 디렉토리의 파일 목록 반환"""
        try:
            files = os.listdir(directory)
            file_info_list = []

            for file_name in files:
                file_path = os.path.join(directory, file_name)
                file_info = {
                    "name": file_name,
                    "is_directory": os.path.isdir(file_path),
                    "size": os.path.getsize(file_path) if os.path.isfile(file_path) else 0,
                    "modified_time": datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S'),
                }
                file_info_token = TokenUtil.dict_to_hashmap_token(file_info)
                file_info_list.append(file_info_token)            
            return TokenUtil.array_to_array_token(file_info_list)  
        except Exception as e:
            DirFunctions.executor.log_command("ERROR", f"DIR_LIST: Error listing directory: {e}") 
            return Token(data=Array([]), type=TokenType.ARRAY)  # 오류 시 빈 리스트 반환

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
        except Exception as e:
            DirFunctions.executor.log_command("ERROR", f"DIR_CREATE : Error creating directory: {directory}")
            return Token(data=Boolean(False), type=TokenType.BOOLEAN)

    @staticmethod
    def DIR_DELETE(directory: str) -> Token:
        """디렉토리 삭제 (비어 있어야 함)"""
        try:
            os.rmdir(directory)
            return Token(data=Boolean(True), type=TokenType.BOOLEAN)
        except Exception as e:
            DirFunctions.executor.log_command("ERROR", f"DIR_DELETE : Error deleting directory: {directory}")
            return Token(data=Boolean(False), type=TokenType.BOOLEAN)
        
    @staticmethod
    def DIR_RENAME(old_directory: str, new_directory: str) -> Token:
        """디렉토리 이름 변경"""
        try:
            os.rename(old_directory, new_directory)
            return Token(data=Boolean(True), type=TokenType.BOOLEAN)
        except Exception as e:
            DirFunctions.executor.log_command("ERROR", f"DIR_RENAME : Error renaming directory from {old_directory} to {new_directory}")
            return Token(data=Boolean(False), type=TokenType.BOOLEAN)
