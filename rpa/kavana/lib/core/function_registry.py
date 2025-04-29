from typing import List
from lib.core.builtins.builtin_registry import BUILTIN_FUNCTIONS
from lib.core.exceptions.kavana_exception import KavanaValueError

class FunctionRegistry:
    """사용자함수의 본체를 저장"""
    builtin_functions = BUILTIN_FUNCTIONS.copy()
    user_functions = {}

    @staticmethod
    def register_function(name: str, param_names: list, func_body_commands: List[dict]):
        """사용자 정의 함수 등록 (내장 함수 이름과 중복 방지)"""
        name_upper = name.upper()
        if name_upper in FunctionRegistry.builtin_functions:
            raise KavanaValueError(f"Cannot override built-in function: {name}")

        FunctionRegistry.user_functions[name_upper] = {
            "params": param_names,
            "body": func_body_commands  # ✅ Token List의 List로 저장
        }

    @staticmethod
    def get_function(name: str):
        """함수 가져오기 (내장 함수 + 사용자 정의 함수 포함)"""
        name_upper = name.upper()

        if name_upper in FunctionRegistry.builtin_functions:
            func, arg_count = FunctionRegistry.builtin_functions[name_upper]
            return {
                "type": "builtin",
                "name" : name_upper,
                "func": func,
                "arg_count": arg_count,
                "arg_names": []
            }

        if name_upper in FunctionRegistry.user_functions:
            user_func = FunctionRegistry.user_functions[name_upper]
            return {
                "type": "user",
                "name" : name_upper,
                "func": user_func["body"],  # ✅ 문자열이 아닌 list[str]로 반환
                "arg_count": len(user_func["params"]),
                "arg_names": user_func["params"]
            }

        return None  # 함수가 없으면 None 반환

    @staticmethod
    def print_user_functions():
        """사용자 정의 함수 출력"""
        for name, info in FunctionRegistry.user_functions.items():
            print(f"{name}({', '.join(info['params'])})")