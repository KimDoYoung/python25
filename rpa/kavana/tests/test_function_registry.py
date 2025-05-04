# tests/test_function_registry.py

import pytest
from lib.core.function_registry import FunctionRegistry
from lib.core.exceptions.kavana_exception import KavanaValueError


def test_register_and_get_user_function():
    FunctionRegistry.user_functions = {}  # ✅ 테스트 격리

    func_name = "my_func"
    params = ["x", "y"]
    body = [{"cmd": "PRINT", "args": ["x", "y"]}]
    
    FunctionRegistry.register_function(func_name, params, body)
    result = FunctionRegistry.get_function(func_name)

    assert result["type"] == "user"
    assert result["name"] == func_name.upper()
    assert result["func"] == body
    assert result["arg_count"] == len(params)
    assert result["arg_names"] == params


def test_get_builtin_function():
    # ✅ 테스트는 내장 함수 중 하나를 이용 (예: LEN)
    func_info = FunctionRegistry.get_function("LENGTH")
    assert func_info is not None
    assert func_info["type"] == "builtin"
    assert callable(func_info["func"])
    assert isinstance(func_info["arg_count"], int)


def test_register_function_with_builtin_name_raises():
    builtin_name = "LENGTH"
    with pytest.raises(KavanaValueError) as exc_info:
        FunctionRegistry.register_function(builtin_name, ["x"], [{"cmd": "PRINT"}])
    
    assert "Cannot override built-in function" in str(exc_info.value)


def test_get_function_returns_none_for_unknown():
    result = FunctionRegistry.get_function("UNKNOWN_FUNCTION_123")
    assert result is None
