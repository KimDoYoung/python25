"""
FunctionRegistry 클래스를 위한 단위 테스트
"""

import pytest
import sys
from unittest.mock import patch, MagicMock
from io import StringIO
import copy

# 테스트할 모듈 import (모킹 없이)
from lib.core.function_registry import FunctionRegistry
from lib.core.exceptions.kavana_exception import KavanaValueError

class TestFunctionRegistry:
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """각 테스트 전후에 FunctionRegistry 상태를 저장하고 복원"""
        # 원래 상태 저장
        self.original_builtin_functions = copy.deepcopy(FunctionRegistry.builtin_functions)
        self.original_user_functions = copy.deepcopy(FunctionRegistry.user_functions)
        
        # 테스트용 내장 함수 추가 (기존 내장 함수는 유지)
        FunctionRegistry.builtin_functions['TEST_PRINT'] = (lambda x: print(x), 1)
        FunctionRegistry.builtin_functions['TEST_SUM'] = (lambda a, b: a + b, 2)
        
        yield
        
        # 테스트 후 원래 상태로 복원
        FunctionRegistry.builtin_functions = self.original_builtin_functions
        FunctionRegistry.user_functions = self.original_user_functions
    
    def test_register_function(self):
        """사용자 정의 함수 등록 테스트"""
        # 테스트 데이터
        func_name = "TEST_FUNC"
        params = ["x", "y"]
        body = [{"command": "ADD", "args": ["x", "y"]}]
        
        # 함수 등록
        FunctionRegistry.register_function(func_name, params, body)
        
        # 등록 확인
        assert "TEST_FUNC" in FunctionRegistry.user_functions
        assert FunctionRegistry.user_functions["TEST_FUNC"]["params"] == params
        assert FunctionRegistry.user_functions["TEST_FUNC"]["body"] == body
    
    def test_register_function_case_insensitive(self):
        """함수명 대소문자 구분 없음 테스트"""
        # 테스트 데이터
        func_name = "test_func"  # 소문자로 등록
        params = ["x"]
        body = [{"command": "TEST_PRINT", "args": ["x"]}]
        
        # 함수 등록
        FunctionRegistry.register_function(func_name, params, body)
        
        # 대문자로 확인
        assert "TEST_FUNC" in FunctionRegistry.user_functions
        assert FunctionRegistry.user_functions["TEST_FUNC"]["params"] == params
        assert FunctionRegistry.user_functions["TEST_FUNC"]["body"] == body
    
    def test_register_builtin_function_error(self):
        """내장 함수와 이름 충돌 시 예외 발생 테스트"""
        # 내장 함수명으로 등록 시도
        with pytest.raises(KavanaValueError) as excinfo:
            FunctionRegistry.register_function("TEST_PRINT", ["x"], [])
        
        # 오류 메시지 검증
        assert "Cannot override built-in function" in str(excinfo.value)
        
        # 내장 함수명 (소문자)으로 등록 시도
        with pytest.raises(KavanaValueError) as excinfo:
            FunctionRegistry.register_function("test_print", ["x"], [])
        
        # 오류 메시지 검증
        assert "Cannot override built-in function" in str(excinfo.value)
    
    def test_get_builtin_function(self):
        """내장 함수 조회 테스트"""
        # 내장 함수 조회
        func_info = FunctionRegistry.get_function("TEST_PRINT")
        
        # 반환값 검증
        assert func_info["type"] == "builtin"
        assert func_info["name"] == "TEST_PRINT"
        assert func_info["arg_count"] == 1
        assert callable(func_info["func"])
        assert func_info["arg_names"] == []
        
        # 대소문자 구분 없이 조회
        func_info = FunctionRegistry.get_function("test_print")
        assert func_info["name"] == "TEST_PRINT"
    
    def test_get_user_function(self):
        """사용자 정의 함수 조회 테스트"""
        # 사용자 함수 등록
        func_name = "CUSTOM_FUNC"
        params = ["a", "b", "c"]
        body = [{"command": "ADD", "args": ["a", "b", "c"]}]
        FunctionRegistry.register_function(func_name, params, body)
        
        # 사용자 함수 조회
        func_info = FunctionRegistry.get_function("CUSTOM_FUNC")
        
        # 반환값 검증
        assert func_info["type"] == "user"
        assert func_info["name"] == "CUSTOM_FUNC"
        assert func_info["arg_count"] == 3
        assert func_info["func"] == body
        assert func_info["arg_names"] == params
        
        # 대소문자 구분 없이 조회
        func_info = FunctionRegistry.get_function("custom_func")
        assert func_info["name"] == "CUSTOM_FUNC"
    
    def test_get_nonexistent_function(self):
        """존재하지 않는 함수 조회 테스트"""
        # 존재하지 않는 함수 조회
        func_info = FunctionRegistry.get_function("NONEXISTENT")
        
        # None 반환 확인
        assert func_info is None
    
    def test_print_user_functions(self):
        """사용자 정의 함수 출력 테스트"""
        # 사용자 함수 등록
        FunctionRegistry.register_function("FUNC1", ["x"], [{"command": "TEST_PRINT", "args": ["x"]}])
        FunctionRegistry.register_function("FUNC2", ["a", "b"], [{"command": "ADD", "args": ["a", "b"]}])
        
        # 표준 출력 리다이렉션 (patch 사용하여 안전하게 처리)
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            # 함수 출력
            FunctionRegistry.print_user_functions()
            
            # 출력 검증
            output = mock_stdout.getvalue()
            assert "FUNC1(x)" in output
            assert "FUNC2(a, b)" in output
    
    def test_multiple_registrations(self):
        """다중 함수 등록 및 관리 테스트"""
        # 여러 함수 등록
        FunctionRegistry.register_function("FUNC_A", ["x"], [])
        FunctionRegistry.register_function("FUNC_B", ["y"], [])
        FunctionRegistry.register_function("FUNC_C", ["z"], [])
        
        # 등록된 함수 수 확인
        assert len(FunctionRegistry.user_functions) >= 3  # 기존에 함수가 있을 수 있으므로 >= 사용
        
        # 함수별 파라미터 확인
        assert FunctionRegistry.get_function("FUNC_A")["arg_names"] == ["x"]
        assert FunctionRegistry.get_function("FUNC_B")["arg_names"] == ["y"]
        assert FunctionRegistry.get_function("FUNC_C")["arg_names"] == ["z"]

if __name__ == "__main__":
    pytest.main(["-v", "test_function_registry.py"])