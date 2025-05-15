import re
from typing import Any, Dict, List, Union

from lib.core.datatypes.kavana_datatype import Boolean, Float, Integer, String
from lib.core.datatypes.array import Array
from lib.core.exceptions.kavana_exception import KavanaTypeError, KavanaValueError
from lib.core.token import  ArrayToken, StringToken, Token
from lib.core.token_type import TokenType
from lib.core.token_util import TokenUtil


class StringFunctions:
    ''' 문자열 관련 내장 함수들 '''
    executor = None  # ✅ 클래스 변수로 executor 저장
    
    @staticmethod
    def set_executor(executor_instance):
        StringFunctions.executor = executor_instance

    @staticmethod
    def LENGTH(s: Any) -> Token:
        if isinstance(s, str):
            i = len(s)
            return Token(data=Integer(i), type=TokenType.INTEGER)
        elif isinstance(s, List):
            i = len(s)
            return Token(data=Integer(i), type=TokenType.INTEGER)  # Updated to use 'i' instead of 'len(s)'
        elif isinstance(s, Dict):
            i = len(s)
            return Token(data=Integer(i), type=TokenType.INTEGER)
        StringFunctions.executor.log_command("ERROR", "LENGTH() 함수는 문자열과 Array, HashMap 타입에만 적용됩니다")
        raise KavanaTypeError("LENGTH() 함수는 문자열과 Array, HashMap 타입에만 적용됩니다")

    @staticmethod
    def SUBSTR(s: str, start: int, length: int) -> Token:
        if isinstance(s, str) and isinstance(start, int) and isinstance(length, int):
            result = s[start:start + length]
            return StringToken(data=String(result), type=TokenType.STRING)
        StringFunctions.executor.log_command("ERROR", "형식은 SUBSTR(문자열, 시작인덱스, 길이)로 되어 있습니다")
        raise KavanaTypeError("형식은 SUBSTR(문자열, 시작인덱스, 길이)로 되어 있습니다")
    
    @staticmethod
    def UPPER(s: str) -> Token:
        if isinstance(s, str):
            result = s.upper()
            return StringToken(data=String(result), type=TokenType.STRING)
        StringFunctions.executor.log_command("ERROR", "UPPER()는 문자열에만 적용됩니다")
        raise KavanaTypeError("UPPER()는 문자열에만 적용됩니다")
    
    @staticmethod
    def LOWER(s: str) -> Token:
        if isinstance(s, str):
            result = s.lower()
            return StringToken(data=String(result), type=TokenType.STRING)
        
        StringFunctions.executor.log_command("ERROR", "LOWER()는 문자열에만 적용됩니다")
        raise KavanaTypeError("LOWER()는 문자열에만 적용됩니다")
    
    @staticmethod
    def TRIM(s: str) -> Token:
        if isinstance(s, str):
            result = s.strip()
            return StringToken(data=String(result), type=TokenType.STRING)
        
        StringFunctions.executor.log_command("ERROR", "TRIM()는 문자열에만 적용됩니다")
        raise KavanaTypeError("TRIM()는 문자열에만 적용됩니다")
    
    @staticmethod
    def LTRIM(s: str) -> Token:
        if isinstance(s, str):
            result = s.lstrip()
            return StringToken(data=String(result), type=TokenType.STRING)
        
        StringFunctions.executor.log_command("ERROR", "LTRIM()는 문자열에만 적용됩니다")
        raise KavanaTypeError("LTRIM()는 문자열에만 적용됩니다")
    
    @staticmethod
    def RTRIM(s: str) -> Token:
        if isinstance(s, str):
            result = s.rstrip()
            return StringToken(data=String(result), type=TokenType.STRING)
        
        StringFunctions.executor.log_command("ERROR", "RTRIM()는 문자열에만 적용됩니다")
        raise KavanaTypeError("RTRIM()는 문자열에만 적용됩니다")
    
    @staticmethod
    def REPLACE(s: str, old: str, new: str) -> Token:
        if isinstance(s, str) and isinstance(old, str) and isinstance(new, str):
            result = s.replace(old, new)
            return StringToken(data=String(result), type=TokenType.STRING)
        StringFunctions.executor.log_command("ERROR", "사용형식 : REPLACE(문자열, 바꿀문자열 , 새로운문자열)")
        raise KavanaTypeError("사용형식 : REPLACE(문자열, 바꿀문자열 , 새로운문자열)")
    
    @staticmethod
    def SPLIT(s: str, sep: str) -> Token:
        '''  문자열을 구분자로 나누어 리스트로 반환합니다.'''
        if isinstance(s, str) and isinstance(sep, str):
            result = s.split(sep)
            token_list = []
            for item in result:
                token_list.append(StringToken(data=String(item), type=TokenType.STRING))
            return TokenUtil.array_to_array_token(token_list)  
        StringFunctions.executor.log_command("ERROR", "사용형식 : SPLIT(문자열, 구분자)")
        raise KavanaTypeError("사용형식 : SPLIT(문자열, 구분자)")
    
    @staticmethod
    def JOIN(s: List[str], sep: str) -> Token:
        if isinstance(s, List) and isinstance(sep, str):
            result = sep.join(s)
            return StringToken(data=String(result), type=TokenType.STRING)
        StringFunctions.executor.log_command("ERROR", "사용형식 : JOIN(리스트, 구분자)")
        raise KavanaTypeError("사용형식 : JOIN(리스트, 구분자)")
    
    @staticmethod
    def STARTSWITH(s: str, prefix: str) -> Token:
        if isinstance(s, str) and isinstance(prefix, str):
            b = s.startswith(prefix)
            return TokenUtil.boolean_to_boolean_token(b)  
        StringFunctions.executor.log_command("ERROR", "사용형식 : STARTSWITH(문자열, 접두사)")
        raise KavanaTypeError("사용형식 : STARTSWITH(문자열, 접두사)")
    
    @staticmethod
    def ENDSWITH(s: str, suffix: str) -> bool:
        if isinstance(s, str) and isinstance(suffix, str):
            b = s.endswith(suffix)
            return TokenUtil.boolean_to_boolean_token(b)  
        StringFunctions.executor.log_command("ERROR", "사용형식 : ENDSWITH(문자열, 접미사)")
        raise KavanaTypeError("사용형식 : ENDSWITH(문자열, 접미사)")
    

    @staticmethod
    def CONTAINS(s: Union[str, List, Dict], sub: Any) -> Token:
        """
        문자열, 리스트, 딕셔너리에서 특정 요소가 포함되어 있는지 확인합니다.
        
        - 문자열: 부분 문자열이 포함되어 있는지 확인.
        - 리스트: 요소가 포함되어 있는지 확인.
        - 딕셔너리: 키가 포함되어 있는지 확인.
        """
        if isinstance(s, str) and isinstance(sub, str):
            b = sub in s
            return TokenUtil.boolean_to_boolean_token(b)
        elif isinstance(s, List):
            value_array = [token.data.value if hasattr(token, "data") and hasattr(token.data, "value") else token for token in s]
            b = sub in value_array        
            return TokenUtil.boolean_to_boolean_token(b)
        elif isinstance(s, Dict):
            b = sub in s.keys()
            return TokenUtil.boolean_to_boolean_token(b)
        else:
            StringFunctions.executor.log_command("ERROR", "CONTAINS()는 문자열, 리스트, 딕셔너리에만 적용됩니다")
            raise KavanaTypeError("CONTAINS()는 문자열, 리스트, 딕셔너리에만 적용됩니다")

    @staticmethod
    def INDEX_OF(s: Union[str, List, Dict], sub: Any) -> Token:
        """
        문자열, 리스트, 딕셔너리에서 특정 요소의 인덱스를 반환합니다.
        - 문자열: 부분 문자열의 시작 인덱스 반환 (없으면 -1)
        - 리스트: 요소의 인덱스 반환 (없으면 -1)
        - 딕셔너리: 키의 인덱스 반환 (없으면 -1)
        """
        if isinstance(s, str) and isinstance(sub, str):
            idx = s.find(sub)
            return Token(data=Integer(idx), type=TokenType.INTEGER)
        elif isinstance(s, List):
            try:
                idx = s.index(sub)
                return Token(data=Integer(idx), type=TokenType.INTEGER)
            except ValueError:
                return Token(data=Integer(-1), type=TokenType.INTEGER)
        elif isinstance(s, Dict):
            keys = list(s.keys())
            try:
                idx = keys.index(sub)
                return Token(data=Integer(idx), type=TokenType.INTEGER)
            except ValueError:
                return Token(data=Integer(-1), type=TokenType.INTEGER)
        else:
            StringFunctions.executor.log_command("ERROR", "INDEX_OF()는 문자열, 리스트, 딕셔너리에만 적용됩니다")
            raise KavanaTypeError("INDEX_OF()는 문자열, 리스트, 딕셔너리에만 적용됩니다")    

    @staticmethod
    def TO_INT(s: Union[str, float]) -> Token:
        '''
        문자열 또는 실수를 정수로 변환합니다.
        
        예:
        TO_INT("42") → 42
        TO_INT("-10") → -10
        TO_INT(3.14) → 3
        
        잘못된 입력 예:
        TO_INT("abc") → 오류 발생
        '''
        if isinstance(s, float):
            return Token(data=Integer(int(s)), type="INTEGER")
        elif isinstance(s, str):
            try:
                return Token(data=Integer(int(s)), type="INTEGER")
            except KavanaValueError as e:
                StringFunctions.executor.log_command("ERROR", f"TO_INT() 함수 변환 에러: {e}")
                raise KavanaValueError(f"TO_INT() 함수 변환 에러: {e}")
        else:
            StringFunctions.executor.log_command("ERROR", "TO_INT() 함수는 문자열 또는 실수만 받을 수 있습니다")
            raise KavanaTypeError("TO_INT() 함수는 문자열 또는 실수만 받을 수 있습니다")
        
    @staticmethod
    def TO_FLOAT(s: Union[str, int]) -> Token:
        '''
        문자열 또는 정수를 실수(float)로 변환합니다.
        
        예:
        TO_FLOAT("3.14") → 3.14
        TO_FLOAT(-2) → -2.0
        
        잘못된 입력 예:
        TO_FLOAT("hello") → 오류 발생
        '''
        if isinstance(s, int):
            return Token(data=Float(float(s)), type="FLOAT")
        elif isinstance(s, str):
            try:
                f = float(s)
                return Token(data=Float(f), type="FLOAT")
            except KavanaValueError as e:
                StringFunctions.executor.log_command("ERROR", f"TO_FLOAT() 함수 변환 예러: {e}")
                raise KavanaValueError(f"TO_FLOAT() 함수 변환 예러: {e}")
        else:
            StringFunctions.executor.log_command("ERROR", "TO_FLOAT() 함수는 문자열 또는 정수만 받을 수 있습니다")
            raise KavanaTypeError("TO_FLOAT() 함수는 문자열 또는 정수만 받을 수 있습니다")

    def TO_STR(s: Any) -> Token:
        """
        주어진 값을 문자열로 변환합니다.
        
        Args:
            s (Any): 변환할 값.
        
        Returns:
            Token: 문자열로 변환된 결과를 포함하는 Token 객체.
        """
        if isinstance(s, str):
            return StringToken(data=String(s), type=TokenType.STRING)
        elif isinstance(s, (int, float)):
            return StringToken(data=String(str(s)), type=TokenType.STRING)
        elif isinstance(s, bool):
            return StringToken(data=String(str(s)), type=TokenType.STRING)
        elif isinstance(s, List):
            # 리스트를 문자열로 변환 (예: ["a", "b", "c"] -> "['a', 'b', 'c']")
            return StringToken(data=String(str(s)), type=TokenType.STRING)
        elif isinstance(s, Dict):
            # 딕셔너리를 문자열로 변환 (예: {"a": 1, "b": 2} -> "{'a': 1, 'b': 2}")
            return StringToken(data=String(str(s)), type=TokenType.STRING)
        elif s is None: 
            return StringToken(data=String(""), type=TokenType.STRING)
        else:
            StringFunctions.executor.log_command("ERROR", "TO_STR() 함수는 문자열, 정수, 실수, 불리언, 배열과 해쉬맵만 받을 수 있습니다")
            raise KavanaTypeError("TO_STR() 함수는 문자열, 정수, 실수, 불리언, 배열과 해쉬맵만 받을 수 있습니다")
        
    @staticmethod
    def REG_EX(s: str, pattern: str) -> Token:
        """
        문자열에서 정규 표현식 패턴을 찾아서 일치되는 것 문자열 리턴 없으면 None리턴
        
        Args:
            s (str): 검색할 문자열.
            pattern (str): 정규 표현식 패턴.
        
        Returns:
            Token: 패턴에 해당하는 문자열 리턴
        """
        import re
        if isinstance(s, str) and isinstance(pattern, str):
            match = re.search(pattern, s)
            if match:
                return StringToken(data=String(match.group()), type=TokenType.STRING)
            else:
                return StringToken(data=String(""), type=TokenType.STRING)
        StringFunctions.executor.log_command("ERROR", "형식은 REG_EX(문자열, 정규표현식)입니다")
        raise KavanaTypeError("형식은 REG_EX(문자열, 정규표현식)입니다")

    @staticmethod
    def MAKE_SQL(sql_template: str, data: dict) -> str:
        # 1. ? 개수 파악
        placeholders = re.findall(r'\?', sql_template)
        num_params = len(placeholders)

        # 2. 필요한 데이터만 앞에서부터 추출
        values = list(data.values())[:num_params]

        # 3. escape 포함한 SQL 값 포맷 함수
        def sql_format(val):
            if val is None:
                return "NULL"
            elif isinstance(val, (int, float)):
                return str(val)
            else:
                # 문자열 escape 처리
                escaped = str(val).replace("'", "''")
                return f"'{escaped}'"

        # 4. 각 ? 자리에 순서대로 대입
        formatted_values = [sql_format(v) for v in values]
        for val in formatted_values:
            sql_template = sql_template.replace("?", val, 1)

        return StringToken(data=String(sql_template), type=TokenType.STRING)
