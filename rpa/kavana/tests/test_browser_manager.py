import pytest
from unittest.mock import MagicMock, patch
from lib.core.managers.browser_manager import BrowserManager

@pytest.fixture
def mock_executor():
    """Mock executor for testing."""
    class MockExecutor:
        def log_command(self, level, message):
            print(f"{level}: {message}")
        def set_variable(self, name, value):
            print(f"Variable set: {name} = {value}")
        def raise_command(self, message):
            print(f"Command failed: {message}")
    return MockExecutor()

@pytest.fixture
def browser_manager(mock_executor):
    """Setup BrowserManager with a mock executor."""
    return BrowserManager(executor=mock_executor, command="open", url="http://example.com")

@patch("lib.core.managers.browser_manager.webdriver.Chrome")
def test_open_browser(mock_chrome, browser_manager):
    """Test open_browser method."""
    mock_driver = MagicMock()
    mock_chrome.return_value = mock_driver

    browser_manager.execute()
    mock_driver.get.assert_called_once_with("http://example.com")

@patch("lib.core.managers.browser_manager.webdriver.Chrome")
@patch("lib.core.managers.browser_manager.WebDriverWait")
def test_click(mock_wait, mock_chrome, browser_manager):
    """Test click method."""
    browser_manager.command = "click"
    browser_manager.options = {
        "select": "#button",
        "select_by": "css",
        "timeout": 10
    }

    mock_driver = MagicMock()
    mock_element = MagicMock()
    mock_chrome.return_value = mock_driver

    # WebDriverWait().until(...)이 mock_element를 반환하게 설정
    mock_wait.return_value.until.return_value = mock_element

    browser_manager.execute()

    mock_element.click.assert_called_once()

@patch("lib.core.managers.browser_manager.webdriver.Chrome")
@patch("lib.core.managers.browser_manager.WebDriverWait")
def test_put_text(mock_wait, mock_chrome, browser_manager):
    browser_manager.command = "put_text"
    browser_manager.options = {
        "select": "#input",
        "select_by": "css",
        "text": "Hello, World!",
        "timeout": 10,
        "scroll_first": False,
        "clear_before": True  # ✅ 핵심 옵션!
    }

    mock_driver = MagicMock()
    mock_element = MagicMock()
    mock_chrome.return_value = mock_driver
    mock_wait.return_value.until.return_value = mock_element

    browser_manager.execute()

    mock_element.clear.assert_called_once()
    mock_element.send_keys.assert_called_once_with("Hello, World!")


@patch("lib.core.managers.browser_manager.webdriver.Chrome")
def test_capture(mock_chrome, browser_manager):
    browser_manager.command = "capture"
    browser_manager.options = {
        "to_file": "screenshot.png"
    }

    mock_driver = MagicMock()
    mock_chrome.return_value = mock_driver

    # 💡 _get_driver()가 mock_driver를 반환하게 강제
    browser_manager._get_driver = MagicMock(return_value=mock_driver)

    browser_manager.execute()

    mock_driver.save_screenshot.assert_called_once_with("screenshot.png")
