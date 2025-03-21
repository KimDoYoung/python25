from abc import ABC, abstractmethod
from typing import List

from lib.core.exceptions.kavana_exception import KavanaSyntaxError
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.token import Token
from lib.core.token_type import TokenType

class BaseCommand(ABC):
    """
    모든 명령어 클래스가 상속해야 하는 기본 인터페이스
    """
    @abstractmethod
    def execute(self, args, executor):
        pass

    def count_express(self, tokens: List[Token]) -> int:
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

    def is_key_exists(self, tokens: List[Token], key: str) -> bool:
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
        {
            "limit": {
                "key_token": Token(IDENTIFIER, 'limit'),
                "express": [Token(INTEGER, '100')]
            },
            "offset": {
                "key_token": Token(IDENTIFIER, 'offset'),
                "express": [Token(INTEGER, '20')]
            }
        }        
        """
        options = {}
        i = start_idx
        
        while i < len(tokens):
            key_token, express_tokens, next_index = self.extract_option1(tokens, i)
            if key_token is None:
                break
            key = key_token.data.string.strip().lower()
            options[key] = {"key_token": key_token, "express": express_tokens}
            i = next_index
        
        return options, i    
    
    def extract_option1(self, tokens: list[Token], start_index: int) -> tuple[Token, List[Token], int]:
        """
        - key=express 파싱
        - 괄호 안의 =, , 는 무시
        - key는 = 앞의 토큰
        - express는 = 뒤부터 괄호 고려해서 , 또는 끝까지
        """
        if start_index >= len(tokens):
            return None, None, start_index

        # 괄호 스택을 사용해 중첩 추적
        bracket_stack = []
        assign_index = -1
        i = start_index

        # 1. ASSIGN(=) 토큰 찾기 (괄호 밖에서)
        while i < len(tokens):
            token = tokens[i]

            if token.type in (TokenType.LEFT_PAREN, TokenType.LEFT_BRACKET):
                bracket_stack.append(token.type)
            elif token.type == TokenType.RIGHT_PAREN:
                if bracket_stack and bracket_stack[-1] == TokenType.LEFT_PAREN:
                    bracket_stack.pop()
                else:
                    raise KavanaSyntaxError("괄호 '(' 와 ')'가 맞지 않습니다.")
            elif token.type == TokenType.RIGHT_BRACKET:
                if bracket_stack and bracket_stack[-1] == TokenType.LEFT_BRACKET:
                    bracket_stack.pop()
                else:
                    raise KavanaSyntaxError("괄호 '[' 와 ']'가 맞지 않습니다.")
            elif token.type == TokenType.ASSIGN and not bracket_stack:
                assign_index = i
                break

            i += 1

        if assign_index == -1:
            raise KavanaSyntaxError("옵션에 '=' 연산자가 없습니다.")

        if assign_index == start_index:
            raise KavanaSyntaxError("'=' 앞에 key 토큰이 없습니다.")

        key_token = tokens[assign_index - 1]
        if key_token.type != TokenType.IDENTIFIER:
            raise KavanaSyntaxError("옵션의 key는 IDENTIFIER 타입이어야 합니다.")

        # 2. express 수집 (괄호 안의 , 는 무시)
        expresses = []
        i = assign_index + 1
        bracket_stack.clear()

        while i < len(tokens):
            token = tokens[i]

            if token.type in (TokenType.LEFT_PAREN, TokenType.LEFT_BRACKET):
                bracket_stack.append(token.type)
            elif token.type == TokenType.RIGHT_PAREN:
                if bracket_stack and bracket_stack[-1] == TokenType.LEFT_PAREN:
                    bracket_stack.pop()
                else:
                    raise KavanaSyntaxError("괄호 '(' 와 ')'가 맞지 않습니다.")
            elif token.type == TokenType.RIGHT_BRACKET:
                if bracket_stack and bracket_stack[-1] == TokenType.LEFT_BRACKET:
                    bracket_stack.pop()
                else:
                    raise KavanaSyntaxError("괄호 '[' 와 ']'가 맞지 않습니다.")

            # 괄호 밖에서 , 만나면 종료
            if token.type == TokenType.COMMA and not bracket_stack:
                i += 1  # 다음 옵션으로 넘어가기 위해 인덱스 증가
                break

            expresses.append(token)
            i += 1

        if not expresses:
            raise KavanaSyntaxError(f"옵션 '{key_token.data.string}'의 값이 없습니다.")

        return key_token, expresses, i


    def parse_and_validate_options(self, options: dict, option_map: dict, executor) -> dict:
        """
        주어진 options를 option_map 기준으로 검증하고 최종 값 딕셔너리를 리턴한다.
        - 타입 체크, required 체크, default 적용 포함
        options, i = self.extract_all_options(args, 0)

        option_map = {
            "count": {"default": 1, "allowed_types": [TokenType.INTEGER]},
            "duration": {"default": 0.2, "allowed_types": [TokenType.FLOAT]},
            "type": {"default": "single", "allowed_types": [TokenType.STRING]},
            "x": {"required": True, "allowed_types": [TokenType.INTEGER]},
        }

        option_values = parse_and_validate_options(options, option_map, executor)        
        """
        option_values = {}

        # 1. 주어진 옵션 해석 및 타입 체크
        for key, value_dict in options.items():
            if key not in option_map:
                raise KavanaSyntaxError(f"알 수 없는 옵션: '{key}'")

            value_express = value_dict["express"]
            evaluated = ExprEvaluator(executor=executor).evaluate(value_express)

            allowed_types = option_map[key].get("allowed_types", [])
            if evaluated.type not in allowed_types:
                raise KavanaSyntaxError(
                    f"옵션 '{key}'의 타입이 올바르지 않습니다. "
                    f"허용된 타입: {', '.join(t.name for t in allowed_types)}, "
                    f"실제 타입: {evaluated.type.name}"
                )

            option_values[key] = evaluated.data.value

        # 2. 필수 옵션 누락 체크
        for key, opt in option_map.items():
            if opt.get("required", False) and key not in option_values:
                raise KavanaSyntaxError(f"필수 옵션 '{key}'가 누락되었습니다.")

        # 3. 기본값 적용
        for key, opt in option_map.items():
            if key not in option_values and "default" in opt:
                option_values[key] = opt["default"]

        return option_values
