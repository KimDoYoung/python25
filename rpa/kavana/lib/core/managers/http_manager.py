import requests

from lib.core.managers.base_manager import BaseManager


class HttpManager(BaseManager):
    def __init__(self, **kwargs):
        super().__init__(kwargs.get("executor", None))
        self.command = kwargs.get("command", None)
        self.options = kwargs
        if not self.command:
            self.raise_error("command 인자가 필요합니다.")

    def execute(self):
        try:
            response = self.send_request_with_requests()
            return self.parse_response(response)
        except requests.exceptions.SSLError as e:
            self.log("WARN", f"requests 실패, curl로 재시도합니다: {e}")
            response = self.send_request_with_curl()
            return self.parse_response(response, is_curl=True)
        except Exception as e:
            self.raise_error(f"HTTP 요청 실패: {e}")

    def send_request_with_requests(self):
        import requests

        method = self.command.upper()
        url = self.options.get("url")
        headers = self.options.get("headers", {})
        headers.setdefault("User-Agent", "Mozilla/5.0")
        params = self.options.get("params", {})
        body = self.options.get("body", None)
        timeout = self.options.get("timeout", 10)
        verify_ssl = self.options.get("verify_ssl", True)
        content_type = self.options.get("content_type")

        if content_type:
            headers["Content-Type"] = content_type

        request_args = {
            "method": method,
            "url": url,
            "headers": headers,
            "params": params,
            "timeout": timeout,
            "verify": verify_ssl,
        }

        if method in ["POST", "PUT", "PATCH"]:
            if content_type == "application/json":
                request_args["json"] = body
            else:
                request_args["data"] = body

        self.log("INFO", f"요청 시작: {method} {url}")
        response = requests.request(**request_args)
        return response

    def send_request_with_curl(self):
        import subprocess, json
        from urllib.parse import urlencode

        method = self.command.upper()
        url = self.options.get("url")
        headers = self.options.get("headers", {})
        params = self.options.get("params", {})
        body = self.options.get("body", None)
        timeout = self.options.get("timeout", 10)

        full_url = f"{url}?{urlencode(params)}"

        curl_cmd = [
            "curl", "-k", "-X", method, full_url,
            "-H", "User-Agent: Mozilla/5.0"
        ]

        for k, v in headers.items():
            curl_cmd += ["-H", f"{k}: {v}"]

        if body:
            if isinstance(body, dict):
                body = json.dumps(body)
            curl_cmd += ["--data", body]

        result = subprocess.run(
            curl_cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8"  # ✅ 여기 중요
        )
        stdout = result.stdout or ""
        if not stdout.strip():
            self.raise_error("curl 응답이 비어 있습니다.")

        return stdout        

    def parse_response(self, response, is_curl=False):
        import json, xmltodict

        try:
            if is_curl:
                # curl의 경우 Content-Type 알 수 없으므로 추정
                try:
                    return json.loads(response)
                except:
                    return xmltodict.parse(response)
            else:
                content_type = response.headers.get("Content-Type", "").lower()
                if "application/json" in content_type:
                    return response.json()
                elif "xml" in content_type:
                    return xmltodict.parse(response.text)
                else:
                    return response.text
        except Exception as e:
            self.log("ERROR", f"HTTP 응답 파싱 실패: {e}")
            return response.text if not is_curl else response
