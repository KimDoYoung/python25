from lib.core.commands.base_command import BaseCommand
from lib.core.exceptions.kavana_exception import KavanaFtpError
from lib.core.managers.ftp_manager import FtpManager
from lib.core.token import Token
from lib.core.token_type import TokenType


class FtpCommand(BaseCommand):
    ''' 데이터베이스 명령어 해석'''
    def execute(self, args: list[Token], executor):
        if not args:
            raise KavanaFtpError("FTP 명령어는 최소 하나 이상의 인자가 필요합니다.")

        sub_command = args[0].data.value.upper()
        options, _ = self.extract_all_options(args, 1)

        option_map = self.get_option_map(sub_command)
        option_values = self.parse_and_validate_options(options, option_map, executor)
        try:
            if sub_command == "UPLOAD":
                ftp_manager = FtpManager(**option_values, executor=executor)
                ftp_manager.upload()
            elif sub_command == "DOWNLOAD":
                ftp_manager = FtpManager(**option_values, executor=executor)
                ftp_manager.download()
            elif sub_command == "LIST":
                ftp_manager = FtpManager(**option_values, executor=executor)
                files = ftp_manager.list()
                if "to_var" in option_values:
                    executor.set_variable(option_values["to_var"], files)
        except KavanaFtpError as e:
            raise KavanaFtpError(f"`{sub_command}` 명령어 처리 중 오류 발생: {str(e)}") from e
        
        return
    
    OPTION_DEFINITIONS = {
        "host": {"required": True, "allowed_types": [TokenType.STRING]},
        "port": {"default": 21, "allowed_types": [TokenType.INTEGER]},
        "user": {"required": True, "allowed_types": [TokenType.STRING]},
        "password": {"required": True, "allowed_types": [TokenType.STRING]},
        "remote_dir": {"required": True, "allowed_types": [TokenType.STRING]},
        "local_dir": {"required": True, "allowed_types": [TokenType.STRING]},
        "files": {"required": False, "allowed_types": [TokenType.ARRAY]},
        "passive": {"default": True, "allowed_types": [TokenType.BOOLEAN]},
        "timeout": {"default": 10, "allowed_types": [TokenType.INTEGER]},
        "overwrite": {"default": True, "allowed_types": [TokenType.BOOLEAN]},
        "pattern": {"default": "*", "allowed_types": [TokenType.STRING]},
        "to_var": {"required": False, "allowed_types": [TokenType.STRING]},
    }

    # 필요한 키만 추려서 option_map 구성
    def option_map_define(self, *keys):
        '''필요한 키만 추려서 option_map 구성'''
        # "host","port", "user", "password", 이 keys에 없으면 추가
        required_keys = {"host", "port", "user", "password", "passive", "timeout", "overwrite"}
        keys = set(keys) | required_keys # keys에 없는 required_keys(필수키) 추가

        option_map = {}
        for key in keys:
            option_map[key] = self.OPTION_DEFINITIONS[key]
        return option_map   
        
    def get_option_map(self, sub_command: str) -> dict:
        '''sub_command에 따른 옵션 맵 생성'''
        match (sub_command):
            case ("UPLOAD"):
                return self.option_map_define( "remote_dir", "local_dir", "files")
            case ("DOWNLOAD"):
                return self.option_map_define( "remote_dir", "local_dir", "files")
            case ("LIST"):
                return self.option_map_define( "remote_dir", "pattern", "to_var")
            case _:
                raise KavanaFtpError(f"지원하지 않는 ftp sub_command: {sub_command}")