from abc import ABC, abstractmethod
from typing import List

from lib.core.exceptions.kavana_exception import KavanaSyntaxError
from lib.core.token import Token
from lib.core.token_type import TokenType

class BaseCommand(ABC):
    """
    모든 명령어 클래스가 상속해야 하는 기본 인터페이스
    """
    @abstractmethod
    def execute(self, args, executor):
        pass

    def count_express(tokens: List[Token]) -> int:
            """
            tokens 리스트에서 ','(COMMA)의 개수를 세고, 괄호나 대괄호 안에 있는 경우 제외.
            - 괄호 내부의 ','는 무시함.
            - ','가 없으면 1을 반환, 있으면 ',' 개수 + 1을 반환.
            """
            count = 0
            paren_depth = 0  # 괄호 깊이 확인
            bracket_depth = 0  # 대괄호 깊이 확인
            
            for token in tokens:
                if token.type == TokenType.LEFT_PAREN:
                    paren_depth += 1
                elif token.type == TokenType.RIGHT_PAREN:
                    paren_depth -= 1
                elif token.type == TokenType.LEFT_BRACKET:
                    bracket_depth += 1
                elif token.type == TokenType.RIGHT_BRACKET:
                    bracket_depth -= 1
                elif token.type == TokenType.COMMA and paren_depth == 0 and bracket_depth == 0:
                    count += 1
            
            return count + 1 if count > 0 else 1

    def is_key_exists(tokens: List[Token], key: str) -> bool:
        """
        tokens 리스트에서 특정 key가 '=' (ASSIGN) 왼쪽에 존재하는지 확인.
        - 괄호 ()나 대괄호 [] 안에 있는 경우 제외.
        - key가 존재하면 True, 없으면 False 반환.
        """
        paren_depth = 0  # 괄호 깊이
        bracket_depth = 0  # 대괄호 깊이
        
        for i in range(1, len(tokens)):
            token = tokens[i]
            
            if token.type == TokenType.LEFT_PAREN:
                paren_depth += 1
            elif token.type == TokenType.RIGHT_PAREN:
                paren_depth -= 1
            elif token.type == TokenType.LEFT_BRACKET:
                bracket_depth += 1
            elif token.type == TokenType.RIGHT_BRACKET:
                bracket_depth -= 1
            
            if token.type == TokenType.ASSIGN and paren_depth == 0 and bracket_depth == 0:
                prev_token = tokens[i - 1]
                if prev_token.type == TokenType.IDENTIFIER and prev_token.data.string == key:
                    return True
        
        return False    
    
    def extract_command_option(tokens: list[Token], start_index: int) -> tuple[Token, List[Token], int]:
        """
        주어진 토큰 리스트에서 key=<express> 구조를 파싱하는 함수
        - key는 IDENTIFIER 토큰으로 시작해야 함
        - '=' 연산자가 반드시 있어야 함
        - express는 TokenType.COMMA 또는 tokens의 끝까지
        - next_index 반환 (다음 key-express 파싱을 위한 인덱스)
        """
        if start_index >= len(tokens):
            return None, None, start_index
        
        key_token = tokens[start_index]
        if key_token.type != TokenType.IDENTIFIER:
            raise KavanaSyntaxError("명령어의 옵션 키는 IDENTIFIER 타입이어야 합니다.")
        
        if start_index + 1 >= len(tokens) or tokens[start_index + 1].type != TokenType.ASSIGN:
            raise KavanaSyntaxError(f"옵션 '{key_token.data.string}' 뒤에 '=' 연산자가 필요합니다.")
        
        expresses = []
        i = start_index + 2  # '=' 다음 토큰부터 시작
        while i < len(tokens):
            token = tokens[i]
            if token.type == TokenType.COMMA:
                i += 1  # 다음 key-value로 이동하기 위해 인덱스 증가
                break
            expresses.append(token)
            i += 1
        
        if not expresses:
            raise KavanaSyntaxError(f"옵션 '{key_token.data.string}'의 값이 없습니다.")
        
        return key_token, expresses, i


    def get_express(self, tokens, start_idx):
        """
        주어진 tokens에서 start_idx부터 시작하여 ',' 또는 끝까지 표현식을 추출하는 함수
        괄호 (), 대괄호 [] 깊이를 고려하여 올바르게 표현식을 분리함.
        """
        if start_idx >= len(tokens):
            return start_idx, []
        
        expresses = []
        paren_depth = 0  # 괄호 깊이
        bracket_depth = 0  # 대괄호 깊이
        
        i = start_idx
        while tokens[i].type == TokenType.COMMA:
            i += 1

        while i < len(tokens):
            token = tokens[i]
            if token.type == TokenType.LEFT_PAREN:
                paren_depth += 1
            elif token.type == TokenType.RIGHT_PAREN:
                paren_depth -= 1
            elif token.type == TokenType.LEFT_BRACKET:
                bracket_depth += 1
            elif token.type == TokenType.RIGHT_BRACKET:
                bracket_depth -= 1
            elif token.type == TokenType.COMMA and paren_depth == 0 and bracket_depth == 0:
                return i + 1, expresses  # ','를 만나면 표현식 종료
            
            expresses.append(token)
            i += 1
        
        return i, expresses
    
    def extract_all_options(self, tokens: List[Token], start_idx: int):
        """
        주어진 tokens 리스트에서 key=value 옵션을 모두 추출하는 함수.
        - key는 IDENTIFIER
        - '=' 연산자가 반드시 있어야 함
        - value는 ',' 또는 tokens 끝까지 표현식을 포함
        """
        options = {}
        i = start_idx
        
        while i < len(tokens):
            key_token, express_tokens, next_index = self.extract_command_option(tokens, i)
            if key_token is None:
                break
            key = key_token.data.string.strip().lower()
            options[key] = {"key_token": key_token, "express": express_tokens}
            i = next_index
        
        return options, i    