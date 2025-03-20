from lib.core.const_registry import ConstantRegistry
from lib.core.datatypes.kavana_datatype import String
from lib.core.datatypes.list_type import ListType
from lib.core.token import Token
from lib.core.token_type import TokenType
class VariableManager:
    """✅ 변수 및 `CONST` 관리"""

    def __init__(self):
        self.global_vars = {}  
        self.local_vars_stack = []
        self.global_vars["$$LastError"] = Token(data=String(""), type=TokenType.STRING)

    def set_variable(self, var_name: str, token: Token, local=False):
        """✅ 변수 설정 (`CONST` 변경 불가)"""
        var_name = var_name.upper()

        # ✅ `CONST` 변경 금지
        if ConstantRegistry.is_constant(var_name):
            raise ValueError(f"CONST {var_name} can not change")

        if local and self.local_vars_stack:
            self.local_vars_stack[-1][var_name] = token
        else:
            self.global_vars[var_name] = token

    def get_variable(self, var_name: str):
        """✅ 변수를 먼저 찾고, 없으면 `CONST`에서 조회"""
        var_name = var_name.upper()

        # ✅ 지역 변수 확인
        if self.local_vars_stack:
            for scope in reversed(self.local_vars_stack):
                if var_name in scope:
                    return scope[var_name]

        # ✅ 전역 변수 확인
        if var_name in self.global_vars:
            return self.global_vars[var_name]

        # ✅ `CONST`에서 조회
        return ConstantRegistry.get(var_name)

    def has_variable(self, var_name: str):
        """✅ 변수 또는 `CONST` 여부 확인"""
        var_name = var_name.upper()
        return (
            any(var_name in scope for scope in self.local_vars_stack) or
            var_name in self.global_vars or
            ConstantRegistry.is_constant(var_name)
        )

    def set_const(self, name: str, value: Token):
        """✅ `CONST` 등록 (한 번만 설정 가능)"""
        name = name.upper()
        ConstantRegistry.define_constant(name, value)

# class VariableManager:
#     def __init__(self):
#         self.global_vars = {}  # 전역 변수 저장소
#         self.local_vars_stack = []  # 지역 변수 스택 (함수 호출 시 사용)

#     def set_variable(self, var_name: str, token:Token, local=False):
#         """변수 설정 (지역/전역 변수 구분), Token을 저장"""
#         var_name = var_name.upper()  # ✅ 대소문자 무시

#         if local and self.local_vars_stack:
#             self.local_vars_stack[-1][var_name] = token  # 지역 변수 저장
#         else:
#             self.global_vars[var_name] = token  # 전역 변수 저장

#     def get_variable(self, name: str)->Token:
#         """변수 조회 (지역 변수를 먼저 찾고, 없으면 전역 변수에서 찾기)"""
#         name = name.upper()  # ✅ 대소문자 무시
#         for scope in reversed(self.local_vars_stack):
#             if name in scope:
#                 return scope[name]
#         token = self.global_vars.get(name, None)
#         if token is None:
#             return ConstantRegistry.get(name)  # ✅ CONST에서 조회

#     def push_local_scope(self):
#         """새로운 지역 변수 스코프 추가 (함수 호출 시)"""
#         self.local_vars_stack.append({})

#     def pop_local_scope(self):
#         """지역 변수 스코프 제거 (함수 종료 시)"""
#         if self.local_vars_stack:
#             self.local_vars_stack.pop()

