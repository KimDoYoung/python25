from lib.core.commands.base_command import BaseCommand
from lib.core.exceptions.kavana_exception import KavanaHttpError
from lib.core.token import Token
from lib.core.token_type import TokenType


class HttpCommand(BaseCommand):
    ''' HTTP 명령어 해석'''
    def execute(self, args: list[Token], executor):
        if not args:
            raise KavanaHttpError("SFTP 명령어는 최소 하나 이상의 인자가 필요합니다.")

        sub_command = args[0].data.value.upper()
        options, _ = self.extract_all_options(args, 1)

        option_map = self.get_option_map(sub_command)
        option_values = self.parse_and_validate_options(options, option_map, executor)
        try:
            http_manager = HttpCommand(executor=executor)
            option_values["method"] = sub_command
            if sub_command == "GET":
                http_manager.execute(**option_values)
            elif sub_command == "POST":
                http_manager.execute(**option_values)
            elif sub_command == "PUT":
                http_manager.execute(**option_values)
            elif sub_command == "DELETE":
                http_manager.execute(**option_values)
            elif sub_command == "PATCH":
                http_manager.execute(**option_values)
            else:
                raise KavanaHttpError(f"지원하지 않는 HTTP sub_command: {sub_command}")
            http_manager.execute()
        except KavanaHttpError as e:
            raise KavanaHttpError(f"`{sub_command}` 명령어 처리 중 오류 발생: {str(e)}") from e
        return

    OPTION_DEFINITIONS = {
        "url": {"required": True, "allowed_types": [TokenType.STRING]},
        "headers": {"required": False, "allowed_types": [TokenType.INTEGER]},
        "params": {"required": False, "allowed_types": [TokenType.STRING]},
        "body": {"required": False, "allowed_types": [TokenType.BOOLEAN]},
        "content_type": {"required": False, "allowed_types": [TokenType.STRING]},
        "verify_ssl": {"required": False, "allowed_types": [TokenType.BOOLEAN]},
        "timeout": {"default": 10, "allowed_types": [TokenType.INTEGER]},
        "to_var": {"required": True, "allowed_types": [TokenType.STRING]},
    }

    # 필요한 키만 추려서 option_map 구성
    def option_map_define(self, *keys):
        '''필요한 키만 추려서 option_map 구성'''
        keys = set(keys) 
        
        option_map = {}
        for key in keys:
            option_map[key] = self.OPTION_DEFINITIONS[key]
        return option_map   
        
    def get_option_map(self, sub_command: str) -> dict:
        '''sub_command에 따른 옵션 맵 생성'''
        if sub_command == "GET":
            pass
        elif sub_command == "POST":
            pass
        elif sub_command == "PUT":
            pass
        elif sub_command == "DELETE":
            pass
        elif sub_command == "PATCH":
            pass
        else:
            raise KavanaHttpError(f"지원하지 않는 ftp sub_command: {sub_command}")    