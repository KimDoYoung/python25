import pytest
from unittest.mock import Mock, patch
from lib.core.token import StringToken, Token
from lib.core.token_type import TokenType
from lib.core.datatypes.kavana_datatype import Integer, String
from lib.core.exceptions.kavana_exception import KavanaValueError
from lib.core.commands.database.db_commander import DbCommander
from lib.core.variable_manager import VariableManager

@pytest.fixture
def variable_manager():
    return VariableManager()

class TestVariableManager:
    
    def test_init(self, variable_manager):
        """초기화 테스트"""
        assert variable_manager.global_vars["_LastError_"].data.value == ""
        assert variable_manager.local_vars_stack == []
    
    def test_set_variable_global(self, variable_manager):
        """전역 변수 설정 테스트"""
        test_token = StringToken(data=String("test_value"), type=TokenType.STRING)
        variable_manager.set_variable("test_var", test_token)
        
        assert "TEST_VAR" in variable_manager.global_vars
        assert variable_manager.global_vars["TEST_VAR"].data.value == "test_value"
    
    def test_set_variable_local(self, variable_manager):
        """지역 변수 설정 테스트"""
        # 지역 변수 스택을 준비
        variable_manager.local_vars_stack.append({})
        
        test_token = StringToken(data=String("local_value"), type=TokenType.STRING)
        variable_manager.set_variable("local_var", test_token, local=True)
        
        assert "LOCAL_VAR" in variable_manager.local_vars_stack[-1]
        assert variable_manager.local_vars_stack[-1]["LOCAL_VAR"].data.value == "local_value"
    
    def test_set_const_variable_error(self, variable_manager):
        """상수 변경 시도 시 에러 테스트"""
        # 먼저 상수 등록
        test_token = StringToken(data=String("const_value"), type=TokenType.STRING)
        variable_manager.set_const("TEST_CONST", test_token)
        
        # 상수 변경 시도
        with pytest.raises(ValueError, match="CONST TEST_CONST can not change"):
            variable_manager.set_variable("TEST_CONST", StringToken(data=String("new_value"), type=TokenType.STRING))
    
    def test_get_variable_local(self, variable_manager):
        """지역 변수 조회 테스트"""
        # 지역 변수 설정
        variable_manager.local_vars_stack.append({"LOCAL_VAR": StringToken(data=String("local_value"), type=TokenType.STRING)})
        
        result = variable_manager.get_variable("LOCAL_VAR")
        assert result.data.value == "local_value"
    
    def test_get_variable_global(self, variable_manager):
        """전역 변수 조회 테스트"""
        # 전역 변수 설정
        variable_manager.global_vars["GLOBAL_VAR"] = StringToken(data=String("global_value"), type=TokenType.STRING)
        
        result = variable_manager.get_variable("GLOBAL_VAR")
        assert result.data.value == "global_value"
    
    def test_get_variable_const(self, variable_manager):
        """상수 조회 테스트"""
        # 상수 설정
        test_token = StringToken(data=String("const_value"), type=TokenType.STRING)
        variable_manager.set_const("TEST_CONST", test_token)
        
        result = variable_manager.get_variable("TEST_CONST")
        assert result.data.value == "const_value"
    
    def test_has_variable(self, variable_manager):
        """변수 존재 여부 테스트"""
        # 변수들 설정
        variable_manager.local_vars_stack.append({"LOCAL_VAR": StringToken(data=String("local_value"), type=TokenType.STRING)})
        variable_manager.global_vars["GLOBAL_VAR"] = StringToken(data=String("global_value"), type=TokenType.STRING)
        variable_manager.set_const("TEST_CONST", StringToken(data=String("const_value"), type=TokenType.STRING))
        
        assert variable_manager.has_variable("LOCAL_VAR") is True
        assert variable_manager.has_variable("GLOBAL_VAR") is True
        assert variable_manager.has_variable("TEST_CONST") is True
        assert variable_manager.has_variable("NON_EXISTENT") is False
    
    def test_nested_local_vars(self, variable_manager):
        """중첩된 지역 변수 스코프 테스트"""
        # 두 개의 지역 변수 스코프 설정
        variable_manager.local_vars_stack.append({"OUTER": StringToken(data=String("outer_value"), type=TokenType.STRING)})
        variable_manager.local_vars_stack.append({"INNER": StringToken(data=String("inner_value"), type=TokenType.STRING)})
        
        # 가장 안쪽 스코프의 변수 조회
        assert variable_manager.get_variable("INNER").data.value == "inner_value"
        
        # 바깥쪽 스코프의 변수 조회
        assert variable_manager.get_variable("OUTER").data.value == "outer_value"
    
    def test_local_shadowing_global(self, variable_manager):
        """지역 변수가 전역 변수를 가리는 테스트"""
        # 전역 변수 설정
        variable_manager.global_vars["TEST_VAR"] = StringToken(data=String("global_value"), type=TokenType.STRING)
        
        # 동일한 이름의 지역 변수 설정
        variable_manager.local_vars_stack.append({"TEST_VAR": StringToken(data=String("local_value"), type=TokenType.STRING)})
        
        # 지역 변수가 우선 반환되어야 함
        assert variable_manager.get_variable("TEST_VAR").data.value == "local_value"
    
    @patch('lib.core.variable_manager.ConstantRegistry')
    def test_load_built_in_constants(self, mock_registry, variable_manager):
        """내장 상수 로딩 테스트"""
        # 이미 초기화 시 호출되었으므로 다시 호출
        variable_manager.load_built_in_constants()
        
        # 각 Enum 타입별로 상수가 등록되었는지 확인
        assert mock_registry.define_constant.called
    
    @patch('lib.core.variable_manager.DatabaseRegistry')
    def test_get_db_commander(self, mock_db_registry, variable_manager):
        """DB Commander 조회 테스트"""
        mock_commander = Mock(spec=DbCommander)
        mock_db_registry.get_commander.return_value = mock_commander
        
        result = variable_manager.get_db_commander("test_db")
        
        mock_db_registry.get_commander.assert_called_once_with("test_db")
        assert result == mock_commander
    
    @patch('lib.core.variable_manager.DatabaseRegistry')
    def test_set_db_commander(self, mock_db_registry, variable_manager):
        """DB Commander 설정 테스트"""
        mock_commander = Mock(spec=DbCommander)
        mock_db_registry.get_commander.return_value = None
        
        variable_manager.set_db_commander("test_db", mock_commander)
        
        mock_db_registry.get_commander.assert_called_once_with("test_db")
        mock_db_registry.set_commander.assert_called_once_with("test_db", mock_commander)
    
    @patch('lib.core.variable_manager.DatabaseRegistry')
    def test_set_db_commander_existing_error(self, mock_db_registry, variable_manager):
        """이미 존재하는 DB Commander 설정 시 에러 테스트"""
        mock_commander = Mock(spec=DbCommander)
        mock_db_registry.get_commander.return_value = Mock(spec=DbCommander)  # 이미 존재하는 DB
        
        with pytest.raises(KavanaValueError, match="데이터베이스 `test_db` 가 이미 존재합니다."):
            variable_manager.set_db_commander("test_db", mock_commander)