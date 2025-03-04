from lib.core.datatypes.list_type import ListType
from lib.core.token import Token
from lib.core.token_type import TokenType
class VariableManager:
    def __init__(self):
        self.global_vars = {}  # 전역 변수 저장소
        self.local_vars_stack = []  # 지역 변수 스택 (함수 호출 시 사용)

    def set_variable(self, var_name: str, token:Token, local=False):
        """변수 설정 (지역/전역 변수 구분), Token을 저장"""
        var_name = var_name.upper()  # ✅ 대소문자 무시

        # if token.type == TokenType.LIST:   # isinstance(token.value, list):
        #     list_obj = ListType(*token.data.value)  # ListType으로 변환
        #     token = Token(value=list_obj, type=TokenType.LIST, line=token.line, column=token.column)  # 변환된 ListType을 Token으로 래핑

        if local and self.local_vars_stack:
            self.local_vars_stack[-1][var_name] = token  # 지역 변수 저장
        else:
            self.global_vars[var_name] = token  # 전역 변수 저장

    def get_variable(self, name: str)->Token:
        """변수 조회 (지역 변수를 먼저 찾고, 없으면 전역 변수에서 찾기)"""
        name = name.upper()  # ✅ 대소문자 무시
        for scope in reversed(self.local_vars_stack):
            if name in scope:
                return scope[name]
        return self.global_vars.get(name, None)

    def push_local_scope(self):
        """새로운 지역 변수 스코프 추가 (함수 호출 시)"""
        self.local_vars_stack.append({})

    def pop_local_scope(self):
        """지역 변수 스코프 제거 (함수 종료 시)"""
        if self.local_vars_stack:
            self.local_vars_stack.pop()

