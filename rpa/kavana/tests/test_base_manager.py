import pytest
from lib.core.managers.base_manager import BaseManager

class MockExecutor:
    """Mock Executor for testing BaseManager."""
    def __init__(self):
        self.logs = []
        self.errors = []

    def log_command(self, level, message):
        self.logs.append((level, message))

    def raise_command(self, message):
        self.errors.append(message)
        raise RuntimeError(message)

@pytest.fixture
def mock_executor():
    """Mock executor fixture."""
    return MockExecutor()

@pytest.fixture
def base_manager(mock_executor):
    # 싱글톤 리셋
    BaseManager._instances = {}
    return BaseManager(executor=mock_executor)

def test_singleton_behavior():
    """Test that BaseManager behaves as a singleton."""
    manager1 = BaseManager()
    manager2 = BaseManager()
    assert manager1 is manager2

def test_log_with_executor(base_manager, mock_executor):
    """Test log method with an executor."""
    base_manager.log("INFO", "Test log message")
    # assert mock_executor.logs == [("INFO", "Test log message")]
    assert ("INFO", "Test log message") in mock_executor.logs

def test_log_without_executor():
    """Test log method without an executor."""
    manager = BaseManager()
    # No exception should be raised, and output should go to print
    manager.log("INFO", "Test log message")

def test_raise_error_with_executor(base_manager, mock_executor):
    """Test raise_error method with an executor."""
    with pytest.raises(RuntimeError, match="Test error message"):
        base_manager.raise_error("Test error message")
    assert mock_executor.errors == ["Test error message"]

def test_raise_error_without_executor():
    """Test raise_error method without an executor."""
    manager = BaseManager()
    with pytest.raises(RuntimeError, match="Test error message"):
        manager.raise_error("Test error message")

