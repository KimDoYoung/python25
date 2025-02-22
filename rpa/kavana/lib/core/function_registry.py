import re
import operator
from typing import List, Union
from datetime import datetime, timedelta
from lib.core.variable_manager import VariableManager
from lib.core.builtin_functions import BuiltinFunctions

class FunctionRegistry:
    """내장 함수 및 사용자 정의 함수를 관리하는 클래스"""
    builtin_functions = {name.upper(): func for name, func in BuiltinFunctions.__dict__.items() if callable(func)}
    user_functions = {}

    @staticmethod
    def register_function(name: str, param_names: list, func_body: str):
        """사용자 정의 함수 등록 (내장 함수 이름과 중복 방지)"""
        name_upper = name.upper()
        if name_upper in FunctionRegistry.builtin_functions:
            raise ValueError(f"Cannot override built-in function: {name}")
        FunctionRegistry.user_functions[name_upper] = {"params": param_names, "body": func_body}

    @staticmethod
    def get_function(name: str):
        """함수 가져오기 (내장 함수 + 사용자 정의 함수 포함)"""
        name_upper = name.upper()
        if name_upper in FunctionRegistry.builtin_functions:
            return FunctionRegistry.builtin_functions[name_upper]  # 내장 함수 반환
        if name_upper in FunctionRegistry.user_functions:
            return FunctionRegistry.user_functions[name_upper]  # 사용자 함수 반환
        return None
