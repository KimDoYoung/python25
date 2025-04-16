from lib.core.commands.base_command import BaseCommand
from lib.core.exceptions.kavana_exception import KavanaSftpError
from lib.core.managers.sftp_manager import SftpManager
from lib.core.token import Token
from lib.core.token_type import TokenType
from lib.core.token_util import TokenUtil


class SftpCommand(BaseCommand):
    ''' SFTP 명령어 해석'''
    OPTION_DEFINITIONS = {
        "host": {"required": True, "allowed_types": [TokenType.STRING]},
        "port": {"default": 22, "allowed_types": [TokenType.INTEGER]},
        "user": {"required": True, "allowed_types": [TokenType.STRING]},
        "password": {"required": False, "allowed_types": [TokenType.BOOLEAN]},
        "key_file": {"required": False, "allowed_types": [TokenType.BOOLEAN]},
        "remote_dir": {"required": True, "allowed_types": [TokenType.STRING]},
        "local_dir": {"required": True, "allowed_types": [TokenType.STRING]},
        "files": {"required": False, "allowed_types": [TokenType.ARRAY]},
        "timeout": {"default": 10, "allowed_types": [TokenType.INTEGER]},
        "overwrite": {"default": True, "allowed_types": [TokenType.BOOLEAN]},
        "pattern": {"default": "*", "allowed_types": [TokenType.STRING]}, 
        "to_var": {"required": False, "allowed_types": [TokenType.STRING]},
    }

    COMMAND_SPECS = {
        "UPLOAD": {
            "keys": ["host", "port", "user", "password", "key_file", "remote_dir", "local_dir", "files"],
            "overrides": {
                "host": {"required": True},
                "port": {"required": True},
                "user": {"required": True},
                "password": {"required": True},
                "key_file": {"required": True},
                "remote_dir": {"required": True},
                "local_dir": {"required": True},
                "files": {"required": True}
            },
            "rules": {
                "mutually_exclusive": [
                    ["password", "key_file"]
                ],
                "required_together": [
                    ["host", "port", "user", "password", "key_file"]
                ]
            }
        },
        "DOWNLOAD": {
            "keys": ["host", "port", "user", "password", "key_file", "remote_dir", "local_dir"],
            "overrides": {
                "host": {"required": True},
                "port": {"required": True},
                "user": {"required": True},
                "password": {"required": True},
                "key_file": {"required": True},
                "remote_dir": {"required": True},
                "local_dir": {"required": True}
            },
            "rules": {
                "mutually_exclusive": [
                    ["password", "key_file"]
                ],
                "required_together": [
                    ["host", "port", "user", "password", "key_file"]
                ]
            }
        },
        "LIST": {
            "keys": ["host", "port", "user", "password", "key_file", "remote_dir", "pattern", "to_var"],
            "overrides": {
                "host": {"required": True},
                "port": {"required": True},
                "user": {"required": True},
                "password": {"required": True},
                "key_file": {"required": True},
                "remote_dir": {"required": True},
                "pattern": {"required": True}
            },
            "rules": {
                "mutually_exclusive": [
                    ["password", "key_file"]
                ],
                "required_together": [
                    ["host", "port", "user", "password", "key_file"]
                ]
            }
        }
    }


    def execute(self, args: list[Token], executor):
        if not args:
            raise KavanaSftpError("RPA 명령어는 최소 하나 이상의 인자가 필요합니다.")

        sub_command = args[0].data.value.lower()
        options, _ = self.extract_all_options(args, 1)

        option_map, rules = self.get_option_spec(sub_command)
        option_values = self.parse_and_validate_options(options, option_map, executor)
        self.check_option_rules(sub_command, option_values, rules)

        try:
            manager = SftpManager(command=sub_command, **option_values, executor=executor)
            manager.execute()
        except KavanaSftpError as e:
            raise KavanaSftpError(f"RPA `{sub_command}` 명령어 처리 중 오류 발생: {str(e)}") from e

