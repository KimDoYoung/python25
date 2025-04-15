from abc import ABC, abstractmethod
import copy
from typing import List

from lib.core.exceptions.kavana_exception import KavanaSyntaxError, KavanaValueError
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.token import ArrayToken, HashMapToken, Token
from lib.core.token_type import TokenType
from lib.core.token_util import TokenUtil

class BaseCommand(ABC):
    """
    모든 명령어(Command) 클래스가 상속해야 하는 기본 인터페이스
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
        
        return expresses, i
    
    def extract_all_options0(self, tokens: List[Token], start_idx: int):
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
    
    def extract_all_options(self, tokens: List[Token], start_idx: int):
        """
        주어진 tokens 리스트에서 key=value 옵션을 모두 추출하는 함수.
        key=value 옵션들을 ',' 없이도 연속적으로 추출
        다음 토큰이 IDENTIFIER, 그 다음이 ASSIGN(=)이면 새로운 옵션으로 간주
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

            # 기존에는 여기서 무조건 ','를 기대했음
            # 이제는 다음 토큰이 IDENTIFIER이고, 그 다음이 '='이면 새로운 옵션으로 간주
            if i + 1 < len(tokens):
                next_token = tokens[i]
                next_next_token = tokens[i + 1]

                if next_token.type == TokenType.IDENTIFIER and next_next_token.type == TokenType.ASSIGN:
                    continue  # ',' 없이도 다음 옵션으로 인식 → 루프 유지
                elif next_token.type == TokenType.COMMA:
                    i += 1  # ',' 건너뛰고 다음 옵션으로
                    continue

            break  # 다음에 IDENTIFIER= 가 없으면 옵션 추출 종료

        return options, i


    def extract_option1(self, tokens: list[Token], start_index: int) -> tuple[Token, List[Token], int]:
        """
        - key=express 파싱
        - 괄호 안의 =, , 는 무시
        - key는 = 앞의 토큰
        - express는 = 뒤부터 괄호 고려해서 ',' 또는 다음 IDENTIFIER= 또는 끝까지
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

            # ✅ 종료 조건 1: 괄호 밖에서 ',' 만나면 express 종료
            if token.type == TokenType.COMMA and not bracket_stack:
                i += 1
                break

            # ✅ 종료 조건 2: 괄호 밖에서 다음 토큰이 IDENTIFIER = 형태이면 express 종료
            if not bracket_stack and i + 1 < len(tokens):
                next_token = tokens[i]
                next_next_token = tokens[i + 1]
                if next_token.type == TokenType.IDENTIFIER and next_next_token.type == TokenType.ASSIGN:
                    break

            expresses.append(token)
            i += 1

        if not expresses:
            raise KavanaSyntaxError(f"옵션 '{key_token.data.string}'의 값이 없습니다.")

        return key_token, expresses, i

    def hashmap_token_to_dict(self, token: Token, executor) -> dict:
        """HashMapToken을 dict로 변환"""
        if not isinstance(token, Token) or token.type != TokenType.HASH_MAP:
            raise KavanaSyntaxError("HashMapToken이 아닙니다.")
        
        result = {}
        for key, express in token.key_express_map.items():
            if not isinstance(key, str):
                raise KavanaSyntaxError(f"잘못된 키 타입: {key} ({type(key)})")
            token = ExprEvaluator(executor=executor).evaluate(express)
            if token.type == TokenType.HASH_MAP:
                result[key] = self.hashmap_token_to_dict(token, executor)
            elif token.type == TokenType.ARRAY:
                result[key] = self.array_token_to_list(token, executor)
            else:
                result[key] = token.data.value
            # if isinstance(result[key], HashMapToken):
            #     result[key] = self.hashmap_token_to_dict(result[key], executor)
            # elif isinstance(result[key], ArrayToken):
            #     result[key] = self.array_token_to_list(result[key], executor)
                
        return result
    
    def array_token_to_list(self, token: Token, executor) -> list:
        """ArrayToken을 list로 변환"""
        if not isinstance(token, Token) or token.type != TokenType.ARRAY:
            raise KavanaSyntaxError("ArrayToken이 아닙니다.")
        
        result = []
        for express in token.element_expresses:
            result.append(ExprEvaluator(executor=executor).evaluate(express).data.value)
        return result
    

    def parse_and_validate_options(self, options: dict, option_map: dict, executor) -> dict:
        """
        주어진 options를 option_map 기준으로 검증하고 최종 값 딕셔너리를 리턴한다.
        - 타입 체크, required 체크, default 적용 포함
        - min/max, choices 검증 추가
        """
        option_values = {}

        # 1. 'with=' 병합 처리
        if 'with' in options:
            var_name_express = options['with']["express"]
            hashmap_token = ExprEvaluator(executor=executor).evaluate(var_name_express)
            with_values = self.hashmap_token_to_dict(hashmap_token, executor)
            option_values.update(with_values)
            del options['with']

        # 2. 개별 옵션 평가 및 타입 체크
        for key, value_dict in options.items():
            if key not in option_map:
                raise KavanaSyntaxError(f"알 수 없는 옵션: '{key}'")

            opt = option_map[key]
            value_express = value_dict["express"]
            evaluated = ExprEvaluator(executor=executor).evaluate(value_express)

            allowed_types = opt.get("allowed_types", [])
            if evaluated.type not in allowed_types:
                raise KavanaSyntaxError(
                    f"옵션 '{key}'의 타입이 올바르지 않습니다. "
                    f"허용된 타입: {', '.join(t.name for t in allowed_types)}, "
                    f"실제 타입: {evaluated.type.name}"
                )

            if evaluated.type == TokenType.HASH_MAP:
                option_values[key] = self.hashmap_token_to_dict(evaluated, executor)
            elif evaluated.type == TokenType.ARRAY:
                option_values[key] = self.array_token_to_list(evaluated, executor)
            else:
                option_values[key] = evaluated.data.value

            # 🔍 값 범위 체크 (min/max)
            if "min" in opt and option_values[key] < opt["min"]:
                raise KavanaSyntaxError(f"옵션 '{key}' 값은 최소 {opt['min']} 이상이어야 합니다.")
            if "max" in opt and option_values[key] > opt["max"]:
                raise KavanaSyntaxError(f"옵션 '{key}' 값은 최대 {opt['max']} 이하여야 합니다.")

            # 🔍 choices 체크 (열거형 제한)
            if "choices" in opt and option_values[key] not in opt["choices"]:
                raise KavanaSyntaxError(
                    f"옵션 '{key}' 값은 다음 중 하나여야 합니다: "
                    f"{', '.join(str(c) for c in opt['choices'])} "
                    f"(현재 값: {option_values[key]})"
                )

        # 3. 필수 옵션 누락 체크
        for key, opt in option_map.items():
            if opt.get("required", False) and key not in option_values:
                raise KavanaSyntaxError(f"필수 옵션 '{key}'가 누락되었습니다.")

        # 4. 기본값 적용
        for key, opt in option_map.items():
            if key not in option_values and "default" in opt:
                option_values[key] = opt["default"]

        return option_values


    def check_option_rules(self, subcommand: str, params: dict):
        ''' OPTION_RULES에 정의된 규칙을 체크한다.'''
        rules = getattr(self, "OPTION_RULES", {}).get(subcommand, {})

        # 1. 상호 배타 (mutually exclusive)
        for group in rules.get("mutually_exclusive", []):
            present = [key for key in group if key in params]
            if len(present) > 1:
                raise KavanaValueError(f"{subcommand} 옵션 충돌: {', '.join(present)} 는 동시에 사용할 수 없습니다.")

        # 2. 함께 있어야 함 (required together)
        for group in rules.get("required_together", []):
            present = [key for key in group if key in params]
            if 0 < len(present) < len(group):
                missing = [key for key in group if key not in params]
                raise KavanaValueError(f"{subcommand} 옵션 부족: {', '.join(group)} 는 함께 지정해야 합니다. 누락: {', '.join(missing)}")



    def _resolve_option_definitions(
        self,
        option_keys: list[str],
        base_definitions: dict,
        overrides: dict = None
    ) -> dict:
        if overrides is None:
            overrides = {}

        resolved = {}
        for key in option_keys:
            if key not in base_definitions:
                raise ValueError(f"정의되지 않은 옵션 키: {key}")
            base = copy.deepcopy(base_definitions[key])
            override = overrides.get(key, {})
            resolved[key] = {**base, **override}
        return resolved

    def get_option_definitions(self, sub_command: str) -> dict:
        """
        COMMAND_OPTION_MAP과 OPTION_DEFINITIONS를 기반으로
        명령어별 최종 옵션 정의 딕셔너리를 반환
        """
        config = self.COMMAND_OPTION_MAP.get(sub_command)
        if not config:
            raise ValueError(f"지원하지 않는 sub_command: {sub_command}")

        keys = config.get("keys", [])
        overrides = config.get("overrides", {})
        return self._resolve_option_definitions(keys, self.OPTION_DEFINITIONS, overrides)
