import requests
from lib.core.managers.base_manager import BaseManager

class HttpManager(BaseManager):
    def __init__(self, **kwargs):
        super().__init__(kwargs.get("executor", None))

    def execute(self, **kwargs):
        try:
            session = requests.Session()

            # 기본 요청 매개변수 설정
            request_args = {
                "method": kwargs.get("method", "GET").upper(),
                "url": kwargs.get("url"),
                "headers": kwargs.get("headers", {}),
                "params": kwargs.get("params", {}),
                "body": kwargs.get("body", None),
                "timeout": kwargs.get("timeout", 10),
                "verify_ssl": kwargs.get("verify_ssl", True),
            }

            # Content-Type 처리
            content_type = kwargs.get("content_type", "application/json")
            if content_type:
                request_args["headers"]["Content-Type"] = content_type

            # Body 처리
            if request_args["method"] in ["POST", "PUT", "PATCH"]:
                body = kwargs.get("body", None)
                if content_type == "application/json":
                    request_args["json"] = body
                else:
                    request_args["data"] = body

            # 로그 출력
            self.log("INFO", f"요청 시작: {request_args['method']} {request_args['url']}")
            response = session.request(**request_args)

            # 응답 로그 출력
            self.log("INFO", f"응답 수신 완료: {response.status_code}")
            self.log("INFO", f"응답 본문: {response.text[:500]}")  # 최대 500자만 출력
            return response

        except requests.exceptions.RequestException as e:
            self.raise_error(f"HTTP 요청 실패: {e}")