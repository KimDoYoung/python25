import datetime
import fnmatch
import glob
import os
from ftplib import FTP, error_perm
from base_manager import BaseManager
from lib.core.exceptions.kavana_exception import KavanaValueError

class FtpManager(BaseManager):
    def __init__(self, **kwargs):
        super().__init__(kwargs.get("executor", None))
        self.host = kwargs.get("host", "127.0.0.1")
        self.port = kwargs.get("port", 21)
        self.user = kwargs.get("user", None)
        self.password = kwargs.get("password", None) 
        self.remote_dir = kwargs.get("remote_dir", "/home/files")
        self.files = kwargs.get("files", [])  # ✅ 배열로 변경
        self.passive_mode = kwargs.get("passive_mode", True)
        self.timeout = kwargs.get("timeout", 10)
        self.overwrite = kwargs.get("overwrite", False)

        self.ftp = None

    def connect(self):
        try:
            self.ftp = FTP()
            self.ftp.connect(self.host, self.port, timeout=self.timeout)
            self.ftp.login(self.user, self.password)
            self.ftp.set_pasv(self.passive_mode)

            # ✅ 모든 통신에 타임아웃 적용
            self.ftp.sock.settimeout(self.timeout)

            self._ensure_remote_dir(self.remote_dir)

            self.log("INFO", f"Connected to FTP: {self.host}:{self.port}")
        except Exception as e:
            self.raise_error(f"{self.host} FTP 연결 실패: {e}")

    def close(self):
        if self.ftp:
            self.ftp.quit()
            self.log("INFO", f"{self.host} FTP 연결 종료")

    def _ensure_remote_dir(self, path):
        dirs = path.strip("/").split("/")
        current = ""
        for d in dirs:
            current += f"/{d}"
            try:
                self.ftp.cwd(current)
            except error_perm:
                self.ftp.mkd(current)
                self.ftp.cwd(current)

    def upload(self):
        if not self.files:
            self.raise_error("업로드할 파일 목록이 없습니다.")
        try:
            self.connect()

            for filepath in self.files:
                if not os.path.isfile(filepath):
                    self.log("WARNING", f"파일 없음: {filepath}")
                    continue

                filename = os.path.basename(filepath)
                if filename in self.ftp.nlst() and not self.overwrite:
                    self.log("INFO", f"파일 존재 - 건너뜀: {filename}")
                    continue

                with open(filepath, "rb") as f:
                    self.ftp.storbinary(f"STOR {filename}", f)
                    self.log("INFO", f"업로드 완료: {filename}")
        finally:
            self.close()

    def download(self):
        if not self.files:
            self.raise_error("다운로드할 파일 목록이 없습니다.")
        try:
            self.connect()
            for filepath in self.files:
                filename = os.path.basename(filepath)
                if os.path.exists(filepath) and not self.overwrite:
                    self.log("WARNING", f"파일 존재 (무시됨): {filepath}")
                    continue
                with open(filepath, "wb") as f:
                    self.ftp.retrbinary(f"RETR {filename}", f.write)
                    self.log("INFO", f"다운로드 완료: {filename}")
        finally:
            self.close()

    def delete(self):
        if not self.files:
            self.raise_error("삭제할 파일 목록이 없습니다.")
        try:
            self.connect()
            for filename in self.files:
                filename = os.path.basename(filename)
                try:
                    self.ftp.delete(filename)
                    self.log("INFO", f"삭제 완료: {filename}")
                except error_perm as e:
                    self.log("ERROR", f"삭제 실패: {filename} ({e})")
        finally:
            self.close()


    def list(self, pattern=None):
        try:
            self.connect()
            files = self.ftp.nlst()

            if pattern:
                files = fnmatch.filter(files, pattern)

            file_infos = []

            for filename in files:
                try:
                    size = self.ftp.size(filename)
                    mdtm_raw = self.ftp.sendcmd(f"MDTM {filename}")
                    mdtm_str = mdtm_raw[4:]  # "213YYYYMMDDhhmmss" → "YYYYMMDDhhmmss"
                    mod_time = datetime.strptime(mdtm_str, "%Y%m%d%H%M%S")
                    file_infos.append({
                        "name": filename,
                        "size": size,
                        "modified": mod_time.strftime("%Y-%m-%d %H:%M:%S")
                    })
                except Exception as e:
                    self.log("WARNING", f"{filename} 메타데이터 조회 실패: {e}")
                    file_infos.append({
                        "name": filename,
                        "size": None,
                        "modified": None
                    })

            self.log("INFO", f"{len(file_infos)}개 파일 정보 조회 완료")
            return file_infos

        finally:
            self.close()


    def mkdir(self):
        try:
            self.connect()
            self.ftp.mkd(self.remote_dir)
            self.log("INFO", f"디렉토리 생성: {self.remote_dir}")
        finally:
            self.close()

    def rmdir(self):
        try:
            self.connect()
            self.ftp.rmd(self.remote_dir)
            self.log("INFO", f"디렉토리 삭제: {self.remote_dir}")
        finally:
            self.close()

    def execute(self, command):
        """명령어에 따라 실행"""
        commands = {
            "upload": self.upload,
            "download": self.download,
            "list": self.list,
            "delete": self.delete,
            "mkdir": self.mkdir,
            "rmdir": self.rmdir
        }
        func = commands.get(command)
        if not func:
            self.raise_error(f"지원하지 않는 명령어입니다: {command}")
        func()

    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, value):
        if not isinstance(value, list):
            self.raise_error("files는 리스트여야 합니다.")

        expanded = []
        for item in value:
            matched = glob.glob(item)  # ✅ 패턴 확장
            if matched:
                expanded.extend(matched)
            else:
                expanded.append(item)  # 매칭 없으면 그대로 추가 (예: 서버 파일명)

        self._files = expanded