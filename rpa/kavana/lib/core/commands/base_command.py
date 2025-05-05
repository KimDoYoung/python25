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
                
        return result
    
    def array_token_to_list(self, token: Token, executor) -> list:
        """ArrayToken을 list로 변환"""
        if not isinstance(token, Token) or token.type != TokenType.ARRAY:
            raise KavanaSyntaxError("ArrayToken이 아닙니다.")
        
        result = []
        for express in token.element_expresses:
            result.append(ExprEvaluator(executor=executor).evaluate(express).data.value)
        return result
    
    def get_option_spec(self, sub_command: str):
        '''subcommand에 따른 옵션 사양을 반환, overrides는 옵션 정의를 덮어씀'''
        spec = self.COMMAND_SPECS.get(sub_command)
        if not spec:
            raise KavanaValueError(f"지원하지 않는 sub_command: {sub_command}")

        keys = spec.get("keys", [])
        overrides = spec.get("overrides", {})
        rules = spec.get("rules", {})

        option_map = self._resolve_option_definitions(
            option_keys=keys,
            base_definitions=self.OPTION_DEFINITIONS,
            overrides=overrides
        )

        return option_map, rules
    def parse_and_validate_options(self, user_options: dict, option_map: dict, executor) -> dict:
        """
          입력받은 user_options를 option_map의 rule 기준으로 검증하고 최종 값 딕셔너리를 리턴한다.
        """
        option_values = {}

        # 1. 'with=' 병합 처리
        if 'with' in user_options:
            var_name_express = user_options['with']["express"]
            hashmap_token = ExprEvaluator(executor=executor).evaluate(var_name_express)
            with_values = self.hashmap_token_to_dict(hashmap_token, executor)
            option_values.update(with_values)
            del user_options['with']

        # 2. 개별 옵션 평가 및 타입 체크
        for key, value_dict in user_options.items():
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

    def check_option_rules(self, subcommand: str, params: dict, rules: dict):
        ''' rules에 따라 옵션 검증 '''
        for group in rules.get("mutually_exclusive", []):
            present = [key for key in group if key in params]
            if len(present) > 1:
                raise KavanaValueError(f"{subcommand} 옵션 충돌: {', '.join(present)} 는 동시에 사용할 수 없습니다.")

        for group in rules.get("required_together", []):
            present = [key for key in group if key in params]
            if 0 < len(present) < len(group):
                missing = [key for key in group if key not in params]
                raise KavanaValueError(f"{subcommand} 옵션 부족: {', '.join(group)} 는 함께 지정해야 합니다. 누락: {', '.join(missing)}")

        for group in rules.get("at_least_one", []):
            present = [key for key in group if key in params]
            if len(present) == 0:
                raise KavanaValueError(f"{subcommand} 명령어는 다음 중 최소 하나가 필요합니다: {', '.join(group)}")

        for group in rules.get("exactly_one", []):
            present = [key for key in group if key in params]
            if len(present) != 1:
                raise KavanaValueError(f"{subcommand} 명령어는 다음 중 정확히 하나만 지정해야 합니다: {', '.join(group)}")

    def _resolve_option_definitions(self, option_keys, base_definitions, overrides):
        result = {}
        for key in option_keys:
            if key not in base_definitions:
                raise KavanaValueError(f"정의되지 않은 옵션 키: {key}")
            base = copy.deepcopy(base_definitions[key])
            override = overrides.get(key, {})
            result[key] = {**base, **override}
        return result

