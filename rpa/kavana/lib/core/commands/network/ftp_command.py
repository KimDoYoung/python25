from lib.core.commands.base_command import BaseCommand
from lib.core.exceptions.kavana_exception import KavanaFtpError
from lib.core.managers.ftp_manager import FtpManager
from lib.core.token import Token
from lib.core.token_type import TokenType
from lib.core.token_util import TokenUtil


class FtpCommand(BaseCommand):
    ''' FTP 명령어 해석 및 실행 '''
        
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

    COMMAND_SPECS = {
        "upload": {
            "keys": ["remote_dir", "local_dir", "files"],
            "overrides": {
                "remote_dir": {"required": True},
                "local_dir": {"required": True},
                "files": {"required": True}
            },
            "rules": {
                "mutually_exclusive": [],
                "required_together": []
            }
        },
        "download": {
            "keys": ["remote_dir", "local_dir", "files"],
            "overrides": {
                "remote_dir": {"required": True},
                "local_dir": {"required": True},
                "files": {"required": True}
            },
            "rules": {}
        },
        "list": {
            "keys": ["remote_dir", "pattern", "to_var"],
            "overrides": {
                "remote_dir": {"required": True},
                "pattern": {"required": False},
                "to_var": {"required": True}
            },
            "rules": {}
        }
    }

    def execute(self, args: list[Token], executor):
            if not args:
                raise KavanaFtpError("RPA 명령어는 최소 하나 이상의 인자가 필요합니다.")

            sub_command = args[0].data.value.lower()
            options, _ = self.extract_all_options(args, 1)

            option_map, rules = self.get_option_spec(sub_command)
            option_values = self.parse_and_validate_options(options, option_map, executor)
            self.check_option_rules(sub_command, option_values, rules)

            try:
                manager = FtpCommand(command=sub_command, **option_values, executor=executor)
                manager.execute()
            except KavanaFtpError as e:
                raise KavanaFtpError(f"RPA `{sub_command}` 명령어 처리 중 오류 발생: {str(e)}") from e
