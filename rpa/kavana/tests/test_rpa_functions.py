import pytest
from lib.core.builtins.rpa_functions import RpaFunctions
from lib.core.token import Token, NoneToken
from lib.core.token_custom import WindowToken, RegionToken
from lib.core.datatypes.array import Array
from lib.core.token_type import TokenType

@pytest.fixture
def mock_executor():
    """Mock executor for testing."""
    class MockExecutor:
        def log_command(self, level, message):
            print(f"{level}: {message}")
    return MockExecutor()

@pytest.fixture
def setup_rpa_functions(mock_executor):
    """Setup RpaFunctions with a mock executor."""
    RpaFunctions.set_executor(mock_executor)

def test_window_list(setup_rpa_functions):
    """Test WINDOW_LIST function."""
    token = RpaFunctions.WINDOW_LIST()
    assert isinstance(token, Token)
    assert token.type == TokenType.ARRAY
    assert isinstance(token.data, Array)

def test_window_top(setup_rpa_functions):
    """Test WINDOW_TOP function."""
    token = RpaFunctions.WINDOW_TOP()
    assert isinstance(token, (WindowToken, NoneToken))

def test_window_region(setup_rpa_functions):
    """Test WINDOW_REGION function."""
    hwnd = 12345  # Example window handle
    token = RpaFunctions.WINDOW_REGION(hwnd)
    assert isinstance(token, NoneToken) or isinstance(token, RegionToken)
