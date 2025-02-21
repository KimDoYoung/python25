import re

class FunctionParser:
    def __init__(self, expression: str):
        self.expression = expression

    def parse_arguments(self):
        """
        함수 인자를 분석하여 위치 기반 인자와 키워드 인자를 구분하여 반환한다.
        숫자, Boolean, NULL 값을 자동 변환한다.
        """
        args = []
        kwargs = {}

        match = re.search(r'\((.*?)\)', self.expression)
        if not match:
            raise ValueError("잘못된 함수 호출 형식")

        arg_string = match.group(1).strip()
        if not arg_string:
            return [], {}  # ✅ 빈 인자 처리 (empty_func())

        tokens = [t.strip() for t in arg_string.split(",")]

        for token in tokens:
            if "=" in token:
                key, value = token.split("=", 1)
                kwargs[key.strip()] = self._convert_value(value.strip())  # ✅ 값 변환 적용
            else:
                args.append(self._convert_value(token))  # ✅ 값 변환 적용

        return args, kwargs

    def _convert_value(self, value: str):
        """숫자, Boolean, NULL, 문자열 값 변환"""
        value_upper = value.upper()

        if value_upper == "TRUE":
            return True
        elif value_upper == "FALSE":
            return False
        elif value_upper == "NULL":
            return None
        elif value.startswith('"') and value.endswith('"'):
            return value.strip('"')  # ✅ 문자열 리터럴 따옴표 제거
        elif value.isdigit():
            return int(value)
        try:
            return float(value) if "." in value else int(value)
        except ValueError:
            return value  # 변환할 수 없는 경우 원본 문자열 유지
