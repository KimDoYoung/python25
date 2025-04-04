import requests
from base_manager import BaseManager

class HttpManager(BaseManager):
    def __init__(self, **kwargs):
        super().__init__(kwargs.get("executor", None))

        self.method = kwargs.get("method", "GET").upper()
        self.url = kwargs.get("url")
        self.headers = kwargs.get("headers", {})
        self.params = kwargs.get("params", {})
        self.body = kwargs.get("body", None)
        self.content_type = kwargs.get("content_type", "application/json")
        self.timeout = kwargs.get("timeout", 10)
        self.verify_ssl = kwargs.get("verify_ssl", True)

        if not self.url:
            self.raise_error("url은 필수입니다.")
        if not self.method:
            self.raise_error("method는 필수입니다.")

    def execute(self):
        try:
            session = requests.Session()

            # Content-Type 처리
            if self.content_type:
                self.headers["Content-Type"] = self.content_type

            request_args = {
                "method": self.method,
                "url": self.url,
                "headers": self.headers,
                "params": self.params,
                "timeout": self.timeout,
                "verify": self.verify_ssl,
            }

            if self.method in ["POST", "PUT", "PATCH"]:
                if self.content_type == "application/json":
                    request_args["json"] = self.body
                else:
                    request_args["data"] = self.body

            self.log("INFO", f"요청 시작: {self.method} {self.url}")
            response = session.request(**request_args)

            self.log("INFO", f"응답 수신 완료: {response.status_code}")
            self.log("INFO", f"응답 본문: {response.text[:500]}")  # 최대 500자만 출력
            return response

        except requests.exceptions.RequestException as e:
            self.raise_error(f"HTTP 요청 실패: {e}")
