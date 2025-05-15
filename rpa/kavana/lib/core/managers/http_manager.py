import os
import re
import requests
import subprocess, json
import datetime
import urllib
from lib.core.managers.base_manager import BaseManager
from lib.core.token_util import TokenUtil


class HttpManager(BaseManager):
    def __init__(self, **kwargs):
        super().__init__(kwargs.get("executor", None))
        self.command = kwargs.get("command", None)
        self.options = kwargs
        if not self.command:
            self.raise_error("command 인자가 필요합니다.")

    def execute(self):
        try:
            # response = self.send_request_with_requests()
            # return self.parse_response(response)
            return self.send_request_with_requests()
        except requests.exceptions.SSLError as e:
            self.log("WARN", f"requests 실패, curl로 재시도합니다: {e}")
            return self.send_request_with_curl()
            # response = self.send_request_with_curl()
            # return self.parse_response(response, is_curl=True)
        except Exception as e:
            self.raise_error(f"HTTP 요청 실패: {e}")

    def send_request_with_requests(self):
        import requests

        method = self.command.upper()
        url = self.options.get("url")
        headers = self.options.get("headers", {})
        # headers.setdefault("User-Agent", "Mozilla/5.0")
        params = self.options.get("params", {})
        body = self.options.get("body", None)
        timeout = self.options.get("timeout", 10)
        verify_ssl = self.options.get("verify_ssl", True)
        content_type = self.options.get("content_type")
        to_var = self.options.get("to_var")
        to_file = self.options.get("to_file")
        to_dir = self.options.get("to_dir")


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
        if method == "DOWNLOAD":
            self.log("INFO", f"다운로드 시작: {url}")
            # headers = {
            #     "User-Agent": "Mozilla/5.0",
            #     "Referer" :"https://law.kofia.or.kr/service/revisionNotice/revisionNoticeListframe.do"
            # }
            try:
                response = requests.get(url, headers=headers)
                save_path = None
                if to_file is not None:
                    save_path = to_file
                elif to_dir is not None:
                    # Content-Disposition 헤더에서 파일명 시도
                    # cd = response.headers.get("Content-Disposition", "")
                    filename = self._extract_filename_from_headers(response.headers)
                    save_path = os.path.join(to_dir, filename)
                else:
                    self.raise_error("to_file 또는 to_dir 중 하나는 지정해야 합니다.")
                with open(save_path, "wb") as f:
                    f.write(response.content)
                if to_var:
                    self.executor.set_variable(to_var, TokenUtil.string_to_string_token(save_path))
                self.log("INFO", f"다운로드 완료: {save_path}")
            except requests.exceptions.RequestException as e:
                self.raise_error(f"다운로드 요청 실패: {e}")
            except Exception as e:
                self.raise_error(f"다운로드 파일 저장 실패: {e}")
            return None
        else:
            response = requests.request(**request_args)
            parsed_response = self.parse_response(response)
            if isinstance(parsed_response, str):
                result_token = TokenUtil.string_to_string_token(parsed_response)
            elif isinstance(parsed_response, dict):
                result_token = TokenUtil.dict_to_hashmap_token(parsed_response)
            else:
                raise self.raise_error(f"지원하지 않는 HTTP 응답 타입: {type(parsed_response)}")
            
            if to_var:
                self.executor.set_variable(to_var, result_token)


    def send_request_with_curl(self):
        
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

    def _extract_filename_from_headers(self,headers):
        cd = headers.get('Content-Disposition', '')
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y_%m_%d_%H_%M_%S")
        filename = f"{timestamp}.dat"

        # 우선 filename*= 시도 (RFC 6266)
        match = re.search(r"filename\*=UTF-8''(.+)", cd, re.IGNORECASE)
        if match:
            filename = urllib.parse.unquote(match.group(1))
        else:
            # 일반 filename= 시도
            match = re.search(r'filename="?([^";]+)"?', cd, re.IGNORECASE)
            if match:
                raw_filename = match.group(1)
                try:
                    filename = raw_filename.encode('latin1').decode('euc-kr')
                except:
                    filename = raw_filename  # fallback

        return filename