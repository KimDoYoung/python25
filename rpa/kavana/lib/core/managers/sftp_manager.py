import os
import glob
import paramiko
from base_manager import BaseManager

class SftpManager(BaseManager):
    def __init__(self, **kwargs):
        super().__init__(kwargs.get("executor", None))
        self.host = kwargs.get("host", "127.0.0.1")
        self.port = kwargs.get("port", 22)
        self.user = kwargs.get("user", "myid")
        self.password = kwargs.get("password", "mypassword")
        self.key_file = kwargs.get("key_file")  # 선택적 키 파일 경로
        
        self.remote_dir = kwargs.get("remote_dir", "/home/files")
        self.timeout = kwargs.get("timeout", 10)
        self.overwrite = kwargs.get("overwrite", False)

        self._files = []
        self.files = kwargs.get("files", [])

        self.ssh = None
        self.sftp = None

    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, value):
        if not isinstance(value, list):
            raise ValueError("files는 리스트여야 합니다.")
        expanded = []
        for item in value:
            matched = glob.glob(item)
            if matched:
                expanded.extend(matched)
            else:
                expanded.append(item)
        self._files = expanded

    def _ensure_remote_dir(self, path):
        """remote_dir이 없으면 생성하고 순차적으로 이동"""
        if not path or path == "/":
            return

        parts = path.strip("/").split("/")
        for part in parts:
            try:
                self.sftp.chdir(part)
            except IOError:
                self.sftp.mkdir(part)
                self.sftp.chdir(part)
                self.log("INFO", f"디렉토리 생성: {part}")

    def connect(self):
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # 인증 방식 결정: password 또는 key_file
            if self.password:
                self.ssh.connect(
                    hostname=self.host,
                    port=self.port,
                    username=self.user,
                    password=self.password,
                    timeout=self.timeout
                )
            elif hasattr(self, "key_file") and self.key_file:
                pkey = paramiko.RSAKey.from_private_key_file(self.key_file)
                self.ssh.connect(
                    hostname=self.host,
                    port=self.port,
                    username=self.user,
                    pkey=pkey,
                    timeout=self.timeout
                )
            else:
                self.raise_error("password 또는 key_file 중 하나는 반드시 있어야 합니다.")

            self.sftp = self.ssh.open_sftp()
            self.sftp.get_channel().settimeout(self.timeout)  # ✅ socket 수준 timeout 적용

            # remote_dir이 없으면 생성하고 이동
            self._ensure_remote_dir(self.remote_dir)

            self.log("INFO", f"SFTP 연결 성공: {self.host}:{self.port}")
        except Exception as e:
            self.raise_error(f"SFTP 연결 실패: {e}")


    def close(self):
        if self.sftp:
            self.sftp.close()
        if self.ssh:
            self.ssh.close()
        self.log("INFO", "SFTP 연결 종료")

    def upload(self):
        if not self.files:
            self.raise_error("업로드할 파일이 없습니다.")
        try:
            self.connect()
            for filepath in self.files:
                if not os.path.isfile(filepath):
                    self.log("WARNING", f"파일 없음: {filepath}")
                    continue
                filename = os.path.basename(filepath)
                self.sftp.put(filepath, f"{self.remote_dir}/{filename}")
                self.log("INFO", f"업로드 완료: {filename}")
        finally:
            self.close()

    def download(self):
        if not self.files:
            self.raise_error("다운로드할 파일이 없습니다.")
        try:
            self.connect()
            for filepath in self.files:
                filename = os.path.basename(filepath)
                if os.path.exists(filepath) and not self.overwrite:
                    self.log("WARNING", f"파일 존재(무시됨): {filepath}")
                    continue
                self.sftp.get(f"{self.remote_dir}/{filename}", filepath)
                self.log("INFO", f"다운로드 완료: {filename}")
        finally:
            self.close()

    def delete(self):
        if not self.files:
            self.raise_error("삭제할 파일이 없습니다.")
        try:
            self.connect()
            for filepath in self.files:
                filename = os.path.basename(filepath)
                try:
                    self.sftp.remove(f"{self.remote_dir}/{filename}")
                    self.log("INFO", f"삭제 완료: {filename}")
                except IOError as e:
                    self.log("ERROR", f"삭제 실패: {filename} ({e})")
        finally:
            self.close()

    def list(self):
        try:
            self.connect()
            files = self.sftp.listdir(self.remote_dir)
            self.log("INFO", "디렉토리 목록:\n" + "\n".join(files))
            return files
        finally:
            self.close()

    def mkdir(self):
        try:
            self.connect()
            self.sftp.mkdir(self.remote_dir)
            self.log("INFO", f"디렉토리 생성: {self.remote_dir}")
        finally:
            self.close()

    def rmdir(self):
        try:
            self.connect()
            self.sftp.rmdir(self.remote_dir)
            self.log("INFO", f"디렉토리 삭제: {self.remote_dir}")
        finally:
            self.close()

    def execute(self, command):
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
