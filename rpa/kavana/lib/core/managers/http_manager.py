import requests

from lib.core.managers.base_manager import BaseManager


class HttpManager(BaseManager):
    def __init__(self, **kwargs):
        super().__init__(kwargs.get("executor", None))

    def execute(self, **kwargs):
        try:
            response = self.send_request_with_requests(**kwargs)
            return self.parse_response(response)
        except requests.exceptions.SSLError as e:
            self.log("WARN", f"requests 실패, curl로 재시도합니다: {e}")
            response = self.send_request_with_curl(**kwargs)
            return self.parse_response(response, is_curl=True)
        except Exception as e:
            self.raise_error(f"HTTP 요청 실패: {e}")

    def send_request_with_requests(self, **kwargs):
        import requests

        method = kwargs.get("method", "GET").upper()
        url = kwargs.get("url")
        headers = kwargs.get("headers", {})
        headers.setdefault("User-Agent", "Mozilla/5.0")
        params = kwargs.get("params", {})
        body = kwargs.get("body", None)
        timeout = kwargs.get("timeout", 10)
        verify_ssl = kwargs.get("verify_ssl", True)
        content_type = kwargs.get("content_type")

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

    def send_request_with_curl(self, **kwargs):
        import subprocess, json
        from urllib.parse import urlencode

        method = kwargs.get("method", "GET").upper()
        url = kwargs.get("url")
        headers = kwargs.get("headers", {})
        params = kwargs.get("params", {})
        body = kwargs.get("body", None)
        timeout = kwargs.get("timeout", 10)

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

# import subprocess
# import requests
# from urllib.parse import urlencode
# from lib.core.managers.base_manager import BaseManager


# class HttpManager(BaseManager):
#     def __init__(self, **kwargs):
#         super().__init__(kwargs.get("executor", None))

#     def execute(self, **kwargs):
#         method = kwargs.get("method", "GET").upper()
#         url = kwargs.get("url")
#         headers = kwargs.get("headers", {})
#         headers.setdefault("User-Agent", "Mozilla/5.0")
#         params = kwargs.get("params", {})
#         timeout = kwargs.get("timeout", 10)
#         verify_ssl = kwargs.get("verify_ssl", True)
#         content_type = kwargs.get("content_type")
#         body = kwargs.get("body", None)

#         if content_type:
#             headers["Content-Type"] = content_type

#         # 요청용 딕셔너리 준비
#         request_args = {
#             "method": method,
#             "url": url,
#             "headers": headers,
#             "params": params,
#             "timeout": timeout,
#             "verify": verify_ssl,
#         }

#         if method in ["POST", "PUT", "PATCH"]:
#             if content_type == "application/json":
#                 request_args["json"] = body
#             else:
#                 request_args["data"] = body

#         try:
#             query_string = urlencode(params, doseq=True)
#             self.log("DEBUG", f"최종 요청 URL: {url}?{query_string}")
#             self.log("INFO", f"요청 시작: {method} {url}")

#             response = requests.request(**request_args)
#             self.log("INFO", f"응답 수신 완료: {response.status_code}")
#             self.log("INFO", f"응답 본문: {response.text[:500]}")
#             return response

#         except requests.exceptions.SSLError as e:
#             self.log("WARN", f"requests 실패, curl로 재시도합니다: {e}")

#             # curl 명령어 구성
#             curl_cmd = [
#                 "curl",
#                 "-k",  # verify_ssl=False와 동일
#                 "-X", method,
#                 f"{url}?{urlencode(params)}"
#             ]

#             for k, v in headers.items():
#                 curl_cmd += ["-H", f"{k}: {v}"]

#             if body:
#                 import json
#                 if isinstance(body, dict):
#                     body = json.dumps(body)
#                 curl_cmd += ["--data", body]

#             self.log("DEBUG", f"curl 명령: {' '.join(curl_cmd)}")

#             try:
#                 result = subprocess.run(
#                     curl_cmd,
#                     capture_output=True,
#                     text=True,
#                     timeout=timeout
#                 )
#                 self.log("INFO", f"curl 응답 수신 완료")
#                 self.log("INFO", result.stdout[:500])
#                 return result.stdout
#             except Exception as e2:
#                 self.raise_error(f"curl 요청도 실패했습니다: {e2}")

#         except Exception as e:
#             self.raise_error(f"HTTP 요청 실패: {e}")



# import requests

# from lib.core.managers.base_manager import BaseManager


# class HttpManager(BaseManager):
#     def __init__(self, **kwargs):
#         super().__init__(kwargs.get("executor", None))

#     def execute(self, **kwargs):
#         try:
#             import ssl
#             from urllib3.poolmanager import PoolManager
#             from requests.adapters import HTTPAdapter

#             class TLSAdapter(HTTPAdapter):
#                 def init_poolmanager(self, *args, **kwargs):
#                     context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#                     kwargs['ssl_context'] = context
#                     return super().init_poolmanager(*args, **kwargs)

#             session = requests.Session()
#             session.mount("https://", TLSAdapter())  # ✅ TLS 1.2 강제 적용

#             method = kwargs.get("method", "GET").upper()
#             url = kwargs.get("url")
#             headers = kwargs.get("headers", {})
#             headers.setdefault("User-Agent", "Mozilla/5.0")  # ✅ UA 설정
#             params = kwargs.get("params", {})
#             body = kwargs.get("body", None)
#             timeout = kwargs.get("timeout", 10)
#             verify_ssl = kwargs.get("verify_ssl", True)
#             content_type = kwargs.get("content_type")

#             if content_type:
#                 headers["Content-Type"] = content_type

#             request_args = {
#                 "method": method,
#                 "url": url,
#                 "headers": headers,
#                 "params": params,
#                 "timeout": timeout,
#                 "verify": verify_ssl,
#             }

#             if method in ["POST", "PUT", "PATCH"]:
#                 if content_type == "application/json":
#                     request_args["json"] = body
#                 else:
#                     request_args["data"] = body

#             from urllib.parse import urlencode
#             query_string = urlencode(params, doseq=True)
#             self.log("DEBUG", f"최종 요청 URL: {url}?{query_string}")  # ✅ 디버깅용

#             self.log("INFO", f"요청 시작: {method} {url}")
#             response = session.request(**request_args)

#             self.log("INFO", f"응답 수신 완료: {response.status_code}")
#             self.log("INFO", f"응답 본문: {response.text[:500]}")
#             return response

#         except requests.exceptions.RequestException as e:
#             self.raise_error(f"HTTP 요청 실패: {e}")

