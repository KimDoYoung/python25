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
    OPTION_DEFINITIONS = {
        "url": {"required": True, "allowed_types": [TokenType.STRING]},
        "headers": {"required": False, "allowed_types": [TokenType.HASH_MAP]},
        "params": {"required": False, "allowed_types": [TokenType.HASH_MAP]},
        "body": {"required": False, "allowed_types": [TokenType.BOOLEAN]},
        "content_type": {"required": False, "allowed_types": [TokenType.STRING]},
        "verify_ssl": {"required": False, "allowed_types": [TokenType.BOOLEAN]},
        "timeout": {"default": 10, "allowed_types": [TokenType.INTEGER]},
        "to_var": {"required": False, "allowed_types": [TokenType.STRING]},
        "to_file": {"required": False, "allowed_types": [TokenType.STRING]},
        "to_dir": {"required": False, "allowed_types": [TokenType.STRING]},
    }
    COMMAND_SPECS = {
        "download": {
            "keys": ["url", "headers", "to_file", "to_dir", "to_var"],
            "overrides": {
                "url": {"required": True},
            },
            "rules": {
                "mutually_exclusive": [],
                "required_together": []
            }
        },
        "get": {
            "keys": ["url", "headers", "params", "content_type", "verify_ssl", "timeout", "to_var"],
            "overrides": {
                "url": {"required": True},
                "to_var": {"required": True}
            },
            "rules": {
                "mutually_exclusive": [],
                "required_together": []
            }
        },
        "post": {
            "keys": ["url", "headers", "params", "body", "content_type", "verify_ssl", "timeout", "to_var"],
            "overrides": {
                "url": {"required": True},
                "to_var": {"required": True}
            },
            "rules": {}
        },
        "put": {
            "keys": ["url", "headers", "params", "body", "content_type", "verify_ssl", "timeout"],
            "overrides": {
                "url": {"required": True}
            },
            "rules": {}
        },
        "delete": {
            "keys": ["url", "headers", "params", "content_type", "verify_ssl", "timeout"],
            "overrides": {
                "url": {"required": True}
            },
            "rules": {}
        },
        "patch": {
            "keys": ["url", "headers", "params", "body", "content_type", "verify_ssl", "timeout"],
            "overrides": {
                "url": {"required": True}
            },
            "rules": {}
        }
    }

    def execute(self, args: list[Token], executor):
        if not args:
            raise KavanaHttpError("HTTP 명령어는 최소 하나 이상의 인자가 필요합니다.")

        sub_command = args[0].data.value.lower()
        options, _ = self.extract_all_options(args, 1)

        option_map, rules = self.get_option_spec(sub_command)
        option_values = self.parse_and_validate_options(options, option_map, executor)
        self.check_option_rules(sub_command, option_values, rules)

        try:
            manager = HttpManager(command=sub_command, **option_values, executor=executor)
            manager.execute()
            # response = manager.execute()
            # if response is None:
            #     response = ""
            # var_name = option_values.get("to_var")
            # if var_name:
            #     if isinstance(response, str):
            #         result_token = StringToken(data=String(response), type=TokenType.STRING)
            #     elif isinstance(response, dict):
            #         result_token = TokenUtil.dict_to_hashmap_token(response)
            #     else:
            #         raise KavanaHttpError(f"지원하지 않는 HTTP 응답 타입: {type(response)}")
            #     executor.set_variable(var_name, result_token)            
        except KavanaHttpError as e:
            raise KavanaHttpError(f"HTTP `{sub_command}` 명령어 처리 중 오류 발생: {str(e)}") from e
