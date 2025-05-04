from datetime import datetime
import fnmatch
import os
import glob
import paramiko
from lib.core.managers.base_manager import BaseManager

class SftpManager(BaseManager):
    def __init__(self, **kwargs):
        super().__init__(kwargs.get("executor", None))
        self.command = kwargs.get("command")
        self.options = kwargs

        self.ssh = None
        self.sftp = None

        if not self.command:
            self.raise_error("command는 필수입니다.")

    def execute(self):
        commands = {
            "upload": self.upload,
            "download": self.download,
            "list": self.list,
            "delete": self.delete,
            "mkdir": self.mkdir,
            "rmdir": self.rmdir
        }
        func = commands.get(self.command)
        if not func:
            self.raise_error(f"지원하지 않는 명령어입니다: {self.command}")
        return func()

    def connect(self):
        try:
            host = self.options.get("host", "127.0.0.1")
            port = self.options.get("port", 22)
            user = self.options.get("user")
            password = self.options.get("password")
            key_file = self.options.get("key_file")
            timeout = self.options.get("timeout", 10)

            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if password:
                self.ssh.connect(hostname=host, port=port, username=user, password=password, timeout=timeout)
            elif key_file:
                pkey = paramiko.RSAKey.from_private_key_file(key_file)
                self.ssh.connect(hostname=host, port=port, username=user, pkey=pkey, timeout=timeout)
            else:
                self.raise_error("password 또는 key_file 중 하나는 반드시 있어야 합니다.")

            self.sftp = self.ssh.open_sftp()
            self.sftp.get_channel().settimeout(timeout)

            self.log("INFO", f"SFTP 연결 성공: {host}:{port}")
        except Exception as e:
            self.raise_error(f"SFTP 연결 실패: {e}")

    def close(self):
        if self.sftp:
            self.sftp.close()
        if self.ssh:
            self.ssh.close()
        self.log("INFO", "SFTP 연결 종료")

    def _ensure_remote_dir(self, path):
        if not path or path == "/":
            return
        for part in path.strip("/").split("/"):
            try:
                self.sftp.chdir(part)
            except IOError:
                self.sftp.mkdir(part)
                self.sftp.chdir(part)
                self.log("INFO", f"디렉토리 생성: {part}")

    def _ensure_local_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
            self.log("INFO", f"로컬 디렉토리 생성: {path}")
        os.chdir(path)
        self.log("INFO", f"로컬 디렉토리 이동: {path}")

    def _expand_local_file_patterns(self, patterns):
        expanded = []
        for p in patterns:
            if '*' in p or '?' in p:
                matched = glob.glob(p)
                if not matched:
                    self.log("WARN", f"매칭되는 파일 없음: {p}")
                expanded.extend(matched)
            else:
                expanded.append(p)
        return expanded

    def _expand_remote_file_patterns(self, patterns):
        matched = []
        try:
            remote_files = self.sftp.listdir(self.options.get("remote_dir"))
        except Exception as e:
            self.raise_error(f"원격 디렉토리 목록 가져오기 실패: {e}")

        for pattern in patterns:
            match = fnmatch.filter(remote_files, pattern)
            if not match:
                self.log("WARN", f"매칭되는 원격 파일 없음: {pattern}")
            matched.extend(match)

        return matched

    def upload(self):
        files = self.options.get("files", [])
        local_dir = self.options.get("local_dir")
        remote_dir = self.options.get("remote_dir")

        if not files:
            self.raise_error("SFTP 업로드할 파일이 없습니다.")

        try:
            self.connect()
            self._ensure_remote_dir(remote_dir)
            self._ensure_local_dir(local_dir)
            expanded = self._expand_local_file_patterns(files)

            if not expanded:
                self.raise_error("SFTP 업로드할 파일이 없습니다.")

            for filepath in expanded:
                if not os.path.isfile(filepath):
                    self.log("WARN", f"파일 없음: {filepath}")
                    continue
                filename = os.path.basename(filepath)
                self.sftp.put(os.path.join(local_dir, filepath), f"{remote_dir}/{filename}")
                self.log("INFO", f"SFTP 업로드 완료: {filename}")
        finally:
            self.close()

    def download(self):
        files = self.options.get("files", [])
        local_dir = self.options.get("local_dir")
        remote_dir = self.options.get("remote_dir")
        overwrite = self.options.get("overwrite", True)

        if not files:
            self.raise_error("SFTP 다운로드할 파일이 없습니다.")

        try:
            self.connect()
            self._ensure_local_dir(local_dir)
            expanded = self._expand_remote_file_patterns(files)

            if not expanded:
                self.raise_error("SFTP 다운로드할 파일이 없습니다.")

            for remote_filename in expanded:
                local_filename = os.path.join(local_dir, os.path.basename(remote_filename))
                if os.path.exists(local_filename) and not overwrite:
                    self.log("WARN", f"이미 존재(무시됨): {local_filename}")
                    continue
                self.sftp.get(f"{remote_dir}/{remote_filename}", local_filename)
                self.log("INFO", f"SFTP 다운로드 완료: {remote_filename} -> {local_filename}")
        finally:
            self.close()

    def delete(self):
        files = self.options.get("files", [])
        remote_dir = self.options.get("remote_dir")

        if not files:
            self.raise_error("삭제할 파일이 없습니다.")

        try:
            self.connect()
            for filepath in files:
                filename = os.path.basename(filepath)
                try:
                    self.sftp.remove(f"{remote_dir}/{filename}")
                    self.log("INFO", f"삭제 완료: {filename}")
                except IOError as e:
                    self.log("ERROR", f"삭제 실패: {filename} ({e})")
        finally:
            self.close()

    def list(self):
        remote_dir = self.options.get("remote_dir")
        pattern = self.options.get("pattern", "*")

        try:
            self.connect()
            files = self.sftp.listdir(remote_dir)
            files = fnmatch.filter(files, pattern) if pattern else files

            file_infos = []
            for filename in files:
                try:
                    stat = self.sftp.stat(f"{remote_dir.rstrip('/')}/{filename}")
                    file_infos.append({
                        "name": filename,
                        "size": stat.st_size,
                        "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                    })
                except Exception as e:
                    self.log("WARN", f"{filename} 메타데이터 조회 실패: {e}")
                    file_infos.append({"name": filename, "size": None, "modified": None})

            self.log("INFO", f"{len(file_infos)}개 파일 정보 조회 완료")
            return file_infos
        finally:
            self.close()

    def mkdir(self):
        remote_dir = self.options.get("remote_dir")
        try:
            self.connect()
            self.sftp.mkdir(remote_dir)
            self.log("INFO", f"디렉토리 생성: {remote_dir}")
        finally:
            self.close()

    def rmdir(self):
        remote_dir = self.options.get("remote_dir")
        try:
            self.connect()
            self.sftp.rmdir(remote_dir)
            self.log("INFO", f"디렉토리 삭제: {remote_dir}")
        finally:
            self.close()

# from datetime import datetime
# import fnmatch
# import os
# import glob
# import paramiko
# from lib.core.managers.base_manager import BaseManager

# class SftpManager(BaseManager):
#     def __init__(self, **kwargs):
#         super().__init__(kwargs.get("executor", None))
#         self.host = kwargs.get("host", "127.0.0.1")
#         self.port = kwargs.get("port", 22)
#         self.user = kwargs.get("user")
#         self.password = kwargs.get("password")
#         self.key_file = kwargs.get("key_file")  # 선택적 키 파일 경로
        
#         self.remote_dir = kwargs.get("remote_dir")
#         self.local_dir = kwargs.get("local_dir")
#         self.timeout = kwargs.get("timeout", 10)
#         self.overwrite = kwargs.get("overwrite", True)

#         self.files = kwargs.get("files", [])
#         self.pattern = kwargs.get("pattern", "*")

#         self.ssh = None
#         self.sftp = None

#     def execute(self, command):
#         commands = {
#             "upload": self.upload,
#             "download": self.download,
#             "list": self.list,
#             "delete": self.delete,
#             "mkdir": self.mkdir,
#             "rmdir": self.rmdir
#         }
#         func = commands.get(command)
#         if not func:
#             self.raise_error(f"지원하지 않는 명령어입니다: {command}")
#         func()

#     def _ensure_remote_dir(self, path):
#         """remote_dir이 없으면 생성하고 순차적으로 이동"""
#         if not path or path == "/":
#             return

#         parts = path.strip("/").split("/")
#         for part in parts:
#             try:
#                 self.sftp.chdir(part)
#             except IOError:
#                 self.sftp.mkdir(part)
#                 self.sftp.chdir(part)
#                 self.log("INFO", f"디렉토리 생성: {part}")

#     def _ensure_local_dir(self, path):
#         """필요 시 로컬 디렉토리를 생성하고 이동"""
#         if not os.path.exists(path):
#             os.makedirs(path)
#             self.log("INFO", f"로컬 디렉토리 생성: {path}")
#         os.chdir(path)
#         self.log("INFO", f"로컬 디렉토리 이동: {path}")

#     def _expand_local_file_patterns(self, file_patterns):
#         """
#         파일 패턴 목록에서 와일드카드를 확장하여 실제 파일 목록을 반환합니다.
        
#         Args:
#             file_patterns (list): 파일 경로 또는 와일드카드 패턴 목록
            
#         Returns:
#             list: 확장된 파일 경로 목록
#         """
#         expanded_files = []
        
#         for file_pattern in file_patterns:
#             if '*' in file_pattern or '?' in file_pattern:
#                 # 와일드카드 패턴이 포함된 경우 glob을 사용하여 확장
#                 matching_files = glob.glob(file_pattern)
#                 if not matching_files:
#                     self.log("WARN", f"매칭되는 파일 없음: {file_pattern}")
#                 expanded_files.extend(matching_files)
#             else:
#                 # 와일드카드가 없는 일반 파일
#                 expanded_files.append(file_pattern)
                
#         return expanded_files

#     def _expand_remote_file_patterns(self, file_patterns):
#         """
#         원격 디렉토리 내에서 주어진 패턴에 해당하는 파일 목록을 반환합니다.
        
#         Args:
#             file_patterns (list): 와일드카드 파일 이름 패턴 리스트 (예: ["*.txt", "data_??.csv"])
        
#         Returns:
#             list: 원격 디렉토리 내에서 패턴과 일치하는 파일 이름 목록
#         """
#         matched_files = []

#         try:
#             remote_files = self.sftp.listdir(self.remote_dir)
#         except Exception as e:
#             self.raise_error(f"원격 디렉토리 목록 가져오기 실패: {e}")

#         for pattern in file_patterns:
#             matches = fnmatch.filter(remote_files, pattern)
#             if not matches:
#                 self.log("WARN", f"매칭되는 원격 파일 없음: {pattern}")
#             matched_files.extend(matches)

#         return matched_files

#     def connect(self):
#         try:
#             self.ssh = paramiko.SSHClient()
#             self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#             # 인증 방식 결정: password 또는 key_file
#             if self.password:
#                 self.ssh.connect(
#                     hostname=self.host,
#                     port=self.port,
#                     username=self.user,
#                     password=self.password,
#                     timeout=self.timeout
#                 )
#             elif hasattr(self, "key_file") and self.key_file:
#                 pkey = paramiko.RSAKey.from_private_key_file(self.key_file)
#                 self.ssh.connect(
#                     hostname=self.host,
#                     port=self.port,
#                     username=self.user,
#                     pkey=pkey,
#                     timeout=self.timeout
#                 )
#             else:
#                 self.raise_error("password 또는 key_file 중 하나는 반드시 있어야 합니다.")

#             self.sftp = self.ssh.open_sftp()
#             self.sftp.get_channel().settimeout(self.timeout)  # ✅ socket 수준 timeout 적용

#             self.log("INFO", f"SFTP 연결 성공: {self.host}:{self.port}")
#         except Exception as e:
#             self.raise_error(f"SFTP 연결 실패: {e}")


#     def close(self):
#         if self.sftp:
#             self.sftp.close()
#         if self.ssh:
#             self.ssh.close()
#         self.log("INFO", "SFTP 연결 종료")

#     def upload(self):
#         if not self.files:
#             self.raise_error("SFTP 업로드할 파일이 없습니다.")
        
            
#         try:
#             self.connect()
#             # remote_dir이 없으면 생성하고 이동
#             self._ensure_remote_dir(self.remote_dir)
#             self._ensure_local_dir(self.local_dir)
#             # 와일드카드 패턴 확장
#             expanded_files = self._expand_local_file_patterns(self.files)
            
#             if not expanded_files:
#                 self.close()
#                 self.raise_error("SFTP 업로드할 파일이 없습니다.")


#             for filepath in expanded_files:
#                 if not os.path.isfile(filepath):
#                     self.log("WARN", f"SFTP 파일 없음: {self.local_dir}/{filepath}")
#                     continue
#                 filename = os.path.basename(filepath)
#                 # 현재 디렉토리(remote_dir)에 바로 업로드
#                 self.sftp.put(f"{self.local_dir}/{filepath}", f"{self.remote_dir}/{filename}")
#                 self.log("INFO", f"SFTP 업로드 완료: {filename}")
#         finally:
#             self.close()

#     def download(self):
#         if not self.files:
#             self.raise_error("SFTP 다운로드할 파일이 없습니다.")
        
#         try:
#             self.connect()
#             self._ensure_local_dir(self.local_dir)

#             # 와일드카드 패턴 확장 (서버 파일 목록에 대해)
#             expanded_files = self._expand_remote_file_patterns(self.files)

#             if not expanded_files:
#                 self.close()
#                 self.raise_error("SFTP 다운로드할 파일이 없습니다.")

#             for remote_filename in expanded_files: 
#                 local_filename = os.path.basename(remote_filename)

#                 if os.path.exists(local_filename) and not self.overwrite:
#                     self.log("WARN", f"SFTP 파일 존재(무시됨): {local_filename}")
#                     continue

#                 self.sftp.get(f"{self.remote_dir}/{remote_filename}", f"{self.local_dir}/{local_filename}")
#                 self.log("INFO", f"SFTP 다운로드 완료: {self.remote_dir}/{remote_filename} -> {self.local_dir}/{local_filename}")

#         finally:
#             self.close()

#     def delete(self):
#         if not self.files:
#             self.raise_error("삭제할 파일이 없습니다.")
#         try:
#             self.connect()
#             for filepath in self.files:
#                 filename = os.path.basename(filepath)
#                 try:
#                     self.sftp.remove(f"{self.remote_dir}/{filename}")
#                     self.log("INFO", f"삭제 완료: {filename}")
#                 except IOError as e:
#                     self.log("ERROR", f"삭제 실패: {filename} ({e})")
#         finally:
#             self.close()

#     def list(self):
#         try:
#             self.connect()
#             files = self.sftp.listdir(self.remote_dir)
#             pattern = self.pattern
#             if pattern:
#                 files = fnmatch.filter(files, pattern)

#             file_infos = []
#             for filename in files:
#                 try:
#                     filepath = self.remote_dir.rstrip('/') + '/' + filename
#                     stat = self.sftp.stat(filepath)
#                     size = stat.st_size
#                     mod_time = datetime.fromtimestamp(stat.st_mtime)

#                     file_infos.append({
#                         "name": filename,
#                         "size": size,
#                         "modified": mod_time.strftime("%Y-%m-%d %H:%M:%S")
#                     })
#                 except Exception as e:
#                     self.log("WARN", f"SFTP {filename} 메타데이터 조회 실패: {e}")
#                     file_infos.append({
#                         "name": filename,
#                         "size": None,
#                         "modified": None
#                     })

#             self.log("INFO", f"SFTP {len(file_infos)}개 파일 정보 조회 완료")
#             return file_infos
#         finally:
#             self.close()


#     def mkdir(self):
#         try:
#             self.connect()
#             self.sftp.mkdir(self.remote_dir)
#             self.log("INFO", f"디렉토리 생성: {self.remote_dir}")
#         finally:
#             self.close()

#     def rmdir(self):
#         try:
#             self.connect()
#             self.sftp.rmdir(self.remote_dir)
#             self.log("INFO", f"디렉토리 삭제: {self.remote_dir}")
#         finally:
#             self.close()



