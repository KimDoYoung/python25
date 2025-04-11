from lib.core.commands.base_command import BaseCommand
from lib.core.datatypes.kavana_datatype import String
from lib.core.exceptions.kavana_exception import KavanaHttpError
from lib.core.managers.http_manager import HttpManager
from lib.core.token import StringToken, Token
from lib.core.token_type import TokenType
from lib.core.token_util import TokenUtil

# TODO : download 기능 추가
# from_var	URL 리스트가 저장된 변수명
# to_folder	저장 경로 (./downloads 등)
# prefix	저장할 파일 이름 접두어
# limit	(선택) 최대 다운로드 개수
#     # def save(self):
    # import os
    # import requests
    # from urllib.parse import urlparse
    #     from_var = self.options.get("from_var")
    #     to_folder = self.options.get("to_folder", "./downloads")
    #     prefix = self.options.get("prefix", "file_")
    #     limit = int(self.options.get("limit", 0))  # 0이면 제한 없음

    #     urls = self.get_variable(from_var)
    #     if not isinstance(urls, list):
    #         self.raise_error(f"{from_var}는 리스트가 아닙니다.")

    #     os.makedirs(to_folder, exist_ok=True)

    #     for i, url in enumerate(urls):
    #         if limit and i >= limit:
    #             break
    #         try:
    #             res = requests.get(url, timeout=10)
    #             res.raise_for_status()

    #             # 확장자 자동 추출
    #             file_ext = os.path.splitext(urlparse(url).path)[1] or ".bin"
    #             filename = f"{prefix}{i}{file_ext}"
    #             file_path = os.path.join(to_folder, filename)

    #             with open(file_path, "wb") as f:
    #                 f.write(res.content)

    #             self.log("INFO", f"저장 완료: {file_path}")
    #         except Exception as e:
    #             self.log("WARN", f"{url} 저장 실패: {e}")


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
            http_manager = HttpManager(executor=executor)
            option_values["method"] = sub_command
            if sub_command == "GET":
                response = http_manager.execute(**option_values)
                if response is None:
                    response = ""
                var_name = option_values.get("to_var")
                if var_name:
                    if isinstance(response, str):
                        result_token = StringToken(data=String(response), type=TokenType.STRING)
                    elif isinstance(response, dict):
                        result_token = TokenUtil.dict_to_hashmap_token(response)
                    else:
                        raise KavanaHttpError(f"지원하지 않는 HTTP 응답 타입: {type(response)}")
                    executor.set_variable(var_name, result_token)
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
            return self.option_map_define('url', 'headers', 'params',  'content_type', 'verify_ssl', 'timeout', 'to_var')
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